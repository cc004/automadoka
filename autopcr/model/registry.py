"""Stable public classes, immutable protocol generations, atomic activation."""
import hashlib
import importlib.util
import json
import sys
import threading
import types
import uuid
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

from pydantic import BaseModel
from . import modelbase
from ..constants import CACHE_DIR
from ..util.type_utils import find_type_base

KINDS = ('enums', 'common', 'responses', 'requests')
lock = threading.RLock()
_active = None
_proxies = {}
_facades = {}
_handlers = {}


class ProtocolError(RuntimeError):
    pass


@dataclass(frozen=True)
class Generation:
    version: str
    directory: Path
    classes: object
    package: str
    fingerprint: str


def fingerprint(directory):
    digest = hashlib.sha256()
    for kind in KINDS:
        digest.update(kind.encode())
        digest.update((Path(directory) / (kind + '.py')).read_bytes())
    return digest.hexdigest()


def _unload(package):
    for name in list(sys.modules):
        if name == package or name.startswith(package + '.'):
            sys.modules.pop(name, None)


def load_generation(directory, version, expected_hash=None):
    """Build in isolation; failure never changes public classes or active state."""
    directory = Path(directory).resolve()
    digest = fingerprint(directory)
    if expected_hash and digest != expected_hash:
        raise ProtocolError('Protocol model checksum mismatch: ' + str(directory))
    package = __package__ + '._generation_' + uuid.uuid4().hex
    module = types.ModuleType(package)
    module.__path__ = [str(directory)]
    sys.modules[package] = module
    sys.modules[package + '.modelbase'] = modelbase
    classes = {}
    try:
        for kind in KINDS:
            name = package + '.' + kind
            spec = importlib.util.spec_from_file_location(name, directory / (kind + '.py'))
            child = importlib.util.module_from_spec(spec)
            sys.modules[name] = child
            spec.loader.exec_module(child)
            own = {key: value for key, value in vars(child).items()
                   if isinstance(value, type) and value.__module__ == name}
            classes[kind] = MappingProxyType(own)
            # Resolve postponed/recursive annotations only against this generation.
            for key, cls in own.items():
                if issubclass(cls, BaseModel):
                    cls.update_forward_refs(**{k: v for k, v in vars(child).items() if k != 'cls'})
                cls.__protocol_kind__ = kind
                cls.__protocol_name__ = key
                cls.__protocol_generation__ = package
        if not classes['requests'] or not classes['responses']:
            raise ProtocolError('Protocol contains no requests or responses')
        urls = set()
        for cls in classes['requests'].values():
            if not issubclass(cls, modelbase.RequestBase):
                raise ProtocolError('Not a RequestBase: ' + cls.__name__)
            response = find_type_base(cls, modelbase.RequestBase)
            if not isinstance(response, type) or not issubclass(response, modelbase.ResponseBase):
                raise ProtocolError('Unresolved response type: ' + cls.__name__)
            cls.__response_type__ = response
            url = cls.construct().url
            if not url.startswith('/api/') or url in urls:
                raise ProtocolError('Invalid or duplicate API URL: ' + url)
            urls.add(url)
        return Generation(str(version), directory, MappingProxyType(classes), package, digest)
    except BaseException:
        _unload(package)
        raise


def current():
    global _active
    with lock:
        if _active is None:
            state_path = Path(CACHE_DIR) / 'version.json'
            state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
            saved = state.get('models')
            if saved:
                directory = Path(CACHE_DIR) / saved['directory']
                _active = load_generation(directory, state['version'], saved['sha256'])
            else:
                _active = load_generation(Path(__file__).parent / '_bundled', 'bundled')
        return _active


def resolve(kind, name):
    generation = current()
    try:
        return generation.classes[kind][name]
    except KeyError:
        raise ProtocolError('%s.%s is unavailable in protocol %s' % (kind, name, generation.version)) from None


class _ProxyType(type):
    def __call__(cls, *args, **kwargs):
        return resolve(cls._kind, cls._name)(*args, **kwargs)

    def __getattr__(cls, name):
        target = getattr(resolve(cls._kind, cls._name), name)
        # Bound classmethods may themselves be saved before a version switch.
        if isinstance(target, types.MethodType):
            def dispatch(*args, **kwargs):
                return getattr(resolve(cls._kind, cls._name), name)(*args, **kwargs)
            return dispatch
        return target

    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (getattr(subclass, '__protocol_kind__', None) == cls._kind and
                getattr(subclass, '__protocol_name__', None) == cls._name)

    def __iter__(cls):
        return iter(resolve(cls._kind, cls._name))

    def __getitem__(cls, key):
        return resolve(cls._kind, cls._name)[key]


def proxy(kind, name):
    with lock:
        key = kind, name
        if key not in _proxies:
            def validate(cls, value):
                target = resolve(cls._kind, cls._name)
                return target.validate(value) if issubclass(target, BaseModel) else target(value)
            def validators(cls):
                # Pydantic saves these validators when an enclosing model is defined.
                yield cls.validate
            _proxies[key] = _ProxyType(name, (), {
                '_kind': kind, '_name': name, '__module__': __package__ + '.' + kind,
                '__doc__': 'Stable proxy for the active ' + kind + '.' + name,
                'validate': classmethod(validate), '__get_validators__': classmethod(validators),
            })
        return _proxies[key]


def _exports(kind, generation):
    # Preserve the old generated modules' transitive star imports.
    kinds = KINDS[:KINDS.index(kind) + 1]
    return {name: proxy(group, name) for group in kinds for name in generation.classes[group]}


def install_facade(namespace, kind):
    with lock:
        generation = current()
        namespace.update(_exports(kind, generation))
        namespace['__all__'] = list(_exports(kind, generation))
        def lookup(name):
            for group in reversed(KINDS[:KINDS.index(kind) + 1]):
                if name in current().classes[group]:
                    return proxy(group, name)
            raise AttributeError(name)
        namespace['__getattr__'] = lookup
        _facades[kind] = namespace


def register_handler(name, function):
    with lock:
        resolve('responses', name).update = function
        _handlers[name] = function


def check_activation(generation):
    for name in _handlers:
        if name not in generation.classes['responses']:
            raise ProtocolError('A response handler target was removed: ' + name)


def activate(generation, commit=None):
    """Publish only after persistence succeeds. Callers serialize update jobs."""
    global _active
    with lock:
        check_activation(generation)
        for name, function in _handlers.items():
            generation.classes['responses'][name].update = function
        if commit is not None:
            commit()
        previous = _active
        _active = generation
        for kind, namespace in _facades.items():
            exports = _exports(kind, generation)
            namespace.update(exports)
            namespace['__all__'] = list(exports)
        if previous and previous.package != generation.package:
            _unload(previous.package)


def bind_request(request):
    """Refresh queued requests; pin schema and signing info for this send."""
    from ..core.version import version_info
    with lock:
        kind = getattr(type(request), '__protocol_kind__', None)
        if kind == 'requests':
            target = resolve(kind, type(request).__protocol_name__)
            if type(request) is not target:
                request = target(**request.dict(by_alias=True, exclude_unset=True))
        request._protocol_sm = version_info.sm
        request._protocol_version = version_info.version
        if 'appVersion' in request.__fields__:
            request.appVersion = version_info.version
        return request
