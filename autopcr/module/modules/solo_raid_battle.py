"""总力战（Solo Raid）—— 危险页功能。

设置项：
* 难度：easy / normal / hard / very hard / extra / crisis
* 斩杀时机：秒杀 / 中间时间点斩杀 / 最后关头斩杀
* 出战队伍：队伍名或队伍ID
* 战斗日志模式：模拟完整日志 / 极简日志

boss 数据全部从服务端主数据读取，赛季每月月初更换 boss 后会自动更新。
"""

from ..config import *
from ..modulebase import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import ApiException
from ...model.models import *

from raid.soloraidworker import (
    DIFFICULTY_ORDER,
    DIFFICULTY_NAMES,
    get_boss_info,
    get_open_season,
    list_all_boss_info,
    resolve_party_id,
    run_solo_raid_battle,
)

# 选择型配置的候选项：统一用 "值:显示名" 的格式（沿用项目里 wash 模块的写法）
DIFFICULTY_CANDIDATES = [
    f"{d}: {DIFFICULTY_NAMES[d]}" for d in DIFFICULTY_ORDER
]

KILL_TIMING_CANDIDATES = [
    "instant: 秒杀（进本直接斩杀boss）",
    "middle: 中间时间点斩杀boss",
    "last: 最后关头斩杀boss",
]

BATTLE_LOG_MODE_CANDIDATES = [
    "simulate: 模拟完整战斗日志",
    "minimal: 极简日志（最保守）",
]


def _choice_value(raw: str) -> str:
    return str(raw).split(":", 1)[0].strip()


@name('总力战')
@default(False)
# 前端按 config_order 渲染设置项，而 config_order 等于"装饰器自下而上"的顺序，
# 所以这里把最重要的两项放在最下面，界面上它们才会排在最前面。
@booltype('solo_raid_show_all_boss', '显示全部难度的boss数据', False)
@inttype('solo_raid_times', '执行次数', 1, [1, 2, 3, 4, 5])
@singlechoice('solo_raid_battle_log_mode', '战斗日志模式', BATTLE_LOG_MODE_CANDIDATES[0], BATTLE_LOG_MODE_CANDIDATES)
@texttype('solo_raid_party', '出战队伍名/id', '1')
@singlechoice('solo_raid_kill_timing', '斩杀时机', KILL_TIMING_CANDIDATES[0], KILL_TIMING_CANDIDATES)
@singlechoice('solo_raid_difficulty', '难度', DIFFICULTY_CANDIDATES[3], DIFFICULTY_CANDIDATES)
@description('进本直接斩杀总力战boss（危险功能，请自行评估风险）')
class solo_raid_battle(Module):

    async def do_task(self, client: pcrclient):
        # ---- 1. 赛季 / boss 数据（每月自动更新） ----
        season = await get_open_season()
        if season is None:
            raise SkipError("当前没有开放的总力战活动")
        self._log(f"当前总力战赛季：{season.describe()}")

        difficulty = int(_choice_value(self.get_config('solo_raid_difficulty')))
        boss = await get_boss_info(difficulty)
        if boss is None:
            raise SkipError(f"没有找到难度 {DIFFICULTY_NAMES.get(difficulty, difficulty)} 的总力战关卡")
        self._log(f"目标boss：{boss.describe()}")

        if self.get_config('solo_raid_show_all_boss'):
            for info in await list_all_boss_info():
                self._log(f"  {info.describe()}")

        # ---- 2. 队伍 ----
        party_raw = self.get_config('solo_raid_party')
        party_id = await resolve_party_id(client, party_raw)
        if party_id is None:
            raise AbortError(f"队伍 '{party_raw}' 未找到，请检查队伍ID或名称")

        kill_timing = _choice_value(self.get_config('solo_raid_kill_timing'))
        battle_log_mode = _choice_value(self.get_config('solo_raid_battle_log_mode'))

        # ---- 3. 次数 ----
        top = await client.request(SoloRaidApiGetTopRequest())
        max_per_day = client.data.config.soloRaidConfig.maxPlayCountPerDay
        today = top.soloRaidUserData.todayPlayCount
        remain = max(0, max_per_day - today)
        want = int(self.get_config('solo_raid_times'))
        times = min(want, remain)
        if times <= 0:
            raise SkipError(
                f"总力战今日次数已用完（{today}/{max_per_day}）"
            )
        self._log(
            f"今日已打 {today}/{max_per_day} 次，本次执行 {times} 次"
            f"（队伍 {party_id}，斩杀时机 {kill_timing}，日志模式 {battle_log_mode}）"
        )

        # ---- 4. 逐次战斗 ----
        any_high_score = False
        for index in range(times):
            try:
                result = await run_solo_raid_battle(
                    client,
                    difficulty=difficulty,
                    party_data_id=party_id,
                    kill_timing=kill_timing,
                    mode=battle_log_mode,
                )
            except ApiException as e:
                self._log(f"第 {index + 1} 次战斗失败：{e} (code={e.result_code})")
                break

            if not result.success:
                self._log(f"第 {index + 1} 次战斗未胜利：{result.log}")
                continue

            any_high_score = any_high_score or result.high_score_updated
            rest = f"{result.boss_rest_hp:,}" if result.boss_rest_hp else "0"
            self._log(
                f"第 {index + 1} 次战斗成功：得分 {result.score:,}，"
                f"boss剩余血量 {rest}/{result.boss_max_hp:,}"
                + ("（刷新最高分）" if result.high_score_updated else "")
            )

        if any_high_score:
            self._log("本次刷新了最高分")

        # 顺手领取可领的奖励（不额外发请求，仅在日志里提示）
        if top.rewardInfo and (
            top.rewardInfo.clearRewardMstIds or top.rewardInfo.totalScoreRewardMstIds
        ):
            self._log("有可领取的总力战奖励，可前往游戏内领取")
