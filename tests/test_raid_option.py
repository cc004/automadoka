"""「魔女召唤」纯逻辑的离线测试（不依赖网络与账号）。

只导入 `autopcr.util.raidoption` —— 模块本体在 `autopcr.module.modules` 包里，
导入它会连带 `raid/raidrunner.py`（在模块顶层 open `raid_config.json`），
干净仓库上没有那个文件。
"""
import unittest
from types import SimpleNamespace

from autopcr.util.raidoption import (
    AUTO_DIFFICULTY_NOTE,
    EXEC_LIKE_MEDAL_TYPE,
    highest_unlocked_difficulty,
    medal_per_like,
    parse_raid_difficulty,
    parse_raid_times,
    pending_rewards,
    RAID_DIFFICULTY_MAX,
    RAID_RESULT_LOSE,
    RAID_RESULT_TIMEOUT,
    RAID_RESULT_WIN,
    RAID_TIMES_MAX,
    RAID_TIMES_MIN,
    resolve_battle_result,
)


def stage(identifier, closed, host=1):
    return SimpleNamespace(multiRaidStageDataId=identifier, multiRaidStageMstId=identifier * 100,
                           isClosed=closed, hostUserId=host)


def room(stage_id, user, received=False, quest=1):
    return SimpleNamespace(multiRaidStageDataId=stage_id, multiRaidStageMstId=stage_id * 100,
                           userId=user, isReceivedReward=received, questDataId=quest)


class medal:
    """假装是 `FriendFriendMedal`：`type` 在生成缓存里可能叫 `type_`。"""

    def __init__(self, value, num, field='type'):
        self._value = value
        self.num = num
        self._field = field

    def dict(self, by_alias=False):
        return {('type' if by_alias else self._field): self._value}


class HighestUnlockedDifficultyTests(unittest.TestCase):
    def test_next_difficulty_after_cleared(self):
        self.assertEqual(highest_unlocked_difficulty(0), 1)
        self.assertEqual(highest_unlocked_difficulty(1), 2)
        self.assertEqual(highest_unlocked_difficulty(7), 8)

    def test_stops_at_the_cap(self):
        self.assertEqual(highest_unlocked_difficulty(19), RAID_DIFFICULTY_MAX)
        self.assertEqual(highest_unlocked_difficulty(20), RAID_DIFFICULTY_MAX)
        self.assertEqual(highest_unlocked_difficulty(99), RAID_DIFFICULTY_MAX)

    def test_missing_value_falls_back_to_first_level(self):
        self.assertEqual(highest_unlocked_difficulty(None), 1)


class ParseRaidDifficultyTests(unittest.TestCase):
    def test_blank_means_auto(self):
        for raw in ("", "   ", None):
            with self.subTest(raw=raw):
                difficulty, note = parse_raid_difficulty(raw, 4)
                self.assertEqual(difficulty, 5)
                self.assertEqual(note, AUTO_DIFFICULTY_NOTE)

    def test_zero_and_garbage_mean_auto(self):
        for raw in ("0", "-3", "abc", "Lv.5"):
            with self.subTest(raw=raw):
                difficulty, note = parse_raid_difficulty(raw, 9)
                self.assertEqual(difficulty, 10)
                self.assertEqual(note, AUTO_DIFFICULTY_NOTE)

    def test_explicit_level_is_used(self):
        difficulty, note = parse_raid_difficulty("12", 4)
        self.assertEqual(difficulty, 12)
        self.assertEqual(note, "指定 Lv.12")

    def test_explicit_level_ignores_cleared_difficulty(self):
        # 指定难度不再受「已通关 +1」影响
        self.assertEqual(parse_raid_difficulty("3", 18)[0], 3)

    def test_out_of_range_is_clamped_and_reported(self):
        difficulty, note = parse_raid_difficulty("25", 1)
        self.assertEqual(difficulty, RAID_DIFFICULTY_MAX)
        self.assertIn("25", note)
        self.assertIn(str(RAID_DIFFICULTY_MAX), note)

    def test_whitespace_is_trimmed(self):
        self.assertEqual(parse_raid_difficulty("  6  ", 1)[0], 6)


class ResolveBattleResultTests(unittest.TestCase):
    def test_auto_reports_win_when_damage_covers_boss(self):
        self.assertEqual(resolve_battle_result(True, 3, 1_100_000, 1_000_000), RAID_RESULT_WIN)

    def test_auto_reports_win_on_exact_kill(self):
        self.assertEqual(resolve_battle_result(True, 3, 1_000_000, 1_000_000), RAID_RESULT_WIN)

    def test_auto_reports_timeout_when_boss_survives(self):
        self.assertEqual(resolve_battle_result(True, 1, 900_000, 1_000_000), RAID_RESULT_TIMEOUT)

    def test_auto_does_not_call_a_dead_boss_a_win(self):
        self.assertEqual(resolve_battle_result(True, 1, 5_000, 0), RAID_RESULT_TIMEOUT)

    def test_auto_ignores_the_manual_value(self):
        for manual in (1, 2, 3, "x", None):
            with self.subTest(manual=manual):
                self.assertEqual(
                    resolve_battle_result(True, manual, 500, 1_000), RAID_RESULT_TIMEOUT
                )

    def test_manual_value_is_used_when_auto_is_off(self):
        for manual in (RAID_RESULT_WIN, RAID_RESULT_LOSE, RAID_RESULT_TIMEOUT):
            with self.subTest(manual=manual):
                self.assertEqual(
                    resolve_battle_result(False, manual, 999_999, 1_000_000), manual
                )

    def test_invalid_manual_value_falls_back_to_timeout(self):
        for manual in (0, 4, 99, "", None, "win"):
            with self.subTest(manual=manual):
                self.assertEqual(
                    resolve_battle_result(False, manual, 1, 1), RAID_RESULT_TIMEOUT
                )


class ParseRaidTimesTests(unittest.TestCase):
    def test_normal_values(self):
        self.assertEqual(parse_raid_times(1), 1)
        self.assertEqual(parse_raid_times(6), 6)
        self.assertEqual(parse_raid_times("3"), 3)

    def test_values_are_clamped(self):
        self.assertEqual(parse_raid_times(0), RAID_TIMES_MIN)
        self.assertEqual(parse_raid_times(-5), RAID_TIMES_MIN)
        self.assertEqual(parse_raid_times(99), RAID_TIMES_MAX)

    def test_garbage_falls_back_to_one(self):
        for raw in ("", None, "abc", "1.5"):
            with self.subTest(raw=raw):
                self.assertEqual(parse_raid_times(raw), RAID_TIMES_MIN)


class MedalPerLikeTests(unittest.TestCase):
    """`friendConfig.friendMedal` 里挑「点赞给勋章」那一行。

    原来这里是 `next(...)` 没给默认值：配置一变就抛 `StopIteration`，
    从协程里逃出来变成 `RuntimeError`，「魔女点赞」整个模块报错。
    """

    def test_picks_the_exec_like_row(self):
        medals = [medal('Follow', 5), medal(EXEC_LIKE_MEDAL_TYPE, 2)]
        self.assertEqual(medal_per_like(medals), 2)

    def test_uses_the_alias_not_the_python_field_name(self):
        # 生成缓存里字段叫 type_，只有 by_alias=True 才拿得到 'type'
        medals = [medal(EXEC_LIKE_MEDAL_TYPE, 3, field='type_')]
        self.assertEqual(medal_per_like(medals), 3)

    def test_missing_row_returns_zero_instead_of_raising(self):
        medals = [medal('Follow', 5), medal('Login', 1)]
        self.assertEqual(medal_per_like(medals), 0)

    def test_empty_and_none_are_zero(self):
        for medals in ([], None):
            with self.subTest(medals=medals):
                self.assertEqual(medal_per_like(medals), 0)

    def test_zero_or_missing_num_is_zero(self):
        self.assertEqual(medal_per_like([medal(EXEC_LIKE_MEDAL_TYPE, 0)]), 0)
        self.assertEqual(medal_per_like([medal(EXEC_LIKE_MEDAL_TYPE, None)]), 0)


class PendingRewardsTests(unittest.TestCase):
    """`multiRaidRoomDataList` 里含别人的房间，只能领自己的。

    夹具取自 RustMadoka 的真实抓包样本：关卡 55 下同时存在 userId 20 和 userId 10
    两条房间记录，自己（10）的房间是 questDataId 77。
    """

    def test_only_own_room_is_claimable(self):
        stages = [stage(55, closed=True, host=20)]
        rooms = [room(55, user=20, quest=999), room(55, user=10, quest=77)]
        found = pending_rewards(stages, rooms, 10)
        self.assertEqual([r.questDataId for _, r in found], [77])

    def test_other_users_rooms_are_never_claimed(self):
        stages = [stage(55, closed=True)]
        rooms = [room(55, user=20, quest=999), room(55, user=30, quest=888)]
        self.assertEqual(pending_rewards(stages, rooms, 10), [])

    def test_open_stage_is_skipped(self):
        stages = [stage(55, closed=False)]
        self.assertEqual(pending_rewards(stages, [room(55, user=10)], 10), [])

    def test_already_received_is_skipped(self):
        stages = [stage(55, closed=True)]
        rooms = [room(55, user=10, received=True)]
        self.assertEqual(pending_rewards(stages, rooms, 10), [])

    def test_room_without_quest_id_is_skipped(self):
        stages = [stage(55, closed=True)]
        self.assertEqual(pending_rewards(stages, [room(55, user=10, quest=0)], 10), [])
        self.assertEqual(pending_rewards(stages, [room(55, user=10, quest=None)], 10), [])

    def test_room_without_user_id_is_skipped(self):
        stages = [stage(55, closed=True)]
        self.assertEqual(pending_rewards(stages, [room(55, user=None)], 10), [])

    def test_room_from_an_unknown_stage_is_skipped(self):
        stages = [stage(55, closed=True)]
        rooms = [room(55, user=10, quest=1), room(77, user=10, quest=2)]
        found = pending_rewards(stages, rooms, 10)
        self.assertEqual([r.questDataId for _, r in found], [1])

    def test_rooms_are_returned_with_their_stage(self):
        stages = [stage(55, closed=True, host=20), stage(66, closed=True, host=10)]
        rooms = [room(55, user=10, quest=1), room(66, user=10, quest=2)]
        found = pending_rewards(stages, rooms, 10)
        self.assertEqual([(s.multiRaidStageDataId, r.questDataId) for s, r in found],
                         [(55, 1), (66, 2)])

    def test_skipped_rooms_are_not_returned(self):
        stages = [stage(55, closed=True), stage(66, closed=True)]
        rooms = [room(55, user=10, quest=1), room(66, user=10, quest=2)]
        found = pending_rewards(stages, rooms, 10, skip={1})
        self.assertEqual([r.questDataId for _, r in found], [2])

    def test_skip_accepts_any_iterable(self):
        stages = [stage(55, closed=True)]
        rooms = [room(55, user=10, quest=7)]
        self.assertEqual(pending_rewards(stages, rooms, 10, skip=[7]), [])
        self.assertEqual(pending_rewards(stages, rooms, 10, skip=(7,)), [])

    def test_skip_defaults_to_nothing(self):
        stages = [stage(55, closed=True)]
        rooms = [room(55, user=10, quest=1)]
        self.assertEqual([r.questDataId for _, r in pending_rewards(stages, rooms, 10)], [1])

    def test_skip_is_not_mutated(self):
        stages = [stage(55, closed=True)]
        rooms = [room(55, user=10, quest=1)]
        skip = {9}
        pending_rewards(stages, rooms, 10, skip=skip)
        self.assertEqual(skip, {9})

    def test_room_without_quest_id_is_never_treated_as_skipped(self):
        # questDataId 为 0/None 的房间本来就该被跳过，而不是因为 skip 命中
        stages = [stage(55, closed=True)]
        rooms = [room(55, user=10, quest=None)]
        self.assertEqual(pending_rewards(stages, rooms, 10, skip={None, 0}), [])


if __name__ == "__main__":
    unittest.main()
