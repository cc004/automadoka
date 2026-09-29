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
                digest = hashlib.md5()
                with split_path.open('rb') as stream:
                    for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b''):
                        digest.update(chunk)
                sign = digest.hexdigest()
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
        build_hash = _tool_fingerprint()
        identity = hashlib.sha256(json.dumps([manifest, hashes, build_hash], sort_keys=True).encode()).hexdigest()
        version = str(manifest['version_name'])
        safe_version = re.sub(r'[^A-Za-z0-9._-]', '_', version).strip('.') or 'unknown'
        run = cache / (safe_version + '-' + identity[:16])
        # Both targets are verified before moving the staging directory.
        staging.resolve().relative_to(cache.resolve())
        run.resolve().relative_to(cache.resolve())
        if run.exists():
            for name, digest in hashes.items():
                if file_hash(run / 'extracted/il2cpp' / name) != digest:
                    raise registry.ProtocolError('Cached input checksum mismatch')
        else:
            staging.rename(run)
        complete = run / 'complete.json'
        if complete.exists():
            info = json.loads(complete.read_text(encoding='utf-8'))
            generation = registry.load_generation(run / 'models', version, info['models_sha256'])
        else:
            atomic_json(run / 'input.json', {'manifest': manifest, 'sha256': hashes, 'tools_sha256': build_hash})
            _generate(run)
            generation = registry.load_generation(run / 'models', version)
            atomic_json(complete, {'models_sha256': generation.fingerprint})
        state = {'version': version, 'sign': sign, 'libcount': libcount, 'models': {
            'directory': (run / 'models').relative_to(Path(CACHE_DIR).resolve()).as_posix(),
            'sha256': generation.fingerprint,
        }}
        return generation, state
    finally:
        if staging.exists():
            staging.resolve().relative_to(cache.resolve())
            shutil.rmtree(staging)
