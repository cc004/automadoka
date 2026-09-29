"""Stable names backed by the active protocol generation."""
from .registry import install_facade as _install_facade
_install_facade(globals(), "enums")

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ._bundled.enums import *
