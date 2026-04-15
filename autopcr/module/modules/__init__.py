from dataclasses import field
from typing import Any
from .cron import cron1, cron2, cron3, cron4, cron5, cron6
from .sweep import arena, battle_mission, event, archive, tower, heart, gather, mission, present
from .stamina import stamina_buy, basic 
from .shop import event_shop, raid_shop, arena_shop
from .common import loginbonus, info
from .collection import eventscenario, collection
from .tool import clear_dungeon_event, secret, auto_register, super_sweep
from .wash import super_wash
from .raid import raid_reward, self_raid, support_raid, raid_support, like_raid
from .gacha import freegacha
from typing import List
from dataclasses import dataclass

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
        stamina_buy,
        super_sweep,
        raid_reward,
        self_raid,
        support_raid,
        like_raid,
        arena,
        basic,
        event,
        archive,
        event_shop,
        raid_shop,
        arena_shop,
        tower,
        heart,
        gather,
        freegacha,
        eventscenario,
        collection,
        battle_mission,
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
        super_wash,
        raid_support,
        secret,
        auto_register,
        clear_dungeon_event
    ]
)
