"""Optional integration test against two generated real game model directories."""
import asyncio
import os
import unittest
from pathlib import Path
from types import SimpleNamespace


@unittest.skipUnless(os.getenv('AUTOPCR_PROTOCOL_TEST_RUNS'), 'Set AUTOPCR_PROTOCOL_TEST_RUNS to generated runs')
class RealModelsTests(unittest.TestCase):
    def test_live_switch_preserves_imports_handlers_and_nested_types(self):
        from autopcr.model import registry, models
        from autopcr.model.requests import LoginApiLoginRequest
        from autopcr.model.responses import UserApiGetInitDataListResponse
        from autopcr.model.modelbase import Response
        root = Path(os.environ['AUTOPCR_PROTOCOL_TEST_RUNS'])
        old = registry.current()
        results = []
        try:
            for version in ('3.16.1', '3.19.1'):
                candidates = sorted(root.glob(version + '*/models'))
                directory = candidates[-1] if candidates else root / version
                generation = registry.load_generation(directory, version)
                registry.activate(generation)
                request = LoginApiLoginRequest(appVersion=version)
                response = Response[request.__response_type__].parse_obj({'payload': {'userId': 123}})
                self.assertEqual(response.payload.userId, 123)
                initial = UserApiGetInitDataListResponse.parse_obj({'userParamData': {'userId': 123}})
                manager = SimpleNamespace()
                asyncio.run(initial.update(manager, request))
                self.assertIs(manager.resp, initial)
                self.assertIs(type(initial.userParamData), generation.classes['common']['UserUserParamDataRecord'])
                results.append((generation, request))
            first, second = results[0][0], results[1][0]
            added = set(second.classes['requests']) - set(first.classes['requests'])
            self.assertTrue(added)
            for name in added:
                self.assertIs(type(getattr(models, name)()), second.classes['requests'][name])
            self.assertIsNot(type(results[0][1]), type(results[1][1]))
            self.assertTrue(isinstance(results[0][1], LoginApiLoginRequest))
        finally:
            registry.activate(old)
