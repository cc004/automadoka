"""Exercise the Raid startup import without loading accounts or running jobs."""
import importlib.util
import io
import unittest
from pathlib import Path


class StartupImportTests(unittest.TestCase):
    def test_raidrunner_import_with_model_facades(self):
        path = Path(__file__).resolve().parents[1] / 'raid' / 'raidrunner.py'
        spec = importlib.util.spec_from_file_location('raid._startup_import_test', path)
        module = importlib.util.module_from_spec(spec)

        def open_config(filename, *args, **kwargs):
            self.assertEqual(str(filename), 'raid_config.json')
            return io.StringIO('{"monitor": [], "worker": []}')

        # Restrict the replacement to this module; dependency imports use normal IO.
        module.open = open_config
        spec.loader.exec_module(module)
        self.assertEqual(module.monitor, [])
        self.assertEqual(module.worker, {})
        self.assertTrue(callable(module.main))
