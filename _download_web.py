import asyncio
import aiohttp
import os
import shutil

from autopcr.http_server.version import (
    APP_VERSION_MAJOR, APP_VERSION_MINOR, is_compatible_release,
    parse_release_version,
)


def select_compatible_release(releases):
    """Select the highest stable patch release supported by this backend."""
    compatible = []
    for release in releases:
        tag = release.get('tag_name', '')
        if (release.get('draft') or release.get('prerelease')
                or not is_compatible_release(tag)):
            continue
        urls = [asset['browser_download_url']
                for asset in release.get('assets', [])
                if asset.get('name', '').endswith('.zip')
                and asset.get('browser_download_url')]
        if urls:
            compatible.append((parse_release_version(tag), tag, urls))
    if not compatible:
        raise RuntimeError(
            f"没有找到后端兼容的前端 {APP_VERSION_MAJOR}.{APP_VERSION_MINOR}.x，"
            "请检查 AutoPCR_Web releases；不要安装不兼容的最新版本。"
        )
    _, tag, urls = max(compatible, key=lambda release: release[0])
    return tag, urls


async def get_latest_release_info(owner, repo):
    # /releases/latest may belong to an incompatible API minor version.
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    releases = []
    async with aiohttp.ClientSession() as session:
        page = 1
        while True:
            async with session.get(url, params={'per_page': 100, 'page': page}) as response:
                response.raise_for_status()
                batch = await response.json()
            releases.extend(batch)
            if len(batch) < 100:
                break
            page += 1
    return select_compatible_release(releases)

path = os.path.dirname(os.path.abspath(__file__))

async def check_version(version):
    now_version = None
    web_version = os.path.join(path, "autopcr", "http_server", "client_version")
    if os.path.exists(web_version):
        with open(web_version, "r") as f:
            now_version = f.read().strip()
    version = version.strip()
    index = os.path.join(path, "autopcr", "http_server", "ClientApp", "index.html")
    if not now_version or now_version != version or not os.path.isfile(index):
        return True
    return False

async def save_version(version):
    web_version = os.path.join(path, "autopcr", "http_server", "client_version")
    with open(web_version, "w") as f:
        f.write(version)

async def download_assets(asset_download_urls):
    ret = []
    async with aiohttp.ClientSession() as session:
        for url in asset_download_urls:
            async with session.get(url) as response:
                if response.status == 200:
                    filename = url.split('/')[-1]
                    filepath = os.path.join(path, filename)
                    print(f"Downloading {filename} -> {filepath}")
                    with open(filepath, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                    ret.append(filepath)
                else:
                    print(f"Failed to download {url}")
                    raise Exception(f"Failed to download {url}")
    return ret

async def extract_web(filepaths):
    web_path = os.path.join(path, "autopcr", "http_server", "ClientApp")
    if not os.path.exists(web_path):
        os.makedirs(web_path)

    print(f"Removed old web file")
    shutil.rmtree(web_path)

    for filepath in filepaths:
        print(f"Unzipped {filepath}")
        import zipfile
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(web_path)

        print(f"Delete {filepath}")
        os.remove(filepath)

async def do_download():
    owner = 'Lanly109'
    repo = 'AutoPCR_Web'
    latest_release_tag, asset_download_urls = await get_latest_release_info(owner, repo)
    if latest_release_tag and asset_download_urls:
        print(f"Latest compatible release tag: {latest_release_tag} "
              f"(backend API {APP_VERSION_MAJOR}.{APP_VERSION_MINOR})")
        if await check_version(latest_release_tag):
            filepaths = await download_assets(asset_download_urls)
            await extract_web(filepaths)
            await save_version(latest_release_tag)
        else:
            print("Already up to date")
    else:
        print("Failed to fetch latest release info")
        raise Exception("Failed to fetch latest release info")

async def main(zips):
    if zips:
        await extract_web(zips)
    else:
        await do_download()


if __name__ == "__main__":
    import sys
    zips = sys.argv[1:]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(zips))
