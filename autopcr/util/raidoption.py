"""魔女（团战）相关的纯逻辑：难度选择、战斗结果判定、召唤次数解析、可领奖房间筛选、
点赞勋章折算。

抽到 `autopcr/util/` 下是为了能离线测试 —— 模块本体在 `autopcr.module.modules`
包里，导入它会连带 `raid/raidrunner.py`，而后者在模块顶层 `open('raid_config.json')`，
这个文件在 `.gitignore` 里、干净仓库上没有。

难度与结果的取值都对齐服务端：

* 团战难度 1 ~ 20（`multiRaidStageMstId` 的低两位）
* 战斗结果 1 = win、2 = lose、3 = timeout
"""

from typing import Optional, Tuple

# 团战难度范围（对应 multiRaidStageMstId 的低两位）
RAID_DIFFICULTY_MIN = 1
RAID_DIFFICULTY_MAX = 20

# 一次运行最多召唤几次
RAID_TIMES_MIN = 1
RAID_TIMES_MAX = 6

# 战斗结果（与服务端 MultiRaidApiFinalizeStageForUserRequest.result 一致）
RAID_RESULT_WIN = 1
RAID_RESULT_LOSE = 2
RAID_RESULT_TIMEOUT = 3
RAID_RESULTS = (RAID_RESULT_WIN, RAID_RESULT_LOSE, RAID_RESULT_TIMEOUT)

# 难度设置留空（或填 0、填非数字）时的说明文案
AUTO_DIFFICULTY_NOTE = "自动（已通关 +1）"

# `friendConfig.friendMedal` 里「点赞给勋章」那一行的 type 值
EXEC_LIKE_MEDAL_TYPE = 'ExecLike'


def medal_per_like(medals) -> int:
    """从 `friendConfig.friendMedal` 里取「点赞一次给几个好友勋章」，取不到返回 0。

    返回 0 表示「配置里没有 `ExecLike` 这一行」—— 调用方必须据此**跳过计数**，
    不能让它变成异常。原来这里写的是 `next(...)` 且**没给默认值**，配置一变就抛
    `StopIteration`；`StopIteration` 从协程里逃出来会被 CPython 转成
    `RuntimeError: coroutine raised StopIteration`，直接把「魔女点赞」整个打挂
    （`datamgr.request` 里 `await resp.update(...)` 是在请求链路中间的）。

    ⚠️ 字段名要按 `by_alias=True` 取：生成缓存里这个字段可能叫 `type_`
    （`type` 是 Python 内建名），序列化回别名才是 `type`。
    """
    for medal in medals or []:
        if medal.dict(by_alias=True).get('type') == EXEC_LIKE_MEDAL_TYPE:
            return int(medal.num or 0)
    return 0


def pending_rewards(stages, rooms, my_id, skip=()):
    """挑出「已经结束、属于自己、还没领奖」的房间，返回 ``[(关卡, 房间)]``。

    ⚠️ ``multiRaidRoomDataList`` **里含别人的房间** —— 同一场团战每个参战者各有一条
    记录。RustMadoka 的抓包样本里，关卡 55 下同时存在 ``userId: 20`` 和 ``userId: 10``
    两条。``questDataId`` 是绑在自己身上的，拿别人的去领必然被服务端拒掉
    （「報酬の受け取りに失敗しました。」），所以 ``userId`` 这个过滤不能省。

    另外 ``stages`` 里可能没有房间对应的关卡，那种房间直接跳过（不能 `[]` 取，
    会 KeyError）。

    ``skip`` 里放本轮**已经被服务端拒掉**的 ``questDataId``：服务端在本次运行内
    不会改口，同一个房间每轮再试一遍只是白跑请求 + 刷日志，所以调用方攒下来传进来。
    """
    stage_map = {stage.multiRaidStageDataId: stage for stage in stages}
    skipped = set(skip or ())
    found = []
    for room in rooms:
        if room.questDataId and room.questDataId in skipped:
            continue
        stage = stage_map.get(room.multiRaidStageDataId)
        if stage is None or not stage.isClosed:
            continue
        if room.userId != my_id or room.isReceivedReward or not room.questDataId:
            continue
        found.append((stage, room))
    return found


def highest_unlocked_difficulty(cleared_difficulty: Optional[int]) -> int:
    """当前已通关难度的下一档；到顶就停在 20。"""
    cleared = int(cleared_difficulty or 0)
    return max(RAID_DIFFICULTY_MIN, min(RAID_DIFFICULTY_MAX, cleared + 1))


def parse_raid_difficulty(
    raw: Optional[str], cleared_difficulty: Optional[int]
) -> Tuple[int, str]:
    """把「目标难度」设置解析成实际要打的难度，返回 ``(难度, 说明)``。

    * 留空 / 填 0 / 填了非数字 → 退回「自动打下一档」
    * 超出 1~20 → 夹到边界，说明里写明原值
    * 正常数值 → 原样使用
    """
    fallback = highest_unlocked_difficulty(cleared_difficulty)
    text = str(raw or "").strip()
    if not text:
        return fallback, AUTO_DIFFICULTY_NOTE
    try:
        value = int(text)
    except (TypeError, ValueError):
        return fallback, AUTO_DIFFICULTY_NOTE
    if value <= 0:
        return fallback, AUTO_DIFFICULTY_NOTE
    clamped = max(RAID_DIFFICULTY_MIN, min(RAID_DIFFICULTY_MAX, value))
    if clamped != value:
        return clamped, f"指定 Lv.{value}，已夹到 Lv.{clamped}"
    return clamped, f"指定 Lv.{clamped}"


def resolve_battle_result(
    auto: bool, manual_result: Optional[int], damage: int, hp: int
) -> int:
    """决定上报给服务端的战斗结果。

    ``auto`` 为真时按「这一刀够不够把 boss 打掉」判断：够就是 win，不够就是
    timeout（和 RustMadoka 的 `finish_open_raid` 同一套规则）。boss 已经没血了
    （``hp <= 0``）不算 win —— 那种房间本来就该是已结束状态。
    """
    if auto:
        remaining = max(0, int(hp or 0))
        return (
            RAID_RESULT_WIN
            if remaining > 0 and int(damage) >= remaining
            else RAID_RESULT_TIMEOUT
        )
    try:
        value = int(manual_result)
    except (TypeError, ValueError):
        return RAID_RESULT_TIMEOUT
    return value if value in RAID_RESULTS else RAID_RESULT_TIMEOUT


def parse_raid_times(raw) -> int:
    """自动召唤次数，夹到 1~6；填错就退回 1 次。"""
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError):
        return RAID_TIMES_MIN
    return max(RAID_TIMES_MIN, min(RAID_TIMES_MAX, value))
