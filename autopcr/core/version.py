"""Update app signing data and protocol models as one committed generation."""
import asyncio
import json
import threading
from pathlib import Path
from ..constants import CACHE_DIR
from ..util import streamzip


class AppInfo:
    def __init__(self):
        self._state = {
            'version': '2.6.0', 'sign': '94bf87cd37b5a4f527f4fa5051929454', 'libcount': 0x1f,
        }

    @property
    def version(self): return self._state['version']
    @property
    def sign(self): return self._state['sign']
    @property
    def libcount(self): return self._state['libcount']
    @property
    def sm(self):
        state = self._state
        return f"d{state['sign']}o{state['libcount']}1E88A0177575728C9A399A9BD1F43A11D4100065n"

    def set_version(self, value): self._state = dict(self._state, version=value)
    def set_md5(self, value): self._state = dict(self._state, sign=value)
    def set_libcount(self, value): self._state = dict(self._state, libcount=value)
    def apply(self, state): self._state = dict(state)


version_info = AppInfo()
PATH = str(Path(CACHE_DIR) / 'version.json')
DOWNLOAD_URL = 'https://d.apkpure.net/b/XAPK/com.aniplex.magia.exedra.en?version=latest'
update_lck = asyncio.Lock()
_sync_update_lock = threading.Lock()


def load_version_info():
    with open(PATH, 'r', encoding='utf-8') as stream:
        data = json.load(stream)
    for key in ('version', 'sign', 'libcount'):
        if key not in data: raise ValueError('Invalid version state: missing ' + key)
    version_info.apply(data)


def save_version_info():
    from ..model.update import atomic_json
    atomic_json(PATH, version_info._state)


try:
    load_version_info()
except FileNotFoundError:
    # Do not create files merely by importing model classes.
    pass


def _update_version_sync(source=None, activate=True):
    from ..model import registry
    from ..model.update import prepare_models, atomic_json
    with _sync_update_lock:
        print(f'Checking app/protocol update from {version_info.version}...', flush=True)
        with streamzip.StreamZip(str(source or DOWNLOAD_URL)) as archive:
            with archive.open('manifest.json') as stream:
                manifest = json.load(stream)
            version = str(manifest['version_name'])
            if (activate and version == version_info.version and version_info._state.get('models')
                    and registry.current().version == version):
                print(f'App and models are already at {version}', flush=True)
                return None
            try:
                generation, state = prepare_models(archive, manifest)
            except registry.ProtocolError:
                raise
            except Exception as exc:
                raise registry.ProtocolError('Protocol preparation failed: ' + str(exc)) from exc
        registry.check_activation(generation)
        if not activate:
            print('Prepared protocol models: ' + str(generation.directory), flush=True)
            return generation, state

        def commit():
            atomic_json(PATH, state)
            version_info.apply(state)
        registry.activate(generation, commit=commit)
        print(f'Updated app and protocol models to {version}', flush=True)
        return generation, state


async def update_version(rejected_version=None):
    state_before = version_info._state
    async with update_lck:
        if (version_info._state is not state_before or
                (rejected_version is not None and rejected_version != version_info.version)):
            return True
        result = await asyncio.get_event_loop().run_in_executor(None, _update_version_sync)
        return result is not None
