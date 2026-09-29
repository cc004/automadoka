"""Codec checks, optional C# parity, and opt-in complete Python-only builds."""
import gc
import json
import os
import struct
import subprocess
import tempfile
import unittest
import weakref
from pathlib import Path
from typing import get_args, get_origin
from unittest.mock import patch

from autopcr.model import registry
from autopcr.model.il2cpp.decoder import DecodeError, Decoder, decompress
from autopcr.model.il2cpp.metadata import Metadata, MetadataError, cached, compressed_int, compressed_uint
from autopcr.model.il2cpp.protocol import render_models


class PythonCodecTests(unittest.TestCase):
    def test_compressed_integer_boundaries(self):
        cases = [(b'\x7f', 127), (b'\x80\x80', 128), (b'\xbf\xff', 0x3fff),
                 (b'\xc0\x00\x40\x00', 0x4000), (b'\xdf\xff\xff\xff', 0x1fffffff),
                 (b'\xf0\x78\x56\x34\x12', 0x12345678), (b'\xfe', 0xfffffffe), (b'\xff', 0xffffffff)]
        for data, expected in cases:
            self.assertEqual(compressed_uint(data, 0), (expected, len(data)))
        for data, expected in [(b'\x00', 0), (b'\x01', -1), (b'\x03', -2), (b'\xff', -0x80000000)]:
            self.assertEqual(compressed_int(data, 0)[0], expected)
        for data in (b'', b'\x80', b'\xc0\x00', b'\xf0\x00', b'\xe1'):
            with self.assertRaises(MetadataError): compressed_uint(data, 0)

    def test_literal_repeat_and_back_reference(self):
        table = [(0x8041, 8)] * 256
        for index, symbol in enumerate((0x41, 0x42, 0x102, 0x202, 0x302)):
            table[index] = (0x8000 | symbol, 8)
        self.assertEqual(decompress(bytes([0, 1, 2, 3, 2, 4]), 8, table), b'ABABABAB')
        self.assertEqual(decompress(b'raw', 3, table), b'raw')
        with self.assertRaises(DecodeError): decompress(bytes([2, 4]), 8, table)
        with self.assertRaises(DecodeError): decompress(bytes([0, 2, 3]), 2, table)
        with self.assertRaises(DecodeError): decompress(b'\0', 2, table)

    def test_prefix_tree_branch(self):
        # All first-eight-bit lookups branch on bit nine, selecting A or B.
        table = [(256, 8)] * 256 + [(0x8041, 0), (0x8042, 0)]
        stream = (0x100 << 9).to_bytes(3, 'little')
        self.assertEqual(decompress(stream, 2, table), b'AB')
        with self.assertRaises(DecodeError): decompress(stream[:2], 3, table)

    def test_bad_metadata_and_unknown_decoder_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'metadata.dat'
            for data in (b'bad', struct.pack('<II', 0xfab11baf, 99) + b'\0' * 300):
                path.write_bytes(data)
                with self.assertRaises(MetadataError): Metadata(path)
        with self.assertRaises(DecodeError): Decoder().configure(b'\0' * 512, b'\0' * 12, 10)
        decoder = Decoder()
        decoder.seed = 1
        with self.assertRaises(DecodeError): decoder.decode(b'\0' * 12, 10)

    def test_reader_cache_does_not_retain_owner(self):
        class Reader:
            @cached
            def string(self, value): return str(value)
        reader = Reader()
        reader.string(1)
        ref = weakref.ref(reader)
        del reader
        gc.collect()
        self.assertIsNone(ref())

    def test_generated_aliases_nested_enum_and_master_response(self):
        schema = {'enums': {'Mode': {'Idle': 0, 'None_': -1}},
                  'common': {'Node': {'children': 'List[Node]', 'mode': 'Mode', 'json': 'str', 'from': 'int'}},
                  'apis': [{'url': '/api/test', 'request': 'TestRequest', 'response': 'TestResponse',
                            'request_fields': {'type': 'int'}, 'response_fields': {'node': 'Node'}},
                           {'url': '/api/master', 'request': 'MasterRequest', 'response': 'MasterResponse',
                            'request_fields': {}, 'response_fields': {'mstList': 'List[Node]'}}]}
        with tempfile.TemporaryDirectory() as tmp:
            counts = render_models(schema, tmp)
            self.assertEqual(counts, {'enums': 1, 'common': 1, 'responses': 1, 'requests': 2})
            gen = registry.load_generation(tmp, 'test')
            try:
                node = gen.classes['common']['Node'].parse_obj({'json': 'v', 'from': 5, 'mode': -1, 'children': [{}]})
                self.assertEqual(node.json_, 'v')
                self.assertEqual(node.dict(by_alias=True)['from'], 5)
                self.assertEqual(node.mode.name, 'None_')
                self.assertIs(type(node.children[0]), type(node))
                response = gen.classes['requests']['MasterRequest'].__response_type__.parse_obj({'mstList': [{}]})
                self.assertIs(type(response.mstList[0]), type(node))
            finally:
                registry._unload(gen.package)
            schema['common']['Node']['json_'] = 'str'
            with self.assertRaises(MetadataError): render_models(schema, tmp)


def model_directory(root, version):
    root = Path(root)
    candidates = sorted(root.glob(version + '*/models'))
    return candidates[-1] if candidates else root / version


def type_signature(value):
    origin = get_origin(value)
    return (getattr(origin or value, '__name__', str(origin or value)),
            tuple(type_signature(arg) for arg in get_args(value)))


@unittest.skipUnless(os.getenv('AUTOPCR_PROTOCOL_TEST_RUNS') and os.getenv('AUTOPCR_PROTOCOL_BASELINE'),
                     'Set AUTOPCR_PROTOCOL_TEST_RUNS and AUTOPCR_PROTOCOL_BASELINE for C# comparison')
class PythonGeneratorParityTests(unittest.TestCase):
    def test_every_class_field_enum_url_and_response_matches_csharp(self):
        for version in ('3.16.1', '3.19.1'):
            old = registry.load_generation(model_directory(os.environ['AUTOPCR_PROTOCOL_BASELINE'], version), version)
            new = registry.load_generation(model_directory(os.environ['AUTOPCR_PROTOCOL_TEST_RUNS'], version), version)
            try:
                for kind in registry.KINDS:
                    self.assertEqual(set(old.classes[kind]), set(new.classes[kind]), (version, kind))
                    for name, before in old.classes[kind].items():
                        after = new.classes[kind][name]
                        with self.subTest(version=version, kind=kind, name=name):
                            if kind == 'enums':
                                self.assertEqual({n: v.value for n, v in before.__members__.items()},
                                                 {n: v.value for n, v in after.__members__.items()})
                                continue
                            def fields(cls):
                                return {n: (f.alias, type_signature(f.outer_type_), f.required, f.allow_none, f.default)
                                        for n, f in cls.__fields__.items()}
                            self.assertEqual(fields(before), fields(after))
                            if kind == 'requests':
                                self.assertEqual(before().url, after().url)
                                self.assertEqual(before.__response_type__.__name__, after.__response_type__.__name__)
                                self.assertEqual(fields(before.__response_type__), fields(after.__response_type__))
            finally:
                registry._unload(old.package)
                registry._unload(new.package)


@unittest.skipUnless(os.getenv('AUTOPCR_PROTOCOL_TEST_APKS'), 'Set AUTOPCR_PROTOCOL_TEST_APKS for full recovery')
class PythonApkTests(unittest.TestCase):
    def test_both_apks_without_external_commands(self):
        from autopcr.core import version
        from autopcr.model import update
        from autopcr.model.requests import LoginApiLoginRequest
        old_generation, old_state = registry.current(), version.version_info._state
        expected = {
            '3.16.1': ('48e9c105e9cceb83544d407684f98f2c4ec72240845c7b278fa230cc2084a247', 511),
            '3.19.1': ('7f9df828d11c86f7e94ecbd0a4f3ae4e8d95da6118d8bcec35b36ea0d1411145', 523),
        }
        try:
            with tempfile.TemporaryDirectory(prefix='protocol-python-') as tmp, \
                    patch.object(update, 'CACHE_DIR', tmp), \
                    patch.object(version, 'PATH', str(Path(tmp) / 'version.json')), \
                    patch.object(subprocess, 'Popen', side_effect=AssertionError('External process forbidden')), \
                    patch.object(os, 'system', side_effect=AssertionError('External command forbidden')):
                version.version_info.apply({'version': 'test', 'sign': '', 'libcount': 0})
                for number, (digest, count) in expected.items():
                    apk = Path(os.environ['AUTOPCR_PROTOCOL_TEST_APKS']) / ('Madoka+Magica+Magia+Exedra_' + number + '_APKPure.xapk')
                    generation, state = version._update_version_sync(apk)
                    run = generation.directory.parent
                    self.assertEqual(update.file_hash(run / 'extracted/il2cpp/libil2cpp.restored.so'), digest)
                    self.assertEqual(len(generation.classes['requests']), count)
                    self.assertIs(type(LoginApiLoginRequest()), generation.classes['requests']['LoginApiLoginRequest'])
                    self.assertEqual(json.loads((Path(tmp) / 'version.json').read_text()), state)
                    with patch.object(update, '_generate', side_effect=AssertionError('Cache should be reused')):
                        cached_generation, cached_state = version._update_version_sync(apk, activate=False)
                    self.assertEqual(cached_state, state)
                    registry._unload(cached_generation.package)
        finally:
            registry.activate(old_generation)
            version.version_info.apply(old_state)
