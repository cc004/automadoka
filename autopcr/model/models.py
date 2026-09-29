from .modelbase import *
from .error import *
from .enums import *
from .common import *
from .requests import *
from .responses import *
from .error import *
from .resourcemodels import *
from . import handlers

def __getattr__(name):
    # New model names are also accessible through this long-lived aggregate module.
    from . import registry
    for kind in reversed(registry.KINDS):
        if name in registry.current().classes[kind]:
            return registry.proxy(kind, name)
    raise AttributeError(name)
