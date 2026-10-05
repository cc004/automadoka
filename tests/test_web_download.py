import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import _download_web as download
from autopcr.http_server.version import is_compatible_release, parse_release_version


def release(tag, **kwargs):
    return {
        'tag_name': tag,
        'assets': [{'name': 'web.zip',
                    'browser_download_url': f'https://example.com/{tag}/web.zip'}],
        **kwargs,
    }


class ReleaseSelectionTests(unittest.TestCase):
    def test_latest_incompatible_release_is_not_installed(self):
        tag, urls = download.select_compatible_release([
            release('1.9.0'), release('1.8.0'), release('1.7.1'), release('1.7.0'),
        ])
        self.assertEqual(tag, '1.7.1')
        self.assertEqual(urls, ['https://example.com/1.7.1/web.zip'])

    def test_highest_patch_is_selected_numerically_not_by_list_order(self):
        tag, _ = download.select_compatible_release([
            release('1.7.2'), release('v1.7.10'), release('1.7.9'),
        ])
        self.assertEqual(tag, 'v1.7.10')

    def test_drafts_prereleases_and_missing_archives_are_skipped(self):
        tag, urls = download.select_compatible_release([
            release('1.7.6', draft=True), release('1.7.5', prerelease=True),
            release('1.7.4-rc.1'), release('1.7.3', assets=[]),
            release('1.7.2', assets=[{'name': 'checksum.txt',
                                    'browser_download_url': 'https://example.com/checksum'}]),
            release('1.7.1'),
        ])
        self.assertEqual(tag, '1.7.1')
        self.assertEqual(len(urls), 1)

    def test_no_compatible_release_fails_instead_of_falling_back_to_latest(self):
        for releases in ([], [release('1.9.0')], [release('2.7.0')]):
            with self.subTest(releases=releases):
                with self.assertRaisesRegex(RuntimeError, '1.7.x'):
                    download.select_compatible_release(releases)

    def test_release_version_parser(self):
        self.assertEqual(parse_release_version(' v1.7.10 '), (1, 7, 10))
        for tag in ('1.7', '1.7.1-rc.1', '1.7.-1', 'latest', ''):
            self.assertIsNone(parse_release_version(tag))
        self.assertTrue(is_compatible_release('1.7.1'))
        self.assertFalse(is_compatible_release('1.9.0'))


class DownloaderTests(unittest.IsolatedAsyncioTestCase):
    async def test_pagination_finds_compatible_release_on_later_page(self):
        pages = [[release('1.9.0')] * 100, [release('1.7.1')]]
        calls = []

        class Response:
            status = 200

            def __init__(self, page):
                self.page = page

            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                pass

            def raise_for_status(self):
                pass

            async def json(self):
                return pages[self.page - 1]

        session_kwargs = []

        class Session:
            def __init__(self, **kwargs):
                session_kwargs.append(kwargs)

            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                pass

            def get(self, url, **kwargs):
                calls.append((url, kwargs))
                return Response(kwargs['params']['page'])

        with patch.object(download.aiohttp, 'ClientSession', Session):
            tag, _ = await download.get_latest_release_info('owner', 'repo')
        self.assertEqual(tag, '1.7.1')
        self.assertEqual(len(calls), 2)
        self.assertTrue(all(call[0].endswith('/releases') for call in calls))
        self.assertTrue(all('ssl' not in call[1] for call in calls))
        # 请求头（含可选的 Authorization）挂在 session 上
        self.assertEqual(len(session_kwargs), 1)
        self.assertIn('headers', session_kwargs[0])

    def test_github_token_header(self):
        with patch.dict(os.environ, {}, clear=False):
            for key in ('GITHUB_TOKEN', 'GH_TOKEN'):
                os.environ.pop(key, None)
            headers = download.github_headers()
            self.assertNotIn('Authorization', headers)
            self.assertTrue(headers['User-Agent'])

            os.environ['GITHUB_TOKEN'] = 'ghp_x'
            self.assertEqual(download.github_headers()['Authorization'], 'Bearer ghp_x')

            del os.environ['GITHUB_TOKEN']
            os.environ['GH_TOKEN'] = 'ghp_y'
            self.assertEqual(download.github_headers()['Authorization'], 'Bearer ghp_y')

    async def test_rate_limited_page_is_retried_then_reported(self):
        async def no_sleep(_delay):
            return None

        class FakeAsyncio:
            # 直接替换模块里的 asyncio，跳过退避等待（改 asyncio.sleep 会递归）
            sleep = staticmethod(no_sleep)

        class Response:
            def __init__(self, status):
                self.status = status
                self.headers = {}

            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                pass

            async def text(self):
                return '{"message":"API rate limit exceeded"}'

            async def json(self):
                return [release('1.7.1')]

            def raise_for_status(self):
                if self.status >= 400:
                    raise AssertionError('限流响应不应走到 raise_for_status')

        class Session:
            def __init__(self, **kwargs):
                self.seen = 0

            def get(self, url, **kwargs):
                self.seen += 1
                return Response(403 if self.seen <= 2 else 200)

        session = Session()
        with patch.object(download, 'asyncio', FakeAsyncio):
            batch = await download.fetch_releases_page(session, 'http://x', 1)
        self.assertEqual(session.seen, 3)
        self.assertEqual(batch, [release('1.7.1')])

        session = Session()
        with patch.object(download, 'asyncio', FakeAsyncio):
            with self.assertRaisesRegex(RuntimeError, 'GITHUB_TOKEN'):
                await download.fetch_releases_page(session, 'http://x', 1, retries=1)

    async def test_installed_version_check_repairs_missing_frontend(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(download, 'path', directory):
            web = Path(directory) / 'autopcr' / 'http_server'
            web.mkdir(parents=True)
            (web / 'client_version').write_text('1.7.1')
            self.assertTrue(await download.check_version('1.7.1'))
            (web / 'ClientApp').mkdir()
            (web / 'ClientApp' / 'index.html').write_text('<html></html>')
            self.assertFalse(await download.check_version('1.7.1'))
            self.assertTrue(await download.check_version('1.7.2'))


if __name__ == '__main__':
    unittest.main()
