"""Read the ARM64 IL2CPP metadata needed by the protocol generator.

Layouts and compressed constants follow Il2CppDumper's MIT-licensed definitions.
This reader deliberately rejects unrecognized metadata/layouts.
"""
import io
import struct
from collections import namedtuple
from functools import wraps
from pathlib import Path

from elftools.elf.elffile import ELFFile


class MetadataError(ValueError):
    pass


def cached(method):
    """Instance-owned caches must not retain entire APKs after an update."""
    attribute = '_' + method.__name__ + '_cache'
    @wraps(method)
    def get(self, key):
        cache = self.__dict__.setdefault(attribute, {})
        if key not in cache:
            cache[key] = method(self, key)
        return cache[key]
    return get


HEADERS = '''stringLiteral stringLiteralData string events properties methods parameterDefaultValues
fieldDefaultValues fieldAndParameterDefaultValueData fieldMarshaledSizes parameters fields
genericParameters genericParameterConstraints genericContainers nestedTypes interfaces vtableMethods
interfaceOffsets typeDefinitions images assemblies fieldRefs referencedAssemblies attributeData
attributeDataRange unresolvedVirtualCallParameterTypes unresolvedVirtualCallParameterRanges
windowsRuntimeTypeNames windowsRuntimeStrings exportedTypeDefinitions'''.split()

TypeDefinition = namedtuple('TypeDefinition', '''name namespace byval declaring parent element generic flags
field_start method_start event_start property_start nested_start interfaces_start vtable_start interface_offsets_start
method_count property_count field_count event_count nested_count vtable_count interfaces_count interface_offsets_count
bitfield token''')
Field = namedtuple('Field', 'name type token')
Property = namedtuple('Property', 'name get set attrs token')
Method = namedtuple('Method', 'name declaring return_type return_token parameter_start generic token flags iflags slot parameter_count')
NativeType = namedtuple('NativeType', 'data kind attrs')
TypeRef = namedtuple('TypeRef', 'name arguments definition', defaults=((), None))


def compressed_uint(data, offset):
    if not 0 <= offset < len(data):
        raise MetadataError('Truncated compressed integer')
    first = data[offset]
    offset += 1
    if first < 0x80:
        return first, offset
    if first < 0xc0:
        if offset >= len(data): raise MetadataError('Truncated compressed integer')
        return ((first & 0x7f) << 8) | data[offset], offset + 1
    if first < 0xe0:
        if offset + 3 > len(data): raise MetadataError('Truncated compressed integer')
        return ((first & 0x3f) << 24) | int.from_bytes(data[offset:offset + 3], 'big'), offset + 3
    if first == 0xf0:
        if offset + 4 > len(data): raise MetadataError('Truncated compressed integer')
        return struct.unpack_from('<I', data, offset)[0], offset + 4
    if first in (0xfe, 0xff):
        return 0xfffffffe + first - 0xfe, offset
    raise MetadataError('Invalid compressed integer prefix')


def compressed_int(data, offset):
    value, offset = compressed_uint(data, offset)
    if value == 0xffffffff: return -0x80000000, offset
    return (-(value >> 1) - 1 if value & 1 else value >> 1), offset


class Metadata:
    def __init__(self, path):
        self.data = Path(path).read_bytes()
        if len(self.data) < 8 + len(HEADERS) * 8:
            raise MetadataError('Truncated metadata header')
        magic, self.version = struct.unpack_from('<II', self.data)
        if magic != 0xfab11baf or self.version not in (29, 31):
            raise MetadataError('Supported metadata versions: 29 and 31; got %s' % self.version)
        self.sections = {}
        for i, name in enumerate(HEADERS):
            offset, size = struct.unpack_from('<II', self.data, 8 + i * 8)
            if offset + size > len(self.data): raise MetadataError('Invalid metadata section: ' + name)
            self.sections[name] = offset, size
        self.types = self.table('typeDefinitions', '<16i8H2I', TypeDefinition)
        self.fields = self.table('fields', '<3i', Field)
        self.properties = self.table('properties', '<5i', Property)
        self.methods = self.table('methods', '<7i4H' if self.version == 31 else '<6i4H',
                                  lambda *x: Method(*x) if self.version == 31 else Method(*x[:3], 0, *x[3:]))
        self.images = self.table('images', '<10i')
        self.nested = [x[0] for x in self.table('nestedTypes', '<i')]
        self.defaults = {field: (kind, data) for field, kind, data in self.table('fieldDefaultValues', '<3i')}

    def table(self, name, fmt, record=None):
        offset, size = self.sections[name]
        parser = struct.Struct(fmt)
        if size % parser.size: raise MetadataError('Invalid record size in ' + name)
        rows = parser.iter_unpack(self.data[offset:offset + size])
        return [record(*row) if record else row for row in rows]

    @cached
    def string(self, index):
        offset, size = self.sections['string']
        if not 0 <= index < size: raise MetadataError('String index outside metadata')
        end = self.data.find(b'\0', offset + index, offset + size)
        if end < 0: raise MetadataError('Unterminated metadata string')
        return self.data[offset + index:end].decode('utf-8')

    @cached
    def full_name(self, index):
        definition = self.types[index]
        name = self.string(definition.name)
        # declaring is a native type index, resolved after the ELF type table is bound.
        namespace = self.string(definition.namespace)
        return namespace + '.' + name if namespace else name


class Il2Cpp:
    def __init__(self, library, metadata):
        self.metadata = Metadata(metadata)
        self.data = Path(library).read_bytes()
        elf = ELFFile(io.BytesIO(self.data))
        if elf['e_machine'] != 'EM_AARCH64' or not elf.little_endian:
            raise MetadataError('Only little-endian ARM64 ELF is supported')
        self.loads = [(s['p_vaddr'], s['p_offset'], s['p_filesz']) for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD']
        self.registration, self.type_pointers = self._find_registration()
        self.names = {}
        self._resolving = set()
        self.by_name = {self.full_name(i): i for i in range(len(self.metadata.types))}

    def offset(self, address, size=1):
        for va, offset, length in self.loads:
            if va <= address and address + size <= va + length:
                return offset + address - va
        raise MetadataError('Unmapped ELF address: 0x%x' % address)

    def read(self, address, fmt):
        return struct.unpack_from(fmt, self.data, self.offset(address, struct.calcsize(fmt)))

    def _find_registration(self):
        count = len(self.metadata.types)
        needle = struct.pack('<Q', count)
        candidates = []
        for va, offset, size in self.loads:
            cursor = offset
            while True:
                cursor = self.data.find(needle, cursor, offset + size)
                if cursor < 0: break
                found = cursor
                cursor += 1
                if found % 8 or found < offset + 80: continue
                if self.data[found + 16:found + 24] != needle: continue
                address = va + found - offset - 80
                try:
                    registration = self.read(address, '<16Q')
                    type_count, types = registration[6:8]
                    if not count <= type_count <= 10000000: continue
                    table = self.read(types, '<%dQ' % type_count)
                    # Check every type definition, not just a likely count pattern.
                    for index, definition in enumerate(self.metadata.types):
                        point, bits = self.read(table[definition.byval], '<QI')
                        if point != index or (bits >> 16) & 255 not in (*range(1, 15), 17, 18, 22, 24, 25, 28):
                            raise MetadataError('Type definition cross-check failed')
                    candidates.append((address, table))
                except (MetadataError, IndexError, struct.error):
                    continue
        if len(candidates) != 1:
            raise MetadataError('Expected one metadata registration, found %d' % len(candidates))
        return candidates[0]

    @cached
    def native(self, pointer):
        data, bits = self.read(pointer, '<QI')
        return NativeType(data, (bits >> 16) & 255, bits & 0xffff)

    def native_index(self, index):
        if not 0 <= index < len(self.type_pointers): raise MetadataError('Native type index out of range')
        return self.native(self.type_pointers[index])

    def full_name(self, index):
        if index in self.names: return self.names[index]
        if index in self._resolving: raise MetadataError('Cyclic declaring type')
        self._resolving.add(index)
        definition = self.metadata.types[index]
        if definition.declaring >= 0:
            parent = self.native_index(definition.declaring).data
            result = self.full_name(parent) + '/' + self.metadata.string(definition.name)
        else:
            result = self.metadata.full_name(index)
        self._resolving.remove(index)
        self.names[index] = result
        return result

    @cached
    def type_ref(self, pointer):
        native = self.native(pointer)
        primitives = {1: 'void', 2: 'bool', 3: 'str', 4: 'int', 5: 'int', 6: 'int', 7: 'int',
                      8: 'int', 9: 'int', 10: 'int', 11: 'int', 12: 'float', 13: 'float', 14: 'str', 28: 'Any'}
        if native.kind in primitives: return TypeRef(primitives[native.kind])
        if native.kind in (0x11, 0x12):
            return TypeRef(self.full_name(native.data), (), native.data)
        if native.kind in (0x14, 0x1d):
            element = self.read(native.data, '<Q')[0] if native.kind == 0x14 else native.data
            return TypeRef('List', (self.type_ref(element),))
        if native.kind == 0x15:
            type_pointer, instance = self.read(native.data, '<2Q')
            argc, argv = self.read(instance, '<2Q')
            if not 0 < argc <= 64: raise MetadataError('Invalid generic argument count')
            definition = self.type_ref(type_pointer)
            arguments = tuple(self.type_ref(p) for p in self.read(argv, '<%dQ' % argc))
            return TypeRef(definition.name, arguments, definition.definition)
        raise MetadataError('Unsupported protocol native type: 0x%x' % native.kind)

    def reference(self, index):
        if not 0 <= index < len(self.type_pointers): raise MetadataError('Native type index out of range')
        return self.type_ref(self.type_pointers[index])

    def constant(self, field_index):
        type_index, data_index = self.metadata.defaults[field_index]
        if data_index < 0: return None
        section, size = self.metadata.sections['fieldAndParameterDefaultValueData']
        if not 0 <= data_index < size: raise MetadataError('Constant offset outside metadata')
        data = memoryview(self.metadata.data)[section:section + size]
        kind = self.native_index(type_index).kind
        if kind in (8, 9):
            return (compressed_int if kind == 8 else compressed_uint)(data, data_index)[0]
        if kind == 14:
            length, start = compressed_int(data, data_index)
            if length == -1: return None
            if length < 0 or start + length > len(data): raise MetadataError('Invalid constant string length')
            return bytes(data[start:start + length]).decode('utf-8')
        formats = {2: '?', 3: 'H', 4: 'b', 5: 'B', 6: 'h', 7: 'H', 10: 'q', 11: 'Q', 12: 'f', 13: 'd'}
        if kind not in formats: raise MetadataError('Unsupported constant type: %x' % kind)
        return struct.unpack_from('<' + formats[kind], data, data_index)[0]
