"""Generate Pydantic protocol models directly from IL2CPP type metadata."""
import json
import keyword
from pathlib import Path

from .metadata import Il2Cpp, MetadataError

PRIMITIVES = {'System.DateTime': 'int', 'System.DateTimeOffset': 'str',
              **{'CodeStage.AntiCheat.ObscuredTypes.Obscured' + k: v for k, v in
                 [('Bool', 'bool'), ('Int', 'int'), ('Long', 'int'), ('Float', 'float'),
                  ('Double', 'float'), ('String', 'str')]}}
CONTAINERS = {'System.Collections.Generic.List`1': 'List', 'System.Collections.Generic.Dictionary`2': 'Dict',
              'System.Nullable`1': 'Optional', 'List': 'List'}
# Builtins such as 'type' are valid model fields; only escape keywords/methods.
RESERVED = set(keyword.kwlist) | {'json', 'schema', 'dict', 'copy', 'validate', 'construct',
                                'parse_obj', 'parse_raw', 'parse_file', 'from_orm', 'schema_json', 'update_forward_refs'}


def common_name(name):
    return name.replace('Network.Definition.', '').replace('.', '').replace('/', '')


def api_name(name):
    return name.rsplit('.', 1)[-1].replace('/', '')


class ProtocolGenerator:
    def __init__(self, reader):
        self.reader = reader
        self.meta = reader.metadata
        self.common = {}
        self.enums = {}
        self.visiting = set()

    def field_type(self, reference):
        name = reference.name
        if name in PRIMITIVES: return PRIMITIVES[name]
        if reference.arguments:
            if name not in CONTAINERS: raise MetadataError('Unsupported protocol generic: ' + name)
            return '%s[%s]' % (CONTAINERS[name], ', '.join(self.field_type(arg) for arg in reference.arguments))
        if reference.definition is None: return name
        self.resolve(reference.definition)
        return common_name(name)

    def fields(self, index):
        if self.reader.full_name(index) == 'ReDrive.Api.AppReqBase': return {}
        definition = self.meta.types[index]
        result = {}
        for prop in self.meta.properties[definition.property_start:definition.property_start + definition.property_count]:
            if prop.get < 0 or prop.set < 0: continue
            method = self.meta.methods[definition.method_start + prop.get]
            if method.flags & 7 != 6 or method.flags & 16: continue
            result[self.meta.string(prop.name)] = self.field_type(self.reader.reference(method.return_type))
        for field in self.meta.fields[definition.field_start:definition.field_start + definition.field_count]:
            native = self.reader.native_index(field.type)
            if native.attrs & 7 != 6 or native.attrs & 16: continue
            result[self.meta.string(field.name)] = self.field_type(self.reader.reference(field.type))
        return result

    def resolve(self, index):
        if index in self.visiting: return
        self.visiting.add(index)
        definition = self.meta.types[index]
        name = self.reader.full_name(index)
        if definition.bitfield & 2:
            values = {}
            for field_index in range(definition.field_start, definition.field_start + definition.field_count):
                if field_index in self.meta.defaults:
                    field = self.meta.fields[field_index]
                    values[self.meta.string(field.name)] = self.reader.constant(field_index)
            self.enums[name] = values
        else:
            fields = self.fields(index)
            self.common[name] = fields

    def schema(self):
        apis = []
        assembly = next((image for image in self.meta.images if self.meta.string(image[0]) == 'Assembly-CSharp.dll'), None)
        if assembly is None: raise MetadataError('Assembly-CSharp image not found')
        base_request = self.reader.by_name['ReDrive.Api.AppReqBase']
        for index in range(assembly[2], assembly[2] + assembly[3]):
            definition = self.meta.types[index]
            url = None
            for field_index in range(definition.field_start, definition.field_start + definition.field_count):
                field = self.meta.fields[field_index]
                attrs = self.reader.native_index(field.type).attrs
                if self.meta.string(field.name) == 'Url' and attrs & 7 == 6 and attrs & 16:
                    if field_index not in self.meta.defaults: raise MetadataError('Nonconstant protocol URL')
                    url = self.reader.constant(field_index)
                    break
            if url is None: continue
            nested = {self.meta.string(self.meta.types[i].name): i for i in
                      self.meta.nested[definition.nested_start:definition.nested_start + definition.nested_count]}
            if 'Response' not in nested: continue
            request, response = nested.get('Request', base_request), nested['Response']
            response_name = self.reader.full_name(response)
            request_name = (response_name.replace('Response', 'Request') if request == base_request
                            else self.reader.full_name(request))
            request_fields = self.fields(request)
            response_fields = self.fields(response)
            if not isinstance(url, str) or not url.startswith('/api/'):
                raise MetadataError('Invalid protocol URL: %r' % url)
            apis.append({'url': url, 'request': api_name(request_name), 'response': api_name(response_name),
                         'request_fields': request_fields, 'response_fields': response_fields})
        if not apis: raise MetadataError('No protocol APIs found')
        def flatten(types):
            result = {}
            for name, fields in types.items():
                name = common_name(name)
                if name in result: raise MetadataError('Colliding protocol type name: ' + name)
                result[name] = fields
            return result
        return {'apis': apis, 'common': flatten(self.common), 'enums': flatten(self.enums)}


def render_models(schema, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    files = {'enums': ['from enum import IntEnum', ''],
             'common': ['from __future__ import annotations', 'from typing import List, Dict, Optional, Any',
                        'from .enums import *', 'from pydantic import BaseModel, Field', ''],
             'responses': ['from __future__ import annotations', 'from typing import List, Dict, Optional, Any',
                           'from .modelbase import ResponseBase', 'from .common import *', 'from .enums import *',
                           'from pydantic import Field', ''],
             'requests': ['from __future__ import annotations', 'from typing import List, Dict, Optional, Any',
                          'from .modelbase import RequestBase, MstRequestBase', 'from .responses import *',
                          'from .common import *', 'from .enums import *', 'from pydantic import Field', '']}
    names = {kind: set() for kind in files}

    def declare(kind, name, base, fields, url=None):
        if not name.isidentifier() or keyword.iskeyword(name) or name in names[kind]:
            raise MetadataError('Invalid or duplicate protocol class: ' + name)
        names[kind].add(name)
        lines = files[kind]
        lines.append('class %s(%s):' % (name, base))
        aliases = set()
        for field, annotation in fields.items():
            identifier = field + '_' if field in RESERVED else field
            if not identifier.isidentifier() or identifier.startswith('_') or identifier in aliases:
                raise MetadataError('Unsupported or colliding field name: ' + field)
            aliases.add(identifier)
            value = 'Field(None, alias=%r)' % field if identifier != field else 'None'
            lines.append('    %s: %s = %s' % (identifier, annotation, value))
        if url is not None:
            lines += ['    @property', '    def url(self) -> str:', '        return %r' % url]
        elif not fields:
            lines.append('    pass')
        lines.append('')

    for name, values in schema['enums'].items():
        if not name.isidentifier(): raise MetadataError('Invalid enum name: ' + name)
        names['enums'].add(name)
        files['enums'].append('class %s(IntEnum):' % name)
        for key, value in values.items():
            member = key + '_' if keyword.iskeyword(key) else key
            if not member.isidentifier() or not isinstance(value, int): raise MetadataError('Invalid enum member')
            files['enums'].append('    %s = %d' % (member, value))
        if not values: files['enums'].append('    pass')
        files['enums'].append('')
    for name, fields in schema['common'].items():
        declare('common', name, 'BaseModel', fields)
    for api in schema['apis']:
        fields = api['response_fields']
        master = fields.get('mstList') if len(fields) == 1 else None
        if master and master.startswith('List['):
            base = 'MstRequestBase[%s]' % master[5:-1]
        else:
            declare('responses', api['response'], 'ResponseBase', fields)
            base = 'RequestBase[%s]' % api['response']
        declare('requests', api['request'], base, api['request_fields'], api['url'])
    for kind, lines in files.items():
        source = '\n'.join(lines) + '\n'
        compile(source, str(output / (kind + '.py')), 'exec')
        (output / (kind + '.py')).write_bytes(source.encode('utf-8'))
    return {kind: len(items) for kind, items in names.items()}


def generate(library, metadata, output):
    reader = Il2Cpp(library, metadata)
    schema = ProtocolGenerator(reader).schema()
    counts = render_models(schema, output)
    report = {'generator': 'python-il2cpp', 'metadata_version': reader.metadata.version,
              'metadata_registration': hex(reader.registration), 'type_definitions': len(reader.metadata.types),
              'native_types': len(reader.type_pointers), 'apis': len(schema['apis']), **counts}
    output = Path(output)
    (output / 'protocol.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    (output / 'protocol.schema.json').write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding='utf-8')
    return report
