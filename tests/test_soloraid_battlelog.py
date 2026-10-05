"""总力战战斗日志生成器的离线测试（不依赖网络与账号）。"""
import json
import unittest

from autopcr.util.soloraid_battlelog import (
    BattleUnit,
    build_solo_raid_battle_log,
    KILL_TIME_JITTER,
    MODE_MINIMAL,
    MODE_SIMULATE,
    SoloRaidBattleLogBuilder,
    TIMING_INSTANT,
    TIMING_LAST,
    TIMING_MIDDLE,
)

BOSS_HP = 150_000_000
N_ALLIES = 5
LIMIT_ROUND = 3


def make_allies():
    return [
        BattleUnit(
            index + 1,
            is_ally=True,
            speed=100 + index,
            position_id=index + 1,
            max_hp=12000,
            atk=3200,
            defence=4000,
            element=3,
            role=3,
            critical_rate=100,
            critical_damage_rate=200,
            normal_attack_mst_id=103010,
            active_skill_mst_ids=[103110],
            special_attack_mst_id=103207,
            mst_id=1000 + index,
            style_mst_id=10160101,
        )
        for index in range(5)
    ]


def make_enemies():
    enemies = []
    for index in range(5):
        enemies.append(
            BattleUnit(
                -(index + 1),
                is_ally=False,
                speed=210,
                position_id=index + 1,
                max_hp=BOSS_HP,
                atk=5000,
                defence=3000,
                mst_id=600007 + index,
                enemy_parameter_mst_id=140710411,
                weak_elements=[1, 2, 3],
                is_main_target=(index == 0),
                active_skill_mst_ids=[1001019],
            )
        )
    return enemies


def build(timing, mode=MODE_SIMULATE, limit_round=LIMIT_ROUND):
    return build_solo_raid_battle_log(
        make_allies(),
        make_enemies(),
        boss_max_hp=BOSS_HP,
        kill_timing=timing,
        limit_round=limit_round,
        wave=2,
        season_buff_turn_gauge=15.76,
        mode=mode,
        seed=1234,
    )


def count_ally_actions(log):
    """日志里我方一共行动了几次（每名我方单位一次技能指令 = 一次行动）。"""
    return sum(
        1
        for command in log["Commands"]
        if command["$type"].endswith("CommandSkill, Assembly-CSharp")
        and command["ActUnitId"] > 0
    )


def main_target_damage(log):
    total = 0
    killed = False
    for command in log["Commands"]:
        if not command["$type"].endswith("CommandSkill, Assembly-CSharp"):
            continue
        for notice in command["AffectedUnitNoticeList"]:
            for damage in notice.get("Damages", []):
                if notice["AffectedUnitId"] == -1 and damage.get("Category") == 1:
                    total += damage["DamageValue"]
            if notice["AffectedUnitId"] == -1 and notice.get("IsDead"):
                killed = True
    return total, killed


class BattleLogTests(unittest.TestCase):
    def test_kill_timing_controls_round(self):
        """斩杀回合由时机决定：instant 第 1 回合、middle 第 2 回合、last 第 3 回合。

        ±10% 的波动作用在整个战斗的行动序列上，本用例里 5 名我方单位、上限 3 回合，
        名义斩杀点是第 1 / 8 / 15 个我方行动，波动后最多挪动 ±1.5 个行动，
        所以只会改变「回合内的第几个行动」，不会跨回合。
        """
        expected = {
            TIMING_INSTANT: 1,
            TIMING_MIDDLE: 2,  # ceil(3 / 2)
            TIMING_LAST: 3,
        }
        for timing, rounds in expected.items():
            with self.subTest(timing=timing):
                log = json.loads(build(timing)["battleLog"])
                self.assertEqual(log["ResultRound"], rounds)

    def test_damage_is_lethal(self):
        for timing in (TIMING_INSTANT, TIMING_MIDDLE, TIMING_LAST):
            with self.subTest(timing=timing):
                log = json.loads(build(timing)["battleLog"])
                damage, killed = main_target_damage(log)
                self.assertGreaterEqual(damage, BOSS_HP)
                self.assertTrue(killed)

    def test_result_units_state(self):
        log = json.loads(build(TIMING_LAST)["battleLog"])
        allies = [u for u in log["ResultBattleUnits"] if u["Id"] > 0]
        enemies = [u for u in log["ResultBattleUnits"] if u["Id"] < 0]
        self.assertEqual(len(allies), 5)
        self.assertEqual(len(enemies), 5)
        for unit in allies:
            self.assertIn("HP", unit)
            self.assertEqual(unit["HP"], unit["MaxHP"])
        for unit in enemies:
            self.assertNotIn("HP", unit)  # 阵亡单位不带 HP 字段
            self.assertEqual(unit["MaxHP"], BOSS_HP)

    def test_command_structure(self):
        log = json.loads(build(TIMING_MIDDLE)["battleLog"])
        self.assertTrue(log["Commands"])
        for command in log["Commands"]:
            self.assertIn("$type", command)
            if command["$type"].endswith("CommandBeginTurn, Assembly-CSharp"):
                info = command["TurnActOrderUnitInfo"]
                for key in ("InfoId", "CurrentTurnUnitId", "TurnOrderUnitInfoList",
                            "NextRound", "GaugeValueToNextRound"):
                    self.assertIn(key, info)
                self.assertIn("CurrentRound", command)
                self.assertIn("CurrentWave", command)
            elif command["$type"].endswith("CommandSkill, Assembly-CSharp"):
                for key in ("MainTargetUnitId", "SkillMstId", "ActUnitId",
                            "AffectedUnitNoticeList"):
                    self.assertIn(key, command)

    def test_battle_info_marks_enemies_cleared(self):
        info = build(TIMING_INSTANT)["battleInfo"]
        self.assertEqual(info["enemyInfoList"], [])
        self.assertEqual(info["wave"], 2)
        self.assertTrue(info["isSeasonBuffActive"])

    def test_minimal_mode(self):
        built = build(TIMING_INSTANT, mode=MODE_MINIMAL)
        log = json.loads(built["battleLog"])
        self.assertEqual(log["Commands"], [])
        self.assertEqual(len(log["ResultBattleUnits"]), 10)
        self.assertEqual(log["ResultRound"], 1)

    def test_builder_is_reusable(self):
        """同一个 builder 复用同一批单位对象时不应互相污染。"""
        allies, enemies = make_allies(), make_enemies()
        for _ in range(3):
            built = build_solo_raid_battle_log(
                allies, enemies, boss_max_hp=BOSS_HP,
                kill_timing=TIMING_LAST, limit_round=LIMIT_ROUND, wave=2, seed=5,
            )
            log = json.loads(built["battleLog"])
            self.assertEqual(len(log["Commands"]) > 0, True)
            self.assertEqual(log["ResultRound"], 3)


class KillTimeJitterTests(unittest.TestCase):
    """斩杀时间波动：斩杀点落在整个战斗的我方行动序列上，围绕名义位置上下浮动 ±10%。"""

    # 5 名我方单位、上限 3 回合时，各时机的名义斩杀点（第几个我方行动）
    NOMINAL = {
        TIMING_INSTANT: 1,
        TIMING_MIDDLE: 8,
        TIMING_LAST: 15,
    }

    def builder(self, timing, *, jitter=KILL_TIME_JITTER, seed=1234):
        return SoloRaidBattleLogBuilder(
            make_allies(),
            make_enemies(),
            boss_max_hp=BOSS_HP,
            kill_timing=timing,
            limit_round=LIMIT_ROUND,
            wave=2,
            seed=seed,
            kill_time_jitter=jitter,
        )

    def bounds(self, nominal):
        """名义位置 ±10% 之后，允许落在的闭区间。"""
        total = LIMIT_ROUND * N_ALLIES
        low = max(1, int(round(nominal * (1 - KILL_TIME_JITTER))))
        high = min(total, int(round(nominal * (1 + KILL_TIME_JITTER))))
        return low, high

    def test_nominal_kill_point(self):
        """波动设为 0 时，斩杀点就是名义位置，且回合号与行动序号自洽。"""
        for timing, nominal in self.NOMINAL.items():
            with self.subTest(timing=timing):
                index, round_ = self.builder(timing, jitter=0.0).plan_kill()
                self.assertEqual(index, nominal)
                self.assertEqual(round_, (nominal - 1) // N_ALLIES + 1)

    def test_jitter_stays_within_ten_percent(self):
        """换任意随机种子，斩杀点都被夹在名义位置的 ±10% 区间内，不越界。"""
        for timing, nominal in self.NOMINAL.items():
            low, high = self.bounds(nominal)
            for seed in range(200):
                with self.subTest(timing=timing, seed=seed):
                    index, _ = self.builder(timing, seed=seed).plan_kill()
                    self.assertGreaterEqual(index, low)
                    self.assertLessEqual(index, high)

    def test_jitter_actually_varies_the_kill_point(self):
        """波动确实让斩杀点散开，而不是每次都卡在同一个行动上。"""
        for timing in (TIMING_MIDDLE, TIMING_LAST):
            with self.subTest(timing=timing):
                points = {
                    self.builder(timing, seed=seed).plan_kill()[0]
                    for seed in range(200)
                }
                self.assertGreater(
                    len(points), 1, f"{timing} 的斩杀点在 200 个种子下没有变化"
                )
                # 散开的范围必须仍在 ±10% 内
                low, high = self.bounds(self.NOMINAL[timing])
                self.assertGreaterEqual(min(points), low)
                self.assertLessEqual(max(points), high)

    def test_jitter_input_is_clamped(self):
        """波动幅度被夹到 [0, 1]，传离谱的值也不会炸。"""
        for value, expected in ((5.0, 1.0), (-3.0, 0.0), (0.25, 0.25)):
            with self.subTest(value=value):
                self.assertEqual(
                    self.builder(TIMING_LAST, jitter=value).kill_time_jitter, expected
                )
        # 拉满波动时，斩杀点依然落在合法区间，且回合号推导一致
        index, round_ = self.builder(TIMING_LAST, jitter=1.0, seed=7).plan_kill()
        self.assertGreaterEqual(index, 1)
        self.assertLessEqual(index, LIMIT_ROUND * N_ALLIES)
        self.assertEqual(round_, (index - 1) // N_ALLIES + 1)

    def test_simulated_log_matches_planned_kill_point(self):
        """模拟出的日志里，我方行动次数正好等于计划好的斩杀点。"""
        for timing, nominal in self.NOMINAL.items():
            low, high = self.bounds(nominal)
            for seed in (1, 2, 3):
                with self.subTest(timing=timing, seed=seed):
                    builder = self.builder(timing, seed=seed)
                    log = json.loads(builder.build()["battleLog"])
                    actions = count_ally_actions(log)
                    self.assertGreaterEqual(actions, low)
                    self.assertLessEqual(actions, high)
                    # 报告出来的回合数必须和实际打了几个行动对得上
                    self.assertEqual(
                        log["ResultRound"], (actions - 1) // N_ALLIES + 1
                    )

    def test_minimal_mode_uses_same_jitter_rule(self):
        """极简模式没有行动指令，但 ResultRound 走同一套波动规则。"""
        rounds = {
            json.loads(self.builder(TIMING_LAST, seed=seed).build_minimal()["battleLog"])[
                "ResultRound"
            ]
            for seed in range(200)
        }
        self.assertTrue(rounds)
        self.assertTrue(rounds.issubset({1, 2, 3}))


if __name__ == "__main__":
    unittest.main()
