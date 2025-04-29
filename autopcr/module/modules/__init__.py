from dataclasses import field
from typing import Any
from .cron import *
from .sweep import *

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
        tower,
        heart,
        gather,
        mission,
        present
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
