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


def github_headers():
    """GitHub API 请求头。

    配置 GITHUB_TOKEN（或 GH_TOKEN）后走认证请求，限额从 60 次/小时
    提升到 5000 次/小时。Docker 构建、共享出口 IP 或代理环境下很容易
    撞到匿名限额（403 rate limit exceeded），建议传一个只读 token。
    """
    headers = {
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'autopcr-download-web',
    }
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers


def _rate_limit_hint(response):
    import datetime
    parts = []
    if github_headers().get('Authorization'):
        parts.append('已配置 GITHUB_TOKEN')
    else:
        parts.append('未配置 GITHUB_TOKEN，匿名请求仅 60 次/小时')
    reset = response.headers.get('x-ratelimit-reset')
    if reset and reset.isdigit():
        parts.append('限额将于 %s 重置' % datetime.datetime.fromtimestamp(
            int(reset)).strftime('%Y-%m-%d %H:%M:%S'))
    return '；'.join(parts)


async def fetch_releases_page(session, url, page, retries=4):
    """拉取一页 releases；遇到限流或临时错误按指数退避重试。"""
    delay = 2
    for attempt in range(retries + 1):
        async with session.get(url, params={'per_page': 100, 'page': page}) as response:
            if response.status in (403, 429):
                body = await response.text()
                if attempt >= retries:
                    raise RuntimeError(
                        f'GitHub API 返回 {response.status}（{_rate_limit_hint(response)}）。\n'
                        f'可设置环境变量 GITHUB_TOKEN 后重试。\n{body[:300]}')
                print(f'GitHub API 限流（{response.status}），{delay}s 后重试'
                      f'（{attempt + 1}/{retries}）：{_rate_limit_hint(response)}')
                await asyncio.sleep(delay)
                delay *= 2
                continue
            response.raise_for_status()
            return await response.json()


async def get_latest_release_info(owner, repo):
    # /releases/latest may belong to an incompatible API minor version.
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    releases = []
    async with aiohttp.ClientSession(headers=github_headers()) as session:
        page = 1
        while True:
            batch = await fetch_releases_page(session, url, page)
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
