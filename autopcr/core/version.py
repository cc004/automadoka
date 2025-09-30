import asyncio, hashlib, zipfile, os, json, requests, io
from ..constants import CACHE_DIR
from ..util.streamzip import StreamZip

class AppInfo:
    def __init__(self):
        pass

    def set_version(self, v: str):
        self.version = v
    
    def set_md5(self, sign: str):
        self.sign = sign

    def set_libcount(self, count: int):
        self.libcount = count
    
    @property
    def sm(self) -> str:
        return f'd{self.sign}o{self.libcount}1E88A0177575728C9A399A9BD1F43A11D4100065n'

version_info: AppInfo = AppInfo()
version_info.set_version("2.6.0")
version_info.set_md5("94bf87cd37b5a4f527f4fa5051929454")
version_info.set_libcount(0x1f)

PATH = os.path.join(CACHE_DIR, 'version.json')

def load_version_info():
    with open(PATH, 'rb') as f:
        data = json.load(f)
    
    version_info.set_version(data['version'])
    version_info.set_md5(data['sign'])
    version_info.set_libcount(data['libcount'])
        
    print(f'Loaded version info: {version_info.version}, {version_info.sign}, {version_info.libcount}')

def save_version_info():
    data = {
        'version': version_info.version,
        'sign': version_info.sign,
        'libcount': version_info.libcount
    }
    with open(PATH, 'w') as f:
        json.dump(data, f)
    
    print(f'Saved version info: {version_info.version}, {version_info.sign}, {version_info.libcount}')

update_lck = asyncio.Lock()

try:
    load_version_info()
except:
    save_version_info()

from typing import IO

def _update_version_sync():
    print(f'Updating version from {version_info.version}...')
    url = 'https://d.apkpure.net/b/XAPK/com.aniplex.magia.exedra.jp?version=latest'
    print(f'Downloading latest version from {url} ...')

    file = StreamZip(url)

    with file.open('manifest.json') as fp:
        manifest = json.load(fp)
    
    version = manifest['version_name']

    if version == version_info.version:
        print(f'Already the latest version {version}, skip updating')
        return

    base_apk = next(f for f in manifest['split_apks'] if f['id'] == 'base')
    lib_apk = next(f for f in manifest['split_apks'] if f['id'] == 'config.arm64_v8a')

    with file.open(base_apk['file']) as apk_fp:
        apk_data = apk_fp.read()
        md5 = hashlib.md5(apk_data).hexdigest()

    with file.open(lib_apk['file']) as apk_fp:
        with zipfile.ZipFile(apk_fp) as apk_zip:
            lib_files = [f for f in apk_zip.namelist() if f.startswith('lib/arm64-v8a/')]
            libcount = len(lib_files)

    version_info.set_version(version)
    version_info.set_md5(md5)
    version_info.set_libcount(libcount)

    save_version_info()
    print(f'Updated to version {version_info.version}, sign {version_info.sign}, libcount {version_info.libcount}')

import sys

if sys.gettrace() is None:
    _update_version_sync()

async def update_version():
    version_to_update = version_info.version
    async with update_lck:
        if version_to_update != version_info.version:
            print(f'Another coroutine updated version to {version_info.version}, skip updating {version_to_update}')
            return
        
        asyncio.get_event_loop().run_in_executor(None, _update_version_sync)
        

