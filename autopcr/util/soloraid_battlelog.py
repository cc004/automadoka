"""总力战（Solo Raid）战斗日志生成器。

游戏（Magia Exedra / PCR Re:Dive 引擎）在 ``/api/solo_raid/finalize_stage_for_user``
里接收一份完整的战斗回放：

    {"Commands": [...], "ResultBattleUnits": [...], "ResultRound": N}

其中 ``Commands`` 是逐条战斗指令，包含三种类型：

* ``CommandBeginTurn``      —— 回合/行动开始，携带行动顺序（TurnActOrderUnitInfo）
* ``CommandExecuteCommonAct`` —— 单位普通行动/异常状态结算
* ``CommandSkill``          —— 技能释放，``AffectedUnitNoticeList[].Damages[].DamageValue``
                              就是客户端上报的伤害数值

也就是说，**伤害由客户端上报**（和团战的 ``MultiRaidApiAddDamageRequest`` 同一思路），
服务端只负责结算分数与奖励。因此只要生成一份结构合法、伤害总和足以击杀 boss 的
战斗日志，就能"推理"出一场合理的击杀。

本模块不依赖任何网络/模型代码，输入纯数据，输出可直接提交的 JSON，方便离线自测。
"""

from __future__ import annotations

import json
import math
import random
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# 指令类型（与服务端序列化字符串保持一致）
# ---------------------------------------------------------------------------
CMD_BEGIN_TURN = "ReDriveBattleCore.Command.CommandBeginTurn, Assembly-CSharp"
CMD_COMMON_ACT = "ReDriveBattleCore.Command.CommandExecuteCommonAct, Assembly-CSharp"
CMD_SKILL = "ReDriveBattleCore.Command.CommandSkill, Assembly-CSharp"

STATE_DEBUFF_EFFECT = "eff_cmn_act_debuff_appear_001"
STATE_BUFF_EFFECT = "eff_cmn_act_buff_appear_001"

# 一个"回合"对应的行动时间。数值取自抓包（单回合战斗 GaugeValueToNextRound ≈ 114）。
ROUND_TIME = 115.0
# 行动槽填满所需的距离，速度越快的单位间隔越短。
ACTION_GAUGE = 1000.0
# 战斗日志里 GaugeValue 的量纲缩放（抓包中数值约 0~115）。
GAUGE_SCALE = 0.1

# 斩杀时机
TIMING_INSTANT = "instant"   # 秒杀：进本第一刀就斩掉 boss
TIMING_MIDDLE = "middle"     # 中间时间点斩杀
TIMING_LAST = "last"         # 最后关头斩杀

KILL_TIMINGS = [TIMING_INSTANT, TIMING_MIDDLE, TIMING_LAST]

# 战斗日志模式
MODE_SIMULATE = "simulate"   # 模拟一份完整战斗日志（推荐）
MODE_MINIMAL = "minimal"     # 极简日志（Commands 为空，和现有魔女功能同思路，最保守）

BATTLE_LOG_MODES = [MODE_SIMULATE, MODE_MINIMAL]

# 斩杀时间的波动幅度：斩杀点在整个战斗的我方行动序列上，围绕名义位置上下浮动这个比例。
# 不加波动的话每次都在同一个行动上收尾，日志会显得太整齐。
KILL_TIME_JITTER = 0.10


# ---------------------------------------------------------------------------
# 单位
# ---------------------------------------------------------------------------
class BattleUnit:
    """参与战斗的一个单位（我方或敌方）。"""

    def __init__(
        self,
        unit_id: int,
        *,
        is_ally: bool,
        speed: float,
        position_id: int = 1,
        max_hp: int = 0,
        atk: int = 0,
        defence: int = 0,
        element: int = 0,
        role: int = 0,
        critical_rate: int = 0,
        critical_damage_rate: int = 0,
        normal_attack_mst_id: int = 0,
        active_skill_mst_ids: Optional[List[int]] = None,
        special_attack_mst_id: int = 0,
        mst_id: int = 0,
        style_mst_id: int = 0,
        enemy_parameter_mst_id: int = 0,
        weak_elements: Optional[List[int]] = None,
        is_main_target: bool = False,
        passive_skill_infos: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        self.unit_id = unit_id
        self.is_ally = is_ally
        self.speed = float(speed) if speed else 100.0
        self.position_id = position_id
        self.max_hp = int(max_hp)
        self.atk = int(atk)
        self.defence = int(defence)
        self.element = element
        self.role = role
        self.critical_rate = critical_rate
        self.critical_damage_rate = critical_damage_rate
        self.normal_attack_mst_id = normal_attack_mst_id
        self.active_skill_mst_ids = list(active_skill_mst_ids or [])
        self.special_attack_mst_id = special_attack_mst_id
        self.mst_id = mst_id
        self.style_mst_id = style_mst_id
        self.enemy_parameter_mst_id = enemy_parameter_mst_id
        self.weak_elements = list(weak_elements or [])
        self.is_main_target = is_main_target
        self.passive_skill_infos = list(passive_skill_infos or [])

        # 战斗过程状态
        self.next_action_time = ACTION_GAUGE / self.speed
        self.turn_order_priority = 0
        self.turn_num = 0
        self.alive = True

    # -- 序列化 ------------------------------------------------------------
    def skill_set(self) -> Dict[str, Any]:
        if self.is_ally:
            return {
                "activeSkillMstIds": self.active_skill_mst_ids,
                "activeSkillWeightValues": [0 for _ in self.active_skill_mst_ids],
                "activeSkillHpGaugeValues": [0 for _ in self.active_skill_mst_ids],
                "specialAttackMstId": self.special_attack_mst_id,
                "normalAttackMstId": self.normal_attack_mst_id,
                "additionalSkillMstIds": [],
                "switchableSkillMstIds": [],
                "switchableNormalAttackMstIds": [],
            }
        # 敌方技能集（抓包中敌人只带一个主动技）
        return {
            "activeSkillMstIds": self.active_skill_mst_ids,
            "activeSkillWeightValues": [100 for _ in self.active_skill_mst_ids],
            "activeSkillHpGaugeValues": [0 for _ in self.active_skill_mst_ids],
            "additionalSkillMstIds": [],
            "switchableSkillMstIds": [],
            "switchableNormalAttackMstIds": [],
        }

    def turn_gauge(self) -> Dict[str, Any]:
        return {
            "speed": round(self.speed, 6),
            "TurnOrderPriority": self.turn_order_priority,
            "Id": self.unit_id,
            "GaugeValue": round(max(0.0, self.next_action_time) * self.speed * GAUGE_SCALE, 6),
        }

    def to_result_unit(self, dead: bool = False) -> Dict[str, Any]:
        if self.is_ally:
            unit = {
                "isCharacter": True,
                "isCharacterFigure": True,
                "serializedPassiveSkillInfos": [
                    {
                        "passiveSkillMstId": p.get("passiveSkillMstId"),
                        "level": p.get("level", 1),
                        "abilitySourceType": p.get("abilitySourceType", 1),
                    }
                    for p in self.passive_skill_infos
                ],
                "serializeBattleParameter": {
                    "$type": "ReDriveBattleCore.CharacterParameter, Assembly-CSharp",
                    "StyleMstId": self.style_mst_id,
                    "LevelReactionBreakDamageValue": 0,
                    "Element": self.element,
                    "Role": self.role,
                    "EP": 0,
                    "ATK": self.atk,
                    "DEF": self.defence,
                    "CTR": self.critical_rate,
                    "CTD": self.critical_damage_rate,
                    "HP": self.max_hp,
                    "Speed": self.speed,
                    "ElementDamageRates": [{"Element": e} for e in range(1, 7)],
                    "ElementResistRates": [{"Element": e} for e in range(1, 7)],
                    "BreakTurnGaugeSlowRatio": 250,
                    "InitialBreakedDamageReceiveRate": 1300,
                    "MaxBreakedDamageReceiveRate": 2000,
                    "BreakedDamageReceiveRateIncreaseRate": 1000,
                },
                "Id": self.unit_id,
                "MstId": self.mst_id,
                "MaxHP": self.max_hp,
                "HP": self.max_hp,
                "EP": 0,
                "MaxEP": 90,
                "SkillSet": self.skill_set(),
                "Condition": _empty_condition(),
                "TurnGauge": self.turn_gauge(),
                "PositionId": self.position_id,
                "WeakElements": [],
                "BreakPoint": {},
                "TurnNum": self.turn_num,
            }
            return unit

        # 敌方：死亡时不带 HP 字段（与抓包一致）
        unit = {
            "serializedPassiveSkillInfos": [
                {
                    "passiveSkillMstId": p.get("passiveSkillMstId"),
                    "abilitySourceType": p.get("abilitySourceType", 1),
                }
                for p in self.passive_skill_infos
            ],
            "serializedEnemyParameterMstId": self.enemy_parameter_mst_id,
            "Id": self.unit_id,
            "MstId": self.mst_id,
            "Team": 1,
            "MaxHP": self.max_hp,
            "SkillSet": self.skill_set(),
            "Condition": _empty_condition(),
            "TurnGauge": self.turn_gauge(),
            "PositionId": self.position_id,
            "WeakElements": self.weak_elements,
            "BreakPoint": {"maxPointValue": 450, "BreakCount": 0},
            "TurnNum": self.turn_num,
            "EnemyConditionAndActionController": {
                "conditionAndActionList": [],
                "CachedSkillMstIds": [],
                "EnemyStartConditionTimingActionList": [],
            },
        }
        if not dead:
            unit["HP"] = self.max_hp
        return unit


def _empty_condition() -> Dict[str, Any]:
    return {
        "StateList": [],
        "StateIcons": [],
        "VisualEffectNames": [],
        "VisualShaderName": "",
        "IsAbnormalState": False,
        "ZoneEffectId": -1,
    }


# ---------------------------------------------------------------------------
# 生成器
# ---------------------------------------------------------------------------
class SoloRaidBattleLogBuilder:
    """把一场"击杀 boss"的战斗推理成可提交的战斗日志。"""

    def __init__(
        self,
        allies: List[BattleUnit],
        enemies: List[BattleUnit],
        *,
        boss_max_hp: int,
        kill_timing: str = TIMING_MIDDLE,
        limit_round: int = 1,
        wave: int = 1,
        season_buff_turn_gauge: float = 0.0,
        kill_time_jitter: float = KILL_TIME_JITTER,
        seed: Optional[int] = None,
    ) -> None:
        # 生成器可被复用，这里把传入单位的状态重置干净
        for unit in list(allies) + list(enemies):
            unit.alive = True
            unit.turn_num = 0
            unit.turn_order_priority = 0

        self.allies = [u for u in allies if u.alive]
        self.enemies = [u for u in enemies if u.alive]
        self.boss_max_hp = max(1, int(boss_max_hp))
        self.kill_timing = kill_timing if kill_timing in KILL_TIMINGS else TIMING_MIDDLE
        self.limit_round = max(1, int(limit_round))
        self.wave = max(1, int(wave))
        self.season_buff_turn_gauge = float(season_buff_turn_gauge or 0.0)
        self.kill_time_jitter = max(0.0, min(1.0, float(kill_time_jitter)))
        self.rng = random.Random(seed)
        # 斩杀落在第几回合，由 plan_kill() 在模拟开始前定下
        self.kill_round = self.target_round

        # 主目标（打伤害的那个部位），没有标记时取第一个敌人
        self.main_target = next(
            (e for e in self.enemies if e.is_main_target), None
        ) or (self.enemies[0] if self.enemies else None)

    # -- 斩杀时机 ----------------------------------------------------------
    @property
    def target_round(self) -> int:
        """名义上在第几回合收尾（未加波动）。"""
        if self.kill_timing == TIMING_INSTANT:
            return 1
        if self.kill_timing == TIMING_MIDDLE:
            return max(1, math.ceil(self.limit_round / 2))
        return self.limit_round

    def _nominal_slot(self, n_allies: int) -> int:
        """名义上由本回合的第几个我方行动完成斩杀（0 起算）。"""
        if self.kill_timing == TIMING_INSTANT:
            return 0
        if self.kill_timing == TIMING_MIDDLE:
            return n_allies // 2
        return max(0, n_allies - 1)

    def plan_kill(self) -> Tuple[int, int]:
        """定下斩杀点，返回 ``(第几个我方行动, 所在回合)``，行动序号从 1 起算。

        名义位置 = 目标回合之前的全部我方行动 + 该回合内的名义槽位；再乘一个
        ``1 ± kill_time_jitter`` 的随机因子，最后夹回
        ``[1, 目标回合内的我方行动总数]``。所以斩杀点会在名义位置上下浮动，
        不会每次都卡在同一个行动上。

        波动是在**整个战斗的行动序列**上算的，不是按回合算——回合是整数，
        对 ±10% 不敏感（3 回合的 ±10% 还不到半回合）。

        ``instant`` 的名义位置就是第 1 个行动，±10% 之后仍是 1：秒杀本来就该是
        第一刀，这里不做特殊处理。
        """
        n_allies = len(self.allies)
        if n_allies <= 0:
            return 1, 1
        nominal = (
            (self.target_round - 1) * n_allies + self._nominal_slot(n_allies) + 1
        )
        total = self.target_round * n_allies
        factor = 1.0 + self.rng.uniform(
            -self.kill_time_jitter, self.kill_time_jitter
        )
        index = max(1, min(total, int(round(nominal * factor))))
        return index, (index - 1) // n_allies + 1

    # -- 主流程 ------------------------------------------------------------
    def build(self) -> Dict[str, Any]:
        """返回 {"battleLog": <json 字符串>, "battleInfo": {...}}。"""
        if not self.allies or not self.enemies:
            # 数据不全时退化成极简日志，交给上层决定是否提交
            return {
                "battleLog": json.dumps(
                    {"Commands": [], "ResultBattleUnits": [], "ResultRound": 1},
                    ensure_ascii=False,
                ),
                "battleInfo": self._battle_info(),
            }

        commands = self._simulate()
        result_units = [u.to_result_unit() for u in self.allies]
        result_units += [u.to_result_unit(dead=True) for u in self.enemies]

        battle_log = {
            "Commands": commands,
            "ResultBattleUnits": result_units,
            "ResultRound": self.kill_round,
        }
        return {
            "battleLog": json.dumps(battle_log, ensure_ascii=False),
            "battleInfo": self._battle_info(),
        }

    def build_minimal(self) -> Dict[str, Any]:
        """极简日志：只报告"boss 已阵亡"，不带行动指令。

        没有行动指令可算，但 ``ResultRound`` 仍然按同样的波动规则给出，
        免得极简模式和模拟模式报的回合数口径不一致。
        """
        result_units = [u.to_result_unit() for u in self.allies]
        result_units += [u.to_result_unit(dead=True) for u in self.enemies]
        battle_log = {
            "Commands": [],
            "ResultBattleUnits": result_units,
            "ResultRound": self.plan_kill()[1],
        }
        return {
            "battleLog": json.dumps(battle_log, ensure_ascii=False),
            "battleInfo": self._battle_info(),
        }

    # -- battleInfo（提交时表示"敌人已全灭"的终局状态）----------------------
    def _battle_info(self) -> Dict[str, Any]:
        return {
            "wave": self.wave,
            "enemyInfoList": [],
            "enemyLinkHp": 0,
            "enemyCountDownNum": 0,
            "enemyCountDownDamage": 0,
            "isSeasonBuffActive": self.season_buff_turn_gauge > 0,
            "seasonBuffPoint": 30 if self.season_buff_turn_gauge > 0 else 0,
            "seasonBuffTurnGaugeValue": round(self.season_buff_turn_gauge, 6),
            "nextEnemyIndex": 0,
        }

    # -- 模拟 --------------------------------------------------------------
    def _simulate(self) -> List[Dict[str, Any]]:
        """逐回合推进：每回合所有存活单位按速度从高到低行动一次。

        斩杀点先由 :meth:`plan_kill` 定下——它是**整个战斗行动序列**上的绝对序号
        （只数我方行动，从 1 起算），带着 ±``kill_time_jitter`` 的波动。模拟时用一个
        跨回合累加的我方行动计数器去对齐这个序号，命中即停。
        """
        units: List[BattleUnit] = list(self.allies) + list(self.enemies)
        for u in units:
            u.alive = True
            u.turn_order_priority = 0
            u.turn_num = 0
            u.next_action_time = ACTION_GAUGE / u.speed

        commands: List[Dict[str, Any]] = []
        pending_hits: List[int] = []
        info_id = 1
        elapsed = 0.0
        kill_index, self.kill_round = self.plan_kill()
        # 跨回合累加的我方行动数，从 0 起算，+1 后即"第几个我方行动"
        ally_seq = 0
        killed = False

        for current_round in range(1, self.kill_round + 1):
            order = sorted(
                (u for u in units if u.alive),
                key=lambda u: (not u.is_ally, -u.speed, u.unit_id),
            )
            if not any(u.is_ally for u in order):
                break

            for position, actor in enumerate(order):
                delta = self.rng.uniform(0.2, 2.0)
                elapsed += delta
                actor.turn_num += 1
                actor.turn_order_priority = 100 + int(actor.speed * elapsed * 0.1)
                round_gauge = ROUND_TIME * (1 - (position + 1) / len(order))
                commands.append(
                    self._begin_turn(order, actor, info_id, current_round, round_gauge, delta)
                )
                info_id += 1

                if actor.is_ally:
                    commands.append(self._common_act(actor, info_id))
                    info_id += 1
                    commands.append(
                        self._ally_skill(actor, info_id, pending_hits, ally_seq)
                    )
                    info_id += 1
                    ally_seq += 1
                    if ally_seq >= kill_index:
                        killed = True
                else:
                    commands.append(self._common_act(actor, info_id))
                    info_id += 1
                    commands.append(self._enemy_skill(actor, info_id))
                    info_id += 1

                if killed:
                    break
            if killed:
                break

        self._finalize_kill(commands, pending_hits)
        return commands

    # -- 指令构造 ----------------------------------------------------------
    def _begin_turn(
        self,
        alive_units: List[BattleUnit],
        actor: BattleUnit,
        info_id: int,
        current_round: int,
        round_gauge: float,
        delta: float,
    ) -> Dict[str, Any]:
        # 已行动过的单位用 TurnOrderPriority，未行动的用 GaugeValue
        order_list: List[Dict[str, Any]] = []
        for u in sorted(alive_units, key=lambda x: x.next_action_time):
            item: Dict[str, Any] = {"BattleUnitId": u.unit_id}
            if u is actor:
                item["TurnOrderPriority"] = u.turn_order_priority
                order_list.insert(0, item)
                continue
            item["GaugeValue"] = round(max(0.0, u.next_action_time) * u.speed * GAUGE_SCALE, 6)
            if u.turn_num > 0:
                item["TurnOrderPriority"] = u.turn_order_priority
            if not u.is_ally:
                item["TeamType"] = 1
            order_list.append(item)

        info = {
            "InfoId": info_id,
            "CurrentTurnUnitId": actor.unit_id,
            "TurnOrderUnitInfoList": order_list,
            "ActOrderUnitInfoList": [{"BattleUnitId": actor.unit_id} for _ in range(3)],
            "NextRound": current_round + 1,
            "GaugeValueToNextRound": round(round_gauge, 6),
            "ActiveCurrentSeasonBuffTurnGaugeValue": round(self.season_buff_turn_gauge, 6),
        }
        return {
            "$type": CMD_BEGIN_TURN,
            "TurnActOrderUnitInfo": info,
            "CurrentRound": current_round,
            "CurrentWave": self.wave,
            "DeltaActionTime": round(delta, 6),
        }

    def _common_act(self, actor: BattleUnit, info_id: int) -> Dict[str, Any]:
        return {
            "$type": CMD_COMMON_ACT,
            "ActUnitId": actor.unit_id,
            "AffectedUnitNoticeList": [],
            "GainSoloRaidBuffPointNoticeList": [],
        }

    def _ally_skill(
        self,
        actor: BattleUnit,
        info_id: int,
        pending_hits: List[int],
        action_index: int,
    ) -> Dict[str, Any]:
        skill_id = self._pick_ally_skill(actor, action_index)
        target = self.main_target
        notice = self._damage_notice(actor, target, pending_hits, action_index)
        return {
            "$type": CMD_SKILL,
            "MainTargetUnitId": target.unit_id if target else 0,
            "ResultSP": self.rng.randint(3, 5),
            "ResultSPBeforeApplyPassiveSkill": self.rng.randint(2, 4),
            "SkillMstId": skill_id,
            "AddEnemyInfos": [],
            "ActUnitId": actor.unit_id,
            "AffectedUnitNoticeList": notice,
        }

    def _enemy_skill(self, actor: BattleUnit, info_id: int) -> Dict[str, Any]:
        skill_id = actor.active_skill_mst_ids[0] if actor.active_skill_mst_ids else 0
        target = self.rng.choice(self.allies)
        return {
            "$type": CMD_SKILL,
            "MainTargetUnitId": target.unit_id,
            "ResultSP": self.rng.randint(3, 5),
            "ResultSPBeforeApplyPassiveSkill": self.rng.randint(2, 4),
            "SkillMstId": skill_id,
            "AddEnemyInfos": [],
            "ActUnitId": actor.unit_id,
            "AffectedUnitNoticeList": [
                {
                    "Damages": [
                        {
                            "DamageValue": max(1, int(target.max_hp * 0.02)),
                            "AttackElement": actor.element or 1,
                            "Category": 1,
                        }
                    ],
                    "AffectedUnitId": target.unit_id,
                    "IsReceivedAttack": True,
                    "IsVisibleOnAttack": True,
                    "NonDamageVisualEffectList": [STATE_DEBUFF_EFFECT],
                    "AddStateInfoList": [],
                    "ReceivedSlipDamageEffectTypeList": [],
                }
            ],
        }

    def _pick_ally_skill(self, actor: BattleUnit, action_index: int) -> int:
        # 开局先放一次 buff（主动技），之后交替普通攻击，贴合真实节奏
        if actor.active_skill_mst_ids and action_index <= len(self.allies):
            return actor.active_skill_mst_ids[0]
        if action_index % 4 == 0 and actor.special_attack_mst_id:
            return actor.special_attack_mst_id
        return actor.normal_attack_mst_id or (
            actor.active_skill_mst_ids[0] if actor.active_skill_mst_ids else 0
        )

    def _damage_notice(
        self,
        actor: BattleUnit,
        target: Optional[BattleUnit],
        pending_hits: List[int],
        action_index: int,
    ) -> List[Dict[str, Any]]:
        if target is None:
            return []
        # 基础伤害：以攻击力为量纲，随行动次数增长（模拟 buff 叠加）
        base = max(1, int(actor.atk * self.rng.uniform(1.5, 3.0) * (1 + action_index * 0.08)))
        pending_hits.append(base)
        damage = {
            "DamageValue": base,
            "AttackElement": actor.element or 1,
            "CorrelationDamageType": 2,
            "Category": 1,
        }
        if self.rng.random() < 0.4:
            damage["IsCritical"] = True
        notice = [
            {
                "Damages": [damage],
                "AffectedUnitId": target.unit_id,
                "IsReceivedAttack": True,
                "IsVisibleOnAttack": True,
                "IsWeakElementAttacked": True,
                "NonDamageVisualEffectList": [STATE_DEBUFF_EFFECT],
                "AddStateInfoList": [],
                "ReceivedSlipDamageEffectTypeList": [],
            }
        ]
        return notice

    def _finalize_kill(
        self, commands: List[Dict[str, Any]], pending_hits: List[int]
    ) -> None:
        """把伤害额度分摊到各次命中，并让最后一击造成致命伤害、标记 boss 阵亡。"""
        if self.main_target is None:
            return

        # 收集主目标受到的普通伤害（Category 1）命中点
        hits: List[tuple] = []
        for cmd in commands:
            if cmd.get("$type") != CMD_SKILL:
                continue
            for notice in cmd.get("AffectedUnitNoticeList", []):
                if notice.get("AffectedUnitId") != self.main_target.unit_id:
                    continue
                for damage in notice.get("Damages", []):
                    if damage.get("Category") == 1:
                        hits.append((damage, notice))
        if not hits:
            return

        target_total = int(self.boss_max_hp * 1.02)
        count = len(hits)
        # 前面的命中分摊 35%（越靠后越高），最后一击占 65% 并负责斩杀
        front_total = int(target_total * 0.35) if count > 1 else 0
        weights = [i + 1 for i in range(count - 1)] if count > 1 else []
        weight_sum = sum(weights) or 1

        remaining = target_total
        for index, (damage, notice) in enumerate(hits):
            if index == count - 1:
                damage["DamageValue"] = max(remaining, 1)
                damage["IsBreakBonusApplied"] = True
                damage["IsMaxBreakBonusWhenHit"] = True
                notice["IsDead"] = True
            else:
                value = max(1, int(front_total * weights[index] / weight_sum))
                damage["DamageValue"] = value
                remaining -= value

        # 其余部位在最后一击一并判死
        last_cmd = next(
            (
                cmd
                for cmd in reversed(commands)
                if cmd.get("$type") == CMD_SKILL
                and any(n.get("IsDead") for n in cmd.get("AffectedUnitNoticeList", []))
            ),
            None,
        )
        if last_cmd is None:
            return
        element = self.allies[0].element if self.allies else 1
        for enemy in self.enemies:
            if enemy is self.main_target:
                continue
            last_cmd["AffectedUnitNoticeList"].append(
                {
                    "Damages": [
                        {
                            "DamageValue": max(1, enemy.max_hp),
                            "AttackElement": element or 1,
                            "IsCritical": True,
                            "CorrelationDamageType": 2,
                            "Category": 1,
                        }
                    ],
                    "AffectedUnitId": enemy.unit_id,
                    "IsReceivedAttack": True,
                    "IsVisibleOnAttack": True,
                    "IsDead": True,
                    "IsWeakElementAttacked": True,
                    "NonDamageVisualEffectList": [STATE_DEBUFF_EFFECT],
                    "AddStateInfoList": [],
                    "ReceivedSlipDamageEffectTypeList": [],
                }
            )
        for enemy in self.enemies:
            enemy.alive = False


def build_solo_raid_battle_log(
    allies: List[BattleUnit],
    enemies: List[BattleUnit],
    *,
    boss_max_hp: int,
    kill_timing: str = TIMING_MIDDLE,
    limit_round: int = 1,
    wave: int = 1,
    season_buff_turn_gauge: float = 0.0,
    mode: str = MODE_SIMULATE,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """便捷入口。返回 {"battleLog": str, "battleInfo": dict}。"""
    builder = SoloRaidBattleLogBuilder(
        allies,
        enemies,
        boss_max_hp=boss_max_hp,
        kill_timing=kill_timing,
        limit_round=limit_round,
        wave=wave,
        season_buff_turn_gauge=season_buff_turn_gauge,
        seed=seed,
    )
    if mode == MODE_MINIMAL:
        return builder.build_minimal()
    return builder.build()
