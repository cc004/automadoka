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

        class Session:
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
