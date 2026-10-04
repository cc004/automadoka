"""总力战战斗日志生成器的离线测试（不依赖网络与账号）。"""
import json
import unittest

from autopcr.util.soloraid_battlelog import (
    BattleUnit,
    build_solo_raid_battle_log,
    MODE_MINIMAL,
    MODE_SIMULATE,
    TIMING_INSTANT,
    TIMING_LAST,
    TIMING_MIDDLE,
)

BOSS_HP = 150_000_000


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


def build(timing, mode=MODE_SIMULATE, limit_round=3):
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
        expected = {
            TIMING_INSTANT: 1,
            TIMING_MIDDLE: 2,
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
                kill_timing=TIMING_LAST, limit_round=3, wave=2, seed=5,
            )
            log = json.loads(built["battleLog"])
            self.assertEqual(len(log["Commands"]) > 0, True)
            self.assertEqual(log["ResultRound"], 3)


if __name__ == "__main__":
    unittest.main()
