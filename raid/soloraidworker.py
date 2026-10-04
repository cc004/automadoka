"""总力战（Solo Raid）执行器。

职责：
1. 从主数据里读取**当前开放赛季**的 boss 数据（赛季每月月初更换，主数据由服务端下发，
   因此这里天然会"自动更新"）。
2. 读取指定难度对应的关卡、boss 血量/弱点/回合上限。
3. 执行 ``initialize_stage -> get_solo_raid_info -> finalize_stage_for_user`` 完整流程，
   战斗日志由 :mod:`autopcr.util.soloraid_battlelog` 推理生成。
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from autopcr.core.pcrclient import pcrclient
from autopcr.core.apiclient import ApiException
from autopcr.db.database import db
from autopcr.model.models import *
from autopcr.util.soloraid_battlelog import (
    BattleUnit,
    build_solo_raid_battle_log,
    KILL_TIMINGS,
    BATTLE_LOG_MODES,
    MODE_SIMULATE,
    TIMING_MIDDLE,
)

# 难度下标 -> 名称（soloRaidStageMstId = 赛季ID * 100 + 难度）
DIFFICULTY_NAMES: Dict[int, str] = {
    1: "easy",
    2: "normal",
    3: "hard",
    4: "very hard",
    5: "extra",
    6: "crisis",
}
DIFFICULTY_ORDER: List[int] = [1, 2, 3, 4, 5, 6]

# 结算方式：提交自制战斗日志 / 让服务端自己跳过战斗
SETTLE_BATTLE_LOG = "battlelog"
SETTLE_SKIP = "skip"

# 总力战依赖的协议类。游戏大版本更新时 autopcr 会整体重新生成协议模型
# （见 autopcr/model/registry.py），若某个类被改名或移除，这里能第一时间给出
# 可读提示，而不是抛一个难以理解的 ProtocolError。
_REQUIRED_PROTOCOL = (
    ("requests", "SoloRaidApiInitializeStageRequest"),
    ("requests", "SoloRaidApiGetSoloRaidInfoRequest"),
    ("requests", "SoloRaidApiFinalizeStageForUserRequest"),
    ("requests", "SoloRaidApiGetTopRequest"),
    ("requests", "SoloRaidApiSkipQuestBattleRequest"),
    ("requests", "MstApiGetSoloRaidMstListRequest"),
    ("requests", "MstApiGetSoloRaidStageMstListRequest"),
    ("requests", "MstApiGetQuestEnemyAppearanceMstListRequest"),
    ("requests", "MstApiGetQuestEnemySkillSetMstListRequest"),
    ("common", "SoloRaidBattleInfo"),
    ("enums", "SoloRaidChallengeType"),
    ("enums", "StyleRentalUsingStatus"),
    ("enums", "SoloRaidRoomResult"),
)


def protocol_version() -> str:
    """当前生效的协议版本号（bundled 表示还在用仓库内置的那一份）。"""
    from autopcr.model import registry

    try:
        return registry.current().version
    except Exception:
        return "unknown"


def check_protocol_compatibility() -> List[str]:
    """检查当前生效的协议代里是否还包含总力战需要的类。

    返回缺失项的 ``"kind.name"`` 列表，空列表表示全部可用。
    用于在游戏更新导致协议改名/移除时给出明确提示。
    """
    from autopcr.model import registry

    missing: List[str] = []
    for kind, name in _REQUIRED_PROTOCOL:
        try:
            registry.resolve(kind, name)
        except Exception:
            missing.append(f"{kind}.{name}")
    return missing


def _parse_time(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


@dataclass
class SoloRaidBossInfo:
    """一个难度下的 boss 数据（全部来自主数据，随赛季自动更新）。"""

    difficulty: int
    difficulty_name: str
    solo_raid_mst_id: int
    stage_mst_id: int
    quest_stage_mst_id: int
    limit_round: int
    comment: str = ""
    boss_max_hp: int = 0
    enemy_count: int = 0
    wave_count: int = 1
    weak_elements: List[int] = field(default_factory=list)
    enemies: List[Any] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.difficulty_name}(难度{self.difficulty})"

    def describe(self) -> str:
        hp = f"{self.boss_max_hp:,}" if self.boss_max_hp else "未知"
        weak = ",".join(str(e) for e in self.weak_elements) or "无"
        return (
            f"{self.label} 关卡{self.stage_mst_id} "
            f"boss血量 {hp} 部位数 {self.enemy_count} 弱点元素 [{weak}] "
            f"回合上限 {self.limit_round}"
        )


@dataclass
class SoloRaidSeason:
    solo_raid_mst_id: int
    start_time: str
    battle_end_time: str
    end_time: str

    def describe(self) -> str:
        return (
            f"赛季 {self.solo_raid_mst_id} "
            f"{self.start_time} ~ {self.battle_end_time}"
        )


# ---------------------------------------------------------------------------
# 主数据读取（每月自动更新）
# ---------------------------------------------------------------------------
async def get_open_season() -> Optional[SoloRaidSeason]:
    """返回当前正在开放的总力战赛季，没有则返回 None。"""
    now = datetime.now(timezone.utc)
    for mst in await db.mst(MstApiGetSoloRaidMstListRequest()):
        start = _parse_time(mst.startTime)
        battle_end = _parse_time(mst.battleEndTime)
        if start is None or battle_end is None:
            continue
        if start <= now <= battle_end:
            return SoloRaidSeason(
                solo_raid_mst_id=mst.soloRaidMstId,
                start_time=mst.startTime,
                battle_end_time=mst.battleEndTime,
                end_time=mst.endTime,
            )
    return None


async def get_season_stages(season: SoloRaidSeason) -> List[Any]:
    stages = [
        s
        for s in await db.mst(MstApiGetSoloRaidStageMstListRequest())
        if s.soloRaidMstId == season.solo_raid_mst_id
    ]
    return sorted(stages, key=lambda s: s.difficulty or 0)


async def get_enemy_appearances(quest_stage_mst_id: int) -> List[Any]:
    return [
        e
        for e in await db.mst(MstApiGetQuestEnemyAppearanceMstListRequest())
        if e.questStageMstId == quest_stage_mst_id
    ]


async def _enemy_skill_ids(enemy_skill_set_id: Optional[int]) -> List[int]:
    if not enemy_skill_set_id:
        return []
    return [
        s.skillMstId
        for s in await db.mst(MstApiGetQuestEnemySkillSetMstListRequest())
        if s.enemySkillSetId == enemy_skill_set_id
    ]


async def get_boss_info(difficulty: int) -> Optional[SoloRaidBossInfo]:
    """读取指定难度的 boss 数据。"""
    season = await get_open_season()
    if season is None:
        return None
    stage = next(
        (
            s
            for s in await get_season_stages(season)
            if s.difficulty == difficulty
        ),
        None,
    )
    if stage is None:
        return None

    enemies = await get_enemy_appearances(stage.questStageMstId)
    weak: List[int] = []
    for rec in enemies:
        for key in ("weakElement1", "weakElement2", "weakElement3",
                    "weakElement4", "weakElement5", "weakElement6"):
            value = getattr(rec, key, None)
            if value and value not in weak:
                weak.append(value)

    return SoloRaidBossInfo(
        difficulty=difficulty,
        difficulty_name=DIFFICULTY_NAMES.get(difficulty, str(difficulty)),
        solo_raid_mst_id=season.solo_raid_mst_id,
        stage_mst_id=stage.soloRaidStageMstId,
        quest_stage_mst_id=stage.questStageMstId,
        limit_round=stage.limitRoundCount or 1,
        comment=stage.comment or "",
        boss_max_hp=max((e.hp or 0) for e in enemies) if enemies else 0,
        enemy_count=len(enemies),
        wave_count=max((e.wave or 1) for e in enemies) if enemies else 1,
        weak_elements=weak,
        enemies=enemies,
    )


async def list_all_boss_info() -> List[SoloRaidBossInfo]:
    """列出当前赛季所有难度的 boss 数据（用于展示）。"""
    result: List[SoloRaidBossInfo] = []
    for difficulty in DIFFICULTY_ORDER:
        info = await get_boss_info(difficulty)
        if info is not None:
            result.append(info)
    return result


# ---------------------------------------------------------------------------
# 战斗单位构造
# ---------------------------------------------------------------------------
def _safe_int(value: Any, default: int = 0) -> int:
    """主数据里 `def` 字段名带下划线（`_def`），pydantic 会把它当私有属性丢掉，
    这里统一做一次容错，取不到就返回默认值。"""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return int(value)


def _style_param(style_mst_id: int) -> Dict[str, int]:
    for style in db.style_list:
        if style.styleMstId == style_mst_id:
            return {
                "element": style.element or 0,
                "role": style.role or 0,
            }
    return {"element": 0, "role": 0}


def ally_to_battle_unit(unit: Any, index: int) -> BattleUnit:
    style = _style_param(unit.styleMstId)
    passive = [
        {
            "passiveSkillMstId": p.passiveSkillMstId,
            "level": p.level or 1,
            "abilitySourceType": p.abilitySourceType or 1,
        }
        for p in (unit.passiveSkillInfoList or [])
    ]
    return BattleUnit(
        unit.battleUnitDataId,
        is_ally=True,
        speed=unit.speed or 100,
        position_id=index + 1,
        max_hp=unit.maxHp or 0,
        atk=unit.atk or 0,
        defence=_safe_int(getattr(unit, "_def", 0)),
        element=style["element"],
        role=style["role"],
        critical_rate=unit.criticalRate or 0,
        critical_damage_rate=unit.criticalDamageRate or 0,
        normal_attack_mst_id=unit.normalAttackInfo.skillMstId if unit.normalAttackInfo else 0,
        active_skill_mst_ids=[a.skillMstId for a in (unit.attackInfoList or [])],
        special_attack_mst_id=unit.specialAttackInfo.skillMstId if unit.specialAttackInfo else 0,
        mst_id=unit.battleUnitMstId or 0,
        style_mst_id=unit.styleMstId or 0,
        passive_skill_infos=passive,
    )


def _enemies_to_battle_units(
    boss: SoloRaidBossInfo,
    skill_map: Dict[int, List[int]],
) -> List[BattleUnit]:
    """把最终波次的敌人转成战斗单位，ID 按出场顺序分配为 -1, -2, ..."""
    final_wave = boss.wave_count
    records = [e for e in boss.enemies if (e.wave or 1) == final_wave]
    if not records:
        records = list(boss.enemies)
    units: List[BattleUnit] = []
    for offset, rec in enumerate(records):
        weak = [
            getattr(rec, key)
            for key in ("weakElement1", "weakElement2", "weakElement3",
                        "weakElement4", "weakElement5", "weakElement6")
            if getattr(rec, key, None)
        ]
        units.append(
            BattleUnit(
                -(offset + 1),
                is_ally=False,
                speed=rec.speed or 100,
                position_id=offset + 1,
                max_hp=rec.hp or boss.boss_max_hp,
                atk=rec.atk or 0,
                defence=_safe_int(getattr(rec, "_def", 0)),
                mst_id=rec.enemyMstId or 0,
                enemy_parameter_mst_id=rec.questEnemyAppearanceMstId or 0,
                weak_elements=weak,
                is_main_target=bool(rec.isMainTargetEnemy),
                active_skill_mst_ids=skill_map.get(rec.enemySkillSetId or 0, []),
            )
        )
    return units


# ---------------------------------------------------------------------------
# 战斗执行
# ---------------------------------------------------------------------------
@dataclass
class SoloRaidBattleResult:
    difficulty: int
    success: bool
    score: int = 0
    boss_rest_hp: int = 0
    boss_max_hp: int = 0
    high_score_updated: bool = False
    log: str = ""


async def resolve_party_id(client: pcrclient, party: Any) -> Optional[int]:
    """把"队伍名/ID"解析成 partyDataId。"""
    try:
        return int(party)
    except (TypeError, ValueError):
        pass
    parties = client.data.resp.partyDataList or []
    for data in parties:
        if data.name == party:
            return data.partyDataId
    return None


async def _initialize_room(
    client: pcrclient, boss: SoloRaidBossInfo, party_data_id: int
) -> Optional[int]:
    """进入指定难度的总力战房间，返回 questDataId（失败返回 None）。"""
    init = await client.request(
        SoloRaidApiInitializeStageRequest(
            soloRaidStageMstId=boss.stage_mst_id,
            partyDataId=party_data_id,
            challengeType=SoloRaidChallengeType.Normal,
            soloRaidStageDataId=0,
            styleRentalUsingStatus=StyleRentalUsingStatus.NotUsing,
        )
    )
    room = init.soloRaidRoomData
    return room.questDataId if room is not None else None


async def run_solo_raid_skip(
    client: pcrclient,
    *,
    difficulty: int,
    party_data_id: int,
    repeat_num: int = 1,
) -> SoloRaidBattleResult:
    """用服务端「跳过战斗」接口结算。

    这是游戏自带的官方机制（``sweep.py`` 里的「扫荡总力战」用的就是它）：
    不提交任何自制战斗日志，由服务端自己模拟战斗，因此**风险最低**。

    前提是**该难度已经通关过一次**，否则服务端会拒绝（返回错误）。
    """
    boss = await get_boss_info(difficulty)
    if boss is None:
        return SoloRaidBattleResult(
            difficulty=difficulty, success=False, log="当前没有开放该难度的总力战"
        )

    quest_data_id = await _initialize_room(client, boss, party_data_id)
    if quest_data_id is None:
        return SoloRaidBattleResult(
            difficulty=difficulty, success=False, log="进入总力战失败：没有返回房间数据"
        )

    await asyncio.sleep(1)

    resp = await client.request(
        SoloRaidApiSkipQuestBattleRequest(repeatNum=repeat_num)
    )
    score_info = resp.scoreInfo
    return SoloRaidBattleResult(
        difficulty=difficulty,
        success=bool(resp.result == SoloRaidRoomResult.Win),
        score=score_info.score if score_info else 0,
        boss_rest_hp=score_info.bossRestHp if score_info else 0,
        boss_max_hp=score_info.bossMaxHp if score_info else boss.boss_max_hp,
        high_score_updated=bool(resp.isHighScoreUpdated),
        log=f"跳过战斗结算 {resp.result}",
    )


async def run_solo_raid_battle(
    client: pcrclient,
    *,
    difficulty: int,
    party_data_id: int,
    kill_timing: str = TIMING_MIDDLE,
    mode: str = MODE_SIMULATE,
    seed: Optional[int] = None,
) -> SoloRaidBattleResult:
    """打一次总力战。返回战斗结果。"""
    boss = await get_boss_info(difficulty)
    if boss is None:
        return SoloRaidBattleResult(
            difficulty=difficulty, success=False, log="当前没有开放该难度的总力战"
        )

    # 1) 进入战斗
    quest_data_id = await _initialize_room(client, boss, party_data_id)
    if quest_data_id is None:
        return SoloRaidBattleResult(
            difficulty=difficulty, success=False, log="进入总力战失败：没有返回房间数据"
        )

    await asyncio.sleep(1)

    # 2) 拉取战斗信息（我方单位）
    info = await client.request(
        SoloRaidApiGetSoloRaidInfoRequest(questDataId=quest_data_id)
    )

    allies = [
        ally_to_battle_unit(unit, index)
        for index, unit in enumerate(info.allyBattleUnitList or [])
    ]

    skill_map: Dict[int, List[int]] = {}
    for rec in boss.enemies:
        key = rec.enemySkillSetId or 0
        if key and key not in skill_map:
            skill_map[key] = await _enemy_skill_ids(key)
    enemies = _enemies_to_battle_units(boss, skill_map)

    boss_max_hp = boss.boss_max_hp or max((e.max_hp for e in enemies), default=0)

    # 3) 推理战斗日志
    built = build_solo_raid_battle_log(
        allies,
        enemies,
        boss_max_hp=boss_max_hp,
        kill_timing=kill_timing,
        limit_round=boss.limit_round,
        wave=boss.wave_count,
        mode=mode,
        seed=seed,
    )

    battle_info = SoloRaidBattleInfo(**built["battleInfo"])

    await asyncio.sleep(1)

    # 4) 结算
    resp = await client.request(
        SoloRaidApiFinalizeStageForUserRequest(
            questDataId=quest_data_id,
            result=1,
            battleInfo=battle_info,
            battleLog=built["battleLog"],
            autoMode=0,
        )
    )

    score_info = resp.scoreInfo
    result = SoloRaidBattleResult(
        difficulty=difficulty,
        success=bool(resp.result == SoloRaidRoomResult.Win),
        score=score_info.score if score_info else 0,
        boss_rest_hp=score_info.bossRestHp if score_info else 0,
        boss_max_hp=score_info.bossMaxHp if score_info else boss_max_hp,
        high_score_updated=bool(resp.isHighScoreUpdated),
        log=f"结算结果 {resp.result}",
    )
    return result
