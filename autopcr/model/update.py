"""Local, staged APK -> restored IL2CPP -> protocol generation in Python."""
import hashlib
import json
import os
import re
import shutil
import traceback
import uuid
import zipfile
from pathlib import Path

from ..constants import CACHE_DIR
from . import registry

def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        with temporary.open('w', encoding='utf-8') as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(str(temporary), str(path))
    finally:
        if temporary.exists():
            temporary.unlink()


def _tool_fingerprint():
    paths = sorted(Path(__file__).with_name('il2cpp').glob('*.py')) + [Path(__file__)]
    return hashlib.sha256(''.join(file_hash(p) for p in paths).encode()).hexdigest()


def archive_digest(archive, manifest):
    """Fingerprint the package from its central directory alone.

    Reading the entry table costs a few megabytes; the split APK payloads are
    never fetched. Sizes and CRCs of the declared splits identify a build, so a
    finished generation can be recognised before downloading anything.
    """
    wanted = {split['file'] for split in manifest['split_apks']}
    entries = {}
    for info in archive.infolist():
        if info.filename in wanted:
            entries[info.filename] = [info.file_size, info.compress_size, info.CRC]
    if set(entries) != wanted:
        raise registry.ProtocolError('Package does not contain every declared split APK')
    return hashlib.sha256(json.dumps(entries, sort_keys=True).encode()).hexdigest()


def _cache_name(version):
    return re.sub(r'[^A-Za-z0-9._-]', '_', str(version)).strip('.') or 'unknown'


def _state_of(run, version, sign, libcount, generation):
    return {'version': version, 'sign': sign, 'libcount': libcount, 'models': {
        'directory': (run / 'models').relative_to(Path(CACHE_DIR).resolve()).as_posix(),
        'sha256': generation.fingerprint,
    }}


def _reusable_run(cache, manifest, build_hash, digest):
    """Find a finished generation built from exactly this package and toolset."""
    for run in sorted(cache.glob(_cache_name(manifest['version_name']) + '-*')):
        if not (run / 'complete.json').exists():
            continue
        try:
            info = json.loads((run / 'input.json').read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        if (info.get('tools_sha256') == build_hash and info.get('manifest') == manifest
                and info.get('archive_sha256') == digest
                and info.get('sign') is not None and info.get('libcount') is not None):
            return run, info
    return None


def _load_cached(run, info, version):
    """Load a cached generation, or None when the cache cannot be trusted."""
    try:
        complete = json.loads((run / 'complete.json').read_text(encoding='utf-8'))
        generation = registry.load_generation(run / 'models', version, complete['models_sha256'])
    except Exception as error:
        print('Cached protocol models for %s are unusable (%s); rebuilding'
              % (version, error), flush=True)
        return None
    return generation, info['sign'], info['libcount']


def _generate(run):
    from .il2cpp.recovery import restore
    from .il2cpp.protocol import generate

    log = run / 'pipeline.log'
    with log.open('a', encoding='utf-8') as stream:
        def report(message):
            print('Protocol update: ' + message, flush=True)
            stream.write(message + '\n')
            stream.flush()
        try:
            library = restore(run, report)
            report('Reading IL2CPP metadata and generating Python models')
            result = generate(library, library.with_name('global-metadata.dat'), run / 'models')
            report(json.dumps(result, ensure_ascii=False))
        except Exception as error:
            stream.write(traceback.format_exc())
            raise registry.ProtocolError('Python protocol build failed; see %s: %s' % (log, error)) from error


def prepare_models(archive, manifest):
    """Use the already-open downloader archive; do not download a second copy."""
    if manifest.get('package_name') != 'com.aniplex.magia.exedra.en':
        raise registry.ProtocolError('Unexpected package: ' + str(manifest.get('package_name')))
    cache = Path(CACHE_DIR).resolve() / 'protocol'
    cache.mkdir(parents=True, exist_ok=True)
    version = str(manifest['version_name'])
    build_hash = _tool_fingerprint()
    digest = archive_digest(archive, manifest)
    # Recognise a finished generation from the package directory alone, so a
    # restart, a rebuilt toolset or a kill during the download never repeats it.
    reuse = _reusable_run(cache, manifest, build_hash, digest)
    if reuse is not None:
        cached = _load_cached(reuse[0], reuse[1], version)
        if cached is not None:
            generation, sign, libcount = cached
            print('Reusing cached protocol models: ' + reuse[0].name, flush=True)
            return generation, _state_of(reuse[0], version, sign, libcount, generation)
    staging = cache / ('extract-' + uuid.uuid4().hex)
    extracted = staging / 'extracted/il2cpp'
    extracted.mkdir(parents=True)
    sign = None
    libcount = None
    try:
        for split in manifest['split_apks']:
            # Spooled split APKs avoid holding an extra full copy in RAM.
            split_path = staging / 'split.apk'
            with archive.open(split['file']) as source, split_path.open('wb') as target:
                shutil.copyfileobj(source, target, 4 * 1024 * 1024)
            if split['id'] == 'base':
                digest_md5 = hashlib.md5()
                with split_path.open('rb') as stream:
                    for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b''):
                        digest_md5.update(chunk)
                sign = digest_md5.hexdigest()
            with zipfile.ZipFile(split_path) as apk:
                names = apk.namelist()
                if split['id'] == 'config.arm64_v8a':
                    libcount = len([n for n in names if n.startswith('lib/arm64-v8a/')])
                for name in names:
                    if not (name == 'lib/arm64-v8a/libil2cpp.so' or name.endswith('/global-metadata.dat')):
                        continue
                    target = extracted / Path(name).name
                    if target.exists():
                        raise registry.ProtocolError('Ambiguous input: ' + target.name)
                    with apk.open(name) as source, target.open('wb') as output:
                        shutil.copyfileobj(source, output, 4 * 1024 * 1024)
            split_path.unlink()
        if sign is None or libcount is None:
            raise registry.ProtocolError('Missing base or ARM64 split')
        hashes = {name: file_hash(extracted / name) for name in ('libil2cpp.so', 'global-metadata.dat')}
        identity = hashlib.sha256(json.dumps([manifest, hashes, build_hash], sort_keys=True).encode()).hexdigest()
        run = cache / (_cache_name(version) + '-' + identity[:16])
        # Both targets are verified before moving the staging directory.
        staging.resolve().relative_to(cache.resolve())
        run.resolve().relative_to(cache.resolve())
        if run.exists():
            for name, expected in hashes.items():
                if file_hash(run / 'extracted/il2cpp' / name) != expected:
                    raise registry.ProtocolError('Cached input checksum mismatch')
        else:
            staging.rename(run)
        # Recorded before the build so a later run can recognise this package
        # without downloading it, and refreshed in place for caches built before
        # the package digest existed.
        record = {'manifest': manifest, 'sha256': hashes, 'tools_sha256': build_hash,
                  'archive_sha256': digest, 'sign': sign, 'libcount': libcount}
        recorded = run / 'input.json'
        if recorded.exists():
            try:
                record = dict(json.loads(recorded.read_text(encoding='utf-8')), **record)
            except (OSError, ValueError):
                pass
        atomic_json(recorded, record)
        complete = run / 'complete.json'
        if complete.exists():
            info = json.loads(complete.read_text(encoding='utf-8'))
            generation = registry.load_generation(run / 'models', version, info['models_sha256'])
        else:
            _generate(run)
            generation = registry.load_generation(run / 'models', version)
            atomic_json(complete, {'models_sha256': generation.fingerprint})
        return generation, _state_of(run, version, sign, libcount, generation)
    finally:
        if staging.exists():
            staging.resolve().relative_to(cache.resolve())
            shutil.rmtree(staging)
