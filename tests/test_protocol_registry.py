import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from autopcr.model import registry
from autopcr.model.modelbase import Response, RequestBase
from autopcr.core import version


def write_generation(root, number):
    root.mkdir(parents=True)
    files = {
        'enums': 'from enum import IntEnum\nclass TestMode(IntEnum):\n    Active = %d\n' % number,
        'common': '''from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List
from .enums import *
class TestItem(BaseModel):
    value: int = None
    json_: str = Field(None, alias='json')
    children: List[TestItem] = None
''',
        'responses': '''from .modelbase import ResponseBase
from .common import *
class TestResponse(ResponseBase):
    item: TestItem = None
    revision: int = %d
''' % number,
        'requests': '''from .modelbase import RequestBase, MstRequestBase
from .responses import *
from .common import *
class TestRequest(RequestBase[TestResponse]):
    item: TestItem = None
    appVersion: str = None
    revision: int = %d
    @property
    def url(self): return '/api/test'
class TestMstRequest(MstRequestBase[TestItem]):
    @property
    def url(self): return '/api/mst/test'
''' % number,
    }
    for name, content in files.items():
        (root / (name + '.py')).write_text(content, encoding='utf-8')
    return registry.load_generation(root, str(number))


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.previous = registry.current()
        self.handlers = dict(registry._handlers)
        registry._handlers.clear()
        self.state = version.version_info._state
        self.temp = tempfile.TemporaryDirectory()
        self.first = write_generation(Path(self.temp.name) / 'one', 1)
        self.second = write_generation(Path(self.temp.name) / 'two', 2)
        registry.activate(self.first)

    def tearDown(self):
        registry._handlers.clear()
        registry._handlers.update(self.handlers)
        registry.activate(self.previous)
        version.version_info.apply(self.state)
        self.temp.cleanup()

    def test_saved_import_constructor_classmethod_nested_model_and_enum(self):
        request = registry.proxy('requests', 'TestRequest')
        response = registry.proxy('responses', 'TestResponse')
        item = registry.proxy('common', 'TestItem')
        mode = registry.proxy('enums', 'TestMode')
        parse = response.parse_obj
        before = request()
        registry.activate(self.second)
        after = request()
        self.assertIsNot(type(before), type(after))
        self.assertTrue(isinstance(before, request))
        self.assertTrue(issubclass(type(after), request))
        self.assertIs(registry.proxy('requests', 'TestRequest'), request)
        parsed = parse({'item': {'value': 3, 'json': 'wire', 'children': [{'value': 4}]}})
        self.assertEqual(parsed.revision, 2)
        self.assertIs(type(parsed.item), self.second.classes['common']['TestItem'])
        self.assertEqual(parsed.item.children[0].value, 4)
        self.assertEqual(parsed.item.dict(by_alias=True)['json'], 'wire')
        self.assertIs(type(item(value=2)), type(parsed.item))
        self.assertEqual(mode.Active, 2)
        self.assertEqual(mode(2), mode.Active)

    def test_inflight_response_and_mst_stay_on_request_generation(self):
        request = registry.proxy('requests', 'TestRequest')()
        mst = registry.proxy('requests', 'TestMstRequest')()
        registry.activate(self.second)
        parsed = Response[request.__response_type__].parse_obj({'payload': {'item': {'value': 7}}})
        self.assertEqual(parsed.payload.revision, 1)
        self.assertIs(type(parsed.payload.item), self.first.classes['common']['TestItem'])
        master = Response[mst.__response_type__].parse_obj({'payload': {'mstList': [{'value': 8}]}})
        self.assertIs(type(master.payload.mstList[0]), self.first.classes['common']['TestItem'])

    def test_queued_request_rebound_with_new_signing_info(self):
        request = registry.proxy('requests', 'TestRequest')(appVersion='old', item={'value': 9})
        registry.activate(self.second, commit=lambda: version.version_info.apply(
            {'version': '2', 'sign': 'new-sign', 'libcount': 11}))
        rebound = registry.bind_request(request)
        self.assertIs(type(rebound), self.second.classes['requests']['TestRequest'])
        self.assertEqual(rebound.item.value, 9)
        self.assertEqual(rebound.appVersion, '2')
        expected_sm = version.version_info.sm
        version.version_info.set_md5('later-sign')
        rebound.prepare()
        self.assertEqual(rebound.sm, expected_sm)

    def test_handlers_apply_to_both_generations(self):
        async def update(self, manager, request):
            manager.append(self.revision)
        registry.register_handler('TestResponse', update)
        old = registry.proxy('responses', 'TestResponse')()
        registry.activate(self.second)
        new = registry.proxy('responses', 'TestResponse')()
        results = []
        asyncio.run(old.update(results, None))
        asyncio.run(new.update(results, None))
        self.assertEqual(results, [1, 2])

    def test_failed_load_and_failed_commit_leave_current_generation_unchanged(self):
        bad = Path(self.temp.name) / 'bad'
        bad.mkdir()
        for name in registry.KINDS:
            (bad / (name + '.py')).write_text('broken syntax @', encoding='utf-8')
        with self.assertRaises(SyntaxError):
            registry.load_generation(bad, 'broken')
        with self.assertRaises(OSError):
            registry.activate(self.second, commit=lambda: (_ for _ in ()).throw(OSError('disk full')))
        self.assertIs(registry.current(), self.first)
        self.assertEqual(version.version_info._state, self.state)

    def test_removed_type_does_not_silently_use_old_schema(self):
        unknown = registry.proxy('requests', 'RemovedRequest')
        with self.assertRaisesRegex(registry.ProtocolError, 'unavailable'):
            unknown()

    def test_bad_saved_checksum_is_rejected(self):
        with self.assertRaisesRegex(registry.ProtocolError, 'checksum'):
            registry.load_generation(self.first.directory, '1', 'bad-hash')

    def test_proxy_annotations_in_handwritten_pydantic_model_follow_updates(self):
        from pydantic import BaseModel
        Item = registry.proxy('common', 'TestItem')
        Mode = registry.proxy('enums', 'TestMode')
        class Envelope(BaseModel):
            item: Item
            mode: Mode
        registry.activate(self.second)
        parsed = Envelope(item={'value': 4}, mode=2)
        self.assertIs(type(parsed.item), self.second.classes['common']['TestItem'])
        self.assertEqual(parsed.mode, 2)

    def test_saved_generation_loads_after_restart_without_dumping(self):
        with patch.object(registry, 'CACHE_DIR', self.temp.name):
            state = {'version': '2', 'models': {'directory': 'two', 'sha256': self.second.fingerprint}}
            (Path(self.temp.name) / 'version.json').write_text(json.dumps(state))
            registry._active = None
            generation = registry.current()
            self.assertEqual(generation.version, '2')
            self.assertEqual(registry.proxy('requests', 'TestRequest')().revision, 2)


class VersionUpdateTests(unittest.TestCase):
    def test_http_428_preserves_update_exception_and_stops_when_no_update_exists(self):
        import importlib
        from types import SimpleNamespace
        api = importlib.import_module('autopcr.core.apiclient')
        from autopcr.model.requests import LoginApiLoginRequest
        class Client(api.apiclient):
            def get_crypto_key(self): return 'key'
            async def post_sign(self, data): return 'signature'
        async def post(*args, **kwargs): return SimpleNamespace(status_code=428)
        async def scenario():
            client = Client(SimpleNamespace(header=lambda: {}))
            client.servers = ['https://offline.invalid']
            for available, exception in ((True, api.VersionUpdatedException), (False, api.ApiException)):
                async def update(*args): return available
                with patch.object(api.aiorequests, 'post', post), \
                        patch.object(api, 'update_version', update), \
                        patch.object(api.crypto.PackHelper, 'pack', return_value=b'wire'), \
                        patch.object(api.crypto.PackHelper, 'get_iv', return_value=b'iv'):
                    with self.assertRaises(exception):
                        await client._request_internal(LoginApiLoginRequest())
        asyncio.run(scenario())

    def test_same_version_without_models_is_still_built(self):
        class Archive:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def open(self, name):
                import io
                return io.BytesIO(json.dumps({'version_name': version.version_info.version}).encode())
        original = version.version_info._state
        version.version_info.apply({k: original[k] for k in ('version', 'sign', 'libcount')})
        try:
            with patch.object(version.streamzip, 'StreamZip', return_value=Archive()), \
                    patch('autopcr.model.update.prepare_models', side_effect=RuntimeError('builder called')):
                with self.assertRaisesRegex(RuntimeError, 'builder called'):
                    version._update_version_sync('offline.xapk')
        finally:
            version.version_info.apply(original)

    def test_no_newer_version_returns_false_instead_of_retrying_forever(self):
        async def scenario():
            with patch.object(version, 'update_lck', asyncio.Lock()), \
                    patch.object(version, '_update_version_sync', return_value=None):
                self.assertFalse(await version.update_version(version.version_info.version))
        asyncio.run(scenario())

    def test_old_inflight_version_reuses_update_already_completed(self):
        async def scenario():
            with patch.object(version, 'update_lck', asyncio.Lock()), \
                    patch.object(version, '_update_version_sync') as update:
                self.assertTrue(await version.update_version('obsolete'))
                update.assert_not_called()
        asyncio.run(scenario())

    def test_failed_builder_preserves_version_file_and_runtime_state(self):
        class Archive:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def open(self, name):
                import io
                return io.BytesIO(json.dumps({'version_name': 'future'}).encode())
        original = version.version_info._state
        with tempfile.TemporaryDirectory() as tmp:
            state_file = Path(tmp) / 'version.json'
            state_file.write_text('unchanged')
            with patch.object(version, 'PATH', str(state_file)), \
                    patch.object(version.streamzip, 'StreamZip', return_value=Archive()), \
                    patch('autopcr.model.update.prepare_models', side_effect=RuntimeError('unsupported loader')):
                with self.assertRaisesRegex(RuntimeError, 'unsupported loader'):
                    version._update_version_sync('offline.xapk')
            self.assertEqual(state_file.read_text(), 'unchanged')
            self.assertIs(version.version_info._state, original)

    def test_concurrent_updates_run_only_once(self):
        original = version.version_info._state
        calls = []
        def update():
            import time
            time.sleep(0.03)
            calls.append(1)
            version.version_info.apply(dict(original, version='updated'))
        async def scenario():
            with patch.object(version, 'update_lck', asyncio.Lock()), \
                    patch.object(version, '_update_version_sync', side_effect=update):
                await asyncio.gather(version.update_version(), version.update_version())
        try:
            asyncio.run(scenario())
            self.assertEqual(len(calls), 1)
        finally:
            version.version_info.apply(original)


if __name__ == '__main__':
    unittest.main()
