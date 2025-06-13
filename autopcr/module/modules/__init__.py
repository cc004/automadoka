from dataclasses import field
from typing import Any
from .cron import *
from .sweep import *
from .stamina import *
from .shop import *
from .common import *
from .collection import *

@dataclass
class ModuleList:
    name: str = ""
    key: str = ""
    modules: List[Any] = field(default_factory=list)

cron_modules = ModuleList(
    '定时',
    'cron',
    [
        cron1,
        cron2,
        cron3,
        cron4,
        cron5,
        cron6,
    ]
)

daily_modules = ModuleList(
    '日常',
    'daily',
    [
        loginbonus,
        basic,
        event,
        archive,
        shop,
        tower,
        heart,
        gather,
        eventscenario,
        collection,
        mission,
        present,
        info
    ]
)

planning_modules = ModuleList(
    '规划',
    'planning',
    [
    ]
)


unit_modules = ModuleList(
    '角色',
    'unit',
    [
    ]
)

clan_modules = ModuleList(
    '公会',
    'clan',
    [
    ]
)

danger_modules = ModuleList(
    '危险',
    'danger',
    [
    ]
)

tool_modules = ModuleList(
    '工具',
    'tool',
    [
    ]
)
