"""Package-directory cache probe and resumable download spool."""
import io
import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from autopcr.model import registry, update
from autopcr.model.il2cpp.protocol import render_models
from autopcr.util import streamzip


PACKAGE = 'com.aniplex.magia.exedra.en'
SPLITS = (('base.apk', 'base'), ('config.arm64_v8a.apk', 'config.arm64_v8a'))


def archive_of(payloads):
    """A real zip, so infolist() carries sizes and CRCs like an XAPK."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as handle:
        for name, payload in payloads.items():
            handle.writestr(name, payload)
    buffer.seek(0)
    return zipfile.ZipFile(buffer)


def manifest_of(version='3.19.1', splits=SPLITS):
    return {'package_name': PACKAGE, 'version_name': version,
            'split_apks': [{'file': name, 'id': identifier} for name, identifier in splits]}


def split_payloads(**changes):
    payloads = {name: name.encode() for name, _ in SPLITS}
    payloads.update(changes)
    return payloads


class ArchiveDigestTests(unittest.TestCase):
    def test_unrelated_entries_do_not_change_the_digest(self):
        manifest = manifest_of()
        plain = archive_of(split_payloads())
        decorated = archive_of(split_payloads(icon=b'x', manifest_json=b'{}'))
        self.assertEqual(update.archive_digest(plain, manifest),
                         update.archive_digest(decorated, manifest))

    def test_split_payload_change_changes_the_digest(self):
        manifest = manifest_of()
        before = archive_of(split_payloads())
        after = archive_of(split_payloads(**{'config.arm64_v8a.apk': b'rebuilt'}))
        self.assertNotEqual(update.archive_digest(before, manifest),
                            update.archive_digest(after, manifest))

    def test_missing_declared_split_is_rejected(self):
        archive = archive_of({'base.apk': b'base.apk'})
        with self.assertRaises(update.registry.ProtocolError):
            update.archive_digest(archive, manifest_of())


def make_run(cache, name, manifest, build_hash, digest, complete=True):
    run = Path(cache) / name
    run.mkdir(parents=True)
    (run / 'input.json').write_text(json.dumps({
        'manifest': manifest, 'sha256': {'libil2cpp.so': 'a', 'global-metadata.dat': 'b'},
        'tools_sha256': build_hash, 'archive_sha256': digest,
        'sign': 'sign', 'libcount': 7}), encoding='utf-8')
    if complete:
        (run / 'complete.json').write_text(json.dumps({'models_sha256': 'unused'}), encoding='utf-8')
    return run


class ReusableRunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.cache = Path(self.temp.name)
        self.manifest = manifest_of()
        self.digest = 'digest-1'

    def build(self, **overrides):
        values = {'manifest': self.manifest, 'build_hash': 'tools-1', 'digest': self.digest}
        values.update(overrides)
        return make_run(self.cache, '3.19.1-abcdef0123456789', **values)

    def probe(self, manifest=None, build_hash='tools-1', digest=None):
        return update._reusable_run(self.cache, manifest or self.manifest, build_hash,
                                    digest or self.digest)

    def test_matching_record_is_reused(self):
        run = self.build()
        found = self.probe()
        self.assertEqual(found[0], run)
        self.assertEqual(found[1]['sign'], 'sign')
        self.assertEqual(found[1]['libcount'], 7)

    def test_rebuilt_toolset_invalidates_the_record(self):
        self.build()
        self.assertIsNone(self.probe(build_hash='tools-2'))

    def test_rebuilt_package_invalidates_the_record(self):
        self.build()
        self.assertIsNone(self.probe(digest='digest-2'))

    def test_other_version_does_not_match(self):
        self.build()
        self.assertIsNone(self.probe(manifest=manifest_of(version='3.19.2')))

    def test_unfinished_run_is_ignored(self):
        self.build(complete=False)
        self.assertIsNone(self.probe())

    def test_record_without_package_digest_is_ignored(self):
        self.build(digest=None)
        self.assertIsNone(self.probe())

    def test_older_run_is_skipped_when_a_newer_one_matches(self):
        self.build(digest='digest-2')
        wanted = make_run(self.cache, '3.19.1-fedcba9876543210', self.manifest, 'tools-1',
                          self.digest)
        found = self.probe()
        self.assertEqual(found[0], wanted)


class LoadCachedTests(unittest.TestCase):
    def test_unusable_models_fall_back_to_rebuilding(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / '3.19.1-abcdef0123456789'
            (run / 'models').mkdir(parents=True)
            (run / 'complete.json').write_text(json.dumps({'models_sha256': 'x'}), encoding='utf-8')
            self.assertIsNone(update._load_cached(run, {'sign': 's', 'libcount': 1}, '3.19.1'))


class CountingArchive:
    """Stands in for the downloader archive and records what was fetched."""

    def __init__(self, path):
        self.handle = zipfile.ZipFile(path)
        self.opened = []

    def infolist(self):
        return self.handle.infolist()

    def open(self, name):
        self.opened.append(name)
        return self.handle.open(name)


SCHEMA = {'enums': {'CacheMode': {'Idle': 0}},
          'common': {'CacheNode': {'mode': 'CacheMode', 'value': 'int'}},
          'apis': [{'url': '/api/cache_probe', 'request': 'CacheProbeRequest',
                    'response': 'CacheProbeResponse',
                    'request_fields': {'node': 'CacheNode'},
                    'response_fields': {'node': 'CacheNode'}}]}


def split_apk(entries):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as handle:
        for name, payload in entries.items():
            handle.writestr(name, payload)
    return buffer.getvalue()


def write_xapk(path, lib=b'libil2cpp-v1', metadata=b'metadata-v1'):
    base = split_apk({'AndroidManifest.xml': b'<manifest/>'})
    arm64 = split_apk({'lib/arm64-v8a/libil2cpp.so': lib,
                       'lib/arm64-v8a/libunity.so': b'unity',
                       'assets/bin/Data/Managed/global-metadata.dat': metadata})
    manifest = manifest_of()
    with zipfile.ZipFile(path, 'w') as handle:
        handle.writestr('manifest.json', json.dumps(manifest))
        handle.writestr('base.apk', base)
        handle.writestr('config.arm64_v8a.apk', arm64)
    return manifest


class PrepareModelsTests(unittest.TestCase):
    """The whole point: a finished generation is found without downloading."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.xapk = self.root / 'game.xapk'
        self.manifest = write_xapk(self.xapk)
        patcher = patch.object(update, 'CACHE_DIR', self.temp.name)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.generations = []
        self.addCleanup(self.unload)

    def unload(self):
        for generation in self.generations:
            registry._unload(generation.package)

    def build(self):
        archive = CountingArchive(self.xapk)
        self.addCleanup(archive.handle.close)

        def generate(run):
            return render_models(SCHEMA, run / 'models')

        with patch.object(update, '_generate', side_effect=generate):
            generation, state = update.prepare_models(archive, self.manifest)
        self.generations.append(generation)
        return archive, generation, state

    def test_first_build_downloads_and_records_the_package(self):
        archive, generation, state = self.build()
        self.assertIn('base.apk', archive.opened)
        self.assertIn('config.arm64_v8a.apk', archive.opened)
        record = json.loads((generation.directory.parent / 'input.json').read_text(encoding='utf-8'))
        self.assertRegex(record['sign'], r'^[0-9a-f]{32}$')
        self.assertRegex(record['archive_sha256'], r'^[0-9a-f]{64}$')
        self.assertEqual(record['libcount'], 2)
        self.assertEqual(state['libcount'], 2)
        self.assertEqual(state['sign'], record['sign'])

    def test_second_build_reads_nothing_from_the_archive(self):
        _, _, state = self.build()
        archive, _, again = self.build()
        self.assertEqual(archive.opened, [])
        self.assertEqual(again, state)

    def test_rebuilt_split_forces_a_download(self):
        _, _, state = self.build()
        write_xapk(self.xapk, lib=b'libil2cpp-v2')
        archive, _, rebuilt = self.build()
        self.assertTrue(archive.opened)
        self.assertNotEqual(rebuilt['models']['directory'], state['models']['directory'])

    def test_rebuilt_toolset_forces_a_download(self):
        _, _, state = self.build()
        with patch.object(update, '_tool_fingerprint', return_value='other-tools'):
            archive, _, rebuilt = self.build()
        self.assertTrue(archive.opened)
        self.assertNotEqual(rebuilt['models']['directory'], state['models']['directory'])

    def test_rebuild_is_not_attempted_when_the_cache_is_reusable(self):
        self.build()
        archive = CountingArchive(self.xapk)
        self.addCleanup(archive.handle.close)
        with patch.object(update, '_generate', side_effect=AssertionError('cache should be reused')):
            update.prepare_models(archive, self.manifest)


class CountingReader(streamzip.RangeReader):
    def __init__(self, payload):
        self.payload = payload
        self.fetches = []

    def total_size(self):
        return len(self.payload)

    def chunk(self, start, size):
        self.fetches.append((start, size))
        return self.payload[start:start + size]


class DownloadSpoolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

    def read_all(self, reader, payload, size=512):
        return b''.join(reader.chunk(start, size) for start in range(0, len(payload), size))

    def test_second_pass_never_touches_the_network(self):
        payload = bytes(range(256)) * 12
        first = CountingReader(payload)
        self.assertEqual(self.read_all(streamzip.DiskCacheReader(first, 'key', self.temp.name), payload),
                         payload)
        self.assertTrue(first.fetches)
        second = CountingReader(payload)
        self.assertEqual(self.read_all(streamzip.DiskCacheReader(second, 'key', self.temp.name), payload),
                         payload)
        self.assertEqual(second.fetches, [])

    def test_truncated_chunk_is_fetched_again(self):
        payload = b'0123456789'
        streamzip.DiskCacheReader(CountingReader(payload), 'key', self.temp.name).chunk(0, 10)
        stored = next(Path(self.temp.name).rglob('*.bin'))
        stored.write_bytes(b'012')
        again = CountingReader(payload)
        self.assertEqual(streamzip.DiskCacheReader(again, 'key', self.temp.name).chunk(0, 10), payload)
        self.assertEqual(again.fetches, [(0, 10)])

    def test_a_half_written_chunk_is_never_left_behind(self):
        payload = b'0123456789'
        reader = CountingReader(payload)
        streamzip.DiskCacheReader(reader, 'key', self.temp.name).chunk(0, 10)
        self.assertEqual(list(Path(self.temp.name).rglob('*.part')), [])

    def test_key_tracks_url_size_and_validator(self):
        class Head:
            def __init__(self, url, size, etag):
                self.url, self.size, self.etag = url, size, etag

            def total_size(self):
                return self.size

        base = streamzip.cache_key(Head('https://cdn/a', 100, 'v1'))
        self.assertEqual(base, streamzip.cache_key(Head('https://cdn/a', 100, 'v1')))
        self.assertNotEqual(base, streamzip.cache_key(Head('https://cdn/b', 100, 'v1')))
        self.assertNotEqual(base, streamzip.cache_key(Head('https://cdn/a', 101, 'v1')))
        self.assertNotEqual(base, streamzip.cache_key(Head('https://cdn/a', 100, 'v2')))

    def test_local_sources_are_not_spooled(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'game.xapk'
            path.write_bytes(b'xapk')
            reader = streamzip.create_range_reader(str(path))
            self.assertIsInstance(reader, streamzip.FileRangeReader)
            reader.close()


class PruneDownloadCacheTests(unittest.TestCase):
    def test_only_the_newest_spools_survive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index, name in enumerate(('old', 'middle', 'new')):
                (root / name).mkdir()
                os.utime(root / name, (1000 + index, 1000 + index))
            self.assertEqual(sorted(streamzip.prune_download_cache(root, keep=1)), ['middle', 'old'])
            self.assertEqual([path.name for path in root.iterdir()], ['new'])

    def test_absent_root_is_not_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(streamzip.prune_download_cache(Path(tmp) / 'absent'), [])


if __name__ == '__main__':
    unittest.main()
