"""隐藏队伍模块的离线测试（不依赖网络与账号）。

重点锁住两件事：

1. ``save_option`` 是**整体替换**，必须读回全量配置再写回。
   一旦有人图省事只提交三个开关，其余设置会被写成 ``null``。
2. 战力门槛的边界值。

只导入 ``autopcr.util.useroption`` 与 ``raid.soloraidworker``：
``autopcr.module.modules`` 在导入时会读 ``raid_config.json``，而该文件在
``.gitignore`` 里，全新克隆上没有，导入会直接失败。纯逻辑放在 util 里
就是为了让测试能在干净仓库上跑起来。
"""
import unittest
from types import SimpleNamespace

from autopcr.model.requests import UserApiSaveOptionRequest
from autopcr.model.responses import UserApiLoadOptionResponse

from autopcr.util.useroption import (
    PUBLISH_MULTI_RAID,
    PUBLISH_SCORE_ATTACK,
    PUBLISH_SOLO_RAID,
    build_option_payload,
)

from raid.soloraidworker import (
    MIN_PARTY_POWER,
    POWER_NOT_ENOUGH_MESSAGE,
    build_difficulty_candidates,
    check_party_power,
    format_power,
    get_party_power,
)


def make_options():
    """造一份"当前设置"：三个展示开关都开着，另有几个字段用来验证不被清掉。"""
    options = UserApiLoadOptionResponse()
    options.paymentAlert = True
    options.battleAuto = 1
    options.battleSpeedType = 3
    options.questPartyDataId = 5
    options.characterHeartPartyDataId = 13
    options.multiRaidLikeAll = True
    options.savedOnce = True
    # pydantic v1 的 BaseModel 不支持 obj[key] = v，只能 setattr
    setattr(options, PUBLISH_SOLO_RAID, True)
    setattr(options, PUBLISH_MULTI_RAID, True)
    setattr(options, PUBLISH_SCORE_ATTACK, True)
    return options


class SaveOptionPayloadTests(unittest.TestCase):
    def test_partial_request_would_null_everything_else(self):
        """反例：只提交一个开关时，其余 39 个字段会变成 None。

        这正是不能"只发三个开关"的原因——apiclient 用的是
        ``req.dict(by_alias=True)``，没有 exclude_none。
        """
        body = UserApiSaveOptionRequest(**{PUBLISH_SOLO_RAID: False}).dict(
            by_alias=True
        )
        self.assertEqual(len(body), 42)
        self.assertEqual(body[PUBLISH_SOLO_RAID], False)
        nulls = [k for k, v in body.items() if v is None]
        # 40 个业务字段里只有 1 个被赋值，其余全为 None
        self.assertEqual(len(nulls), 39)

    def test_full_payload_round_trip_keeps_everything_else(self):
        current = make_options()
        data, changed = build_option_payload(current.dict())

        # 只有三个开关被改动，其余字段原样保留
        self.assertEqual(set(data), set(current.dict()))
        for key, value in current.dict().items():
            if key.startswith("characterBuildDetailPublish"):
                self.assertFalse(data[key])
            else:
                self.assertEqual(data[key], value, key)

        self.assertCountEqual(changed, ["总力战", "团战", "打分"])

        # 写回的请求是完整 42 个字段，没有把设置清空
        body = UserApiSaveOptionRequest(**data).dict(by_alias=True)
        self.assertEqual(len(body), 42)
        self.assertEqual(body[PUBLISH_SOLO_RAID], False)
        self.assertEqual(body[PUBLISH_MULTI_RAID], False)
        self.assertEqual(body[PUBLISH_SCORE_ATTACK], False)
        self.assertEqual(body["paymentAlert"], True)
        self.assertEqual(body["battleSpeedType"], 3)
        self.assertEqual(body["questPartyDataId"], 5)
        self.assertEqual(body["multiRaidLikeAll"], True)
        self.assertEqual(
            UserApiSaveOptionRequest(**data).url, "/api/user/save_option"
        )

    def test_only_solo_raid_when_extra_switches_off(self):
        current = make_options()
        data, changed = build_option_payload(
            current.dict(), hide_multi_raid=False, hide_score_attack=False
        )
        self.assertEqual(changed, ["总力战"])
        self.assertFalse(data[PUBLISH_SOLO_RAID])
        self.assertTrue(data[PUBLISH_MULTI_RAID])
        self.assertTrue(data[PUBLISH_SCORE_ATTACK])

    def test_changed_list_is_empty_when_already_hidden(self):
        """已经是关闭状态时不重复上报，changed 为空。"""
        current = make_options()
        setattr(current, PUBLISH_SOLO_RAID, False)
        setattr(current, PUBLISH_MULTI_RAID, False)
        setattr(current, PUBLISH_SCORE_ATTACK, False)
        data, changed = build_option_payload(current.dict())
        self.assertEqual(changed, [])
        self.assertFalse(data[PUBLISH_SOLO_RAID])
        self.assertFalse(data[PUBLISH_MULTI_RAID])
        self.assertFalse(data[PUBLISH_SCORE_ATTACK])

    def test_payload_is_a_copy(self):
        """不要原地改传入的 dict。"""
        current = make_options().dict()
        before = dict(current)
        build_option_payload(current)
        self.assertEqual(current, before)


class PartyPowerTests(unittest.TestCase):
    def test_thresholds(self):
        self.assertEqual(MIN_PARTY_POWER, {4: 60000, 5: 70000, 6: 80000})

    def test_boundary_is_inclusive(self):
        """刚好达到门槛算通过，差 1 点就拒绝。"""
        for difficulty, required in MIN_PARTY_POWER.items():
            with self.subTest(difficulty=difficulty):
                self.assertIsNone(check_party_power(difficulty, required))
                self.assertIsNone(check_party_power(difficulty, required + 100))
                self.assertEqual(
                    check_party_power(difficulty, required - 1),
                    (required - 1, required),
                )

    def test_easy_difficulties_have_no_threshold(self):
        for difficulty in (1, 2, 3):
            with self.subTest(difficulty=difficulty):
                self.assertIsNone(check_party_power(difficulty, 0))

    def test_format_power_uses_wan_for_round_ten_thousands(self):
        self.assertEqual(format_power(60000), "6万")
        self.assertEqual(format_power(70000), "7万")
        self.assertEqual(format_power(80000), "8万")
        self.assertEqual(format_power(100000), "10万")

    def test_format_power_falls_back_to_thousands_separator(self):
        """不是整万时不要瞎凑，直接给精确数字。"""
        self.assertEqual(format_power(9999), "9,999")
        self.assertEqual(format_power(58320), "58,320")
        self.assertEqual(format_power(0), "0")

    def test_get_party_power_reads_party_list(self):
        client = SimpleNamespace(
            data=SimpleNamespace(
                resp=SimpleNamespace(
                    partyDataList=[
                        SimpleNamespace(partyDataId=1, partyPower=42310),
                        SimpleNamespace(partyDataId=5, partyPower=78100),
                        SimpleNamespace(partyDataId=9, partyPower=None),
                    ]
                )
            )
        )
        self.assertEqual(get_party_power(client, 1), 42310)
        self.assertEqual(get_party_power(client, 5), 78100)
        # 战力字段为空时按 0 处理
        self.assertEqual(get_party_power(client, 9), 0)
        # 找不到队伍时按 0 处理
        self.assertEqual(get_party_power(client, 404), 0)

    def test_get_party_power_tolerates_missing_party_list(self):
        client = SimpleNamespace(
            data=SimpleNamespace(resp=SimpleNamespace(partyDataList=None))
        )
        self.assertEqual(get_party_power(client, 1), 0)

    def test_message_is_the_agreed_wording(self):
        self.assertEqual(
            POWER_NOT_ENOUGH_MESSAGE,
            "xdx，战力不够容易被别人看出开挂，请到达战力标准再使用",
        )


class DifficultyLabelTests(unittest.TestCase):
    def test_high_difficulties_show_required_power(self):
        labels = {c.split(":", 1)[0]: c.split(":", 1)[1].strip()
                  for c in build_difficulty_candidates()}
        self.assertEqual(labels["1"], "easy")
        self.assertEqual(labels["2"], "normal")
        self.assertEqual(labels["3"], "hard")
        self.assertEqual(labels["4"], "very hard（需战力 6万）")
        self.assertEqual(labels["5"], "extra（需战力 7万）")
        self.assertEqual(labels["6"], "crisis（需战力 8万）")

    def test_first_colon_split_still_yields_numeric_value(self):
        """候选项是 "值:显示名"，显示名里带括号不能影响取值。"""
        for candidate in build_difficulty_candidates():
            value = candidate.split(":", 1)[0].strip()
            self.assertTrue(value.isdigit(), candidate)


if __name__ == "__main__":
    unittest.main()
