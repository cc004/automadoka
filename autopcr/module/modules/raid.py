from ..config import *
from ..modulebase import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import ApiException
from ...db.database import db
from ...model.models import *
from ...util.raidoption import (
    parse_raid_difficulty,
    parse_raid_times,
    pending_rewards,
    resolve_battle_result,
)

from raid.raidworker import raidworker

from datetime import datetime, timedelta, timezone

from raid.raidrunner import queue_raid

from ...constants import USER_TZ as user_tz

LP_RECOVER_COUNT = 20


def _room_state(room) -> str:
    """把房间的几个关键状态拼成一行，用来定位「報酬の受け取りに失敗しました」。

    全部走 `getattr` 兜底：协议模型是「代」的惰性代理，字段被新版删掉时这里不应该
    再抛 `ProtocolError`，把真正的错误盖掉。
    """
    names = ('questDataId', 'isClosed', 'result', 'isReceivedReward', 'damage', 'endTime')
    return '，'.join(f'{name}={getattr(room, name, None)}' for name in names)


def _claim_error(error) -> str:
    """领奖失败时的统一后缀：服务端状态码 + `result_code`。"""
    return f" [{getattr(error, 'status', '?')}/{getattr(error, 'result_code', '?')}]"


class RaidLPModule(Module):
    async def do_task(self, client: pcrclient):
        await self.refresh_top(client)
        try:
            max_recovery = min(
                client.data.config.multiRaidConfig.staminaMaxCountInDay,
                self.get_config('raid_recovery_count')
            )
            current_recovery = self.raid_top.multiRaidUserData.recoveryCount
            self.available_recovery_count = max_recovery - current_recovery
            if datetime.now().astimezone(user_tz) > datetime.fromisoformat(
                self.raid_top.multiRaidUserData.recoveryResetTime
            ) + timedelta(days=1):
                self.available_recovery_count = max_recovery
            stamina_count = client.raid_stamina(self.raid_top.multiRaidUserData)

            self._log(f"当前体力 {stamina_count}，可恢复次数 {self.available_recovery_count}，今日已发车次数 {self.raid_top.multiRaidUserSeasonData.todayClearedCount}/{client.data.config.multiRaidConfig.maxPlayCountPerDay}")
        except Exception:
            self._log("该功能不支持体力回复")
            
    async def stamina_recovery(self, client: pcrclient, target: int) -> int:
        if self.available_recovery_count * LP_RECOVER_COUNT <= target:
            self._log(f"今日体力恢复次数不足恢复{target}，无法恢复体力")
            return 0
        await client.request(MultiRaidApiRecoverStaminaRequest(
            num=(target + LP_RECOVER_COUNT - 1) // LP_RECOVER_COUNT,
            itemMstId=290001
        ))
        self._log(f"已恢复体力{(target + LP_RECOVER_COUNT - 1) // LP_RECOVER_COUNT * LP_RECOVER_COUNT}，剩余可恢复次数 {self.available_recovery_count - 1}")
        self.available_recovery_count -= 1
        return LP_RECOVER_COUNT

    async def receive_rewards(self, client: pcrclient) -> bool:
        self._log("开始收取团战奖励")
        any_reward = False
        for stage, raid in pending_rewards(
            self.raid_top.multiRaidStageDataList,
            self.raid_top.multiRaidRoomDataList,
            client.data.resp.userParamData.userId,
        ):
            try:
                await client.request(MultiRaidApiReceiveRewardRequest(
                    questDataId=raid.questDataId
                ))
            except ApiException as error:
                # 单个房间领不了不该把整个模块带停，记一行继续。
                self._log(f"收取团战 {stage.multiRaidStageDataId} "
                          f"(关卡 {stage.multiRaidStageMstId}) 奖励失败：{error}"
                          f"{_claim_error(error)}（{_room_state(raid)}），跳过")
                continue
            self._log(f"已收取团战 {stage.multiRaidStageDataId} (关卡 {stage.multiRaidStageMstId}) 奖励")
            any_reward = True
        
        if any_reward:
            await asyncio.sleep(3) # 等待服务器更新数据

        return any_reward

    async def refresh_top(self, client: pcrclient):
        self.raid_top = await client.request(MultiRaidApiGetTopRequest())

@name('魔女救世')
@default(False)
@texttype('raid_support_account', '小号引继码', '')
@texttype('raid_support_password', '小号密码', '')
@booltype('raid_suppport_ignore_host', '忽略本人为房主的房间', True)
@description('秒掉当前参与的所有团战')
class raid_support(RaidLPModule):
    async def do_task(self, client: pcrclient):
        await super().do_task(client)

        client2 = raidworker(
            self.get_config('raid_support_account'),
            self.get_config('raid_support_password'),
            'Raid Worker',
            client.session.sdk.__class__
        )

        await client2.prepare()
        stamina = await client2.now_stamina()
        
        stamina_cost = {
            stage.multiRaidStageMstId: stage.useStaminaForRescue
            for stage in await db.mst(MstApiGetMultiRaidStageMstListRequest())
        }

        ignore = self.get_config('raid_suppport_ignore_host')
        stage_ids = set(
            raid.multiRaidStageDataId
            for raid in self.raid_top.multiRaidRoomDataList
            if raid.userId == client.data.resp.userParamData.userId
        )
        for raid in self.raid_top.multiRaidStageDataList:
            if not raid.multiRaidStageDataId in stage_ids:
                continue
            if ignore and raid.hostUserId == client.data.resp.userParamData.userId:
                self._log(f"跳过团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 因为是自己开的")
                continue
            if raid.isClosed:
                self._log(f"跳过团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 因为已经结束")
                continue
            cost = stamina_cost[raid.multiRaidStageMstId]
            if stamina < cost:
                self._log(f"体力不足，无法继续秒团战 (当前体力 {stamina}，需要 {cost})")
                break
            stamina -= cost
            await client2.add_damage(raid, raid.hp)
            self._log(f"已秒掉团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) {raid.hp} 伤害 by {raid.hostUserName}")

from autopcr.core.sdkclient import region
import asyncio

@name('魔女舔盒')
@default(True)
@booltype('raid_reward_self_only', '仅收取本人发车的战斗', False)
@description('自动收取团战结算奖励')
class raid_reward(RaidLPModule):
    async def do_task(self, client: pcrclient):
        await super().do_task(client)
        
        self_only = self.get_config('raid_reward_self_only')
        my_id = client.data.resp.userParamData.userId
        any_reward = False

        for stage, raid in pending_rewards(
            self.raid_top.multiRaidStageDataList,
            self.raid_top.multiRaidRoomDataList,
            my_id,
        ):
            if self_only and stage.hostUserId != my_id:
                self._log(f"跳过团战 {stage.multiRaidStageDataId} (关卡 {stage.multiRaidStageMstId}) 因为不是自己开的")
                continue
            try:
                await client.request(MultiRaidApiReceiveRewardRequest(
                    questDataId=raid.questDataId
                ))
            except ApiException as error:
                # 单个房间领不了不该把整个模块带停，记一行继续。
                self._log(f"收取团战 {stage.multiRaidStageDataId} "
                          f"(关卡 {stage.multiRaidStageMstId}) 奖励失败：{error}"
                          f"{_claim_error(error)}（{_room_state(raid)}），跳过")
                continue
            self._log(f"已收取团战 {stage.multiRaidStageDataId} (关卡 {stage.multiRaidStageMstId}) 奖励")
            any_reward = True
        
        if any_reward:
            await asyncio.sleep(3) # 等待服务器更新数据
            

import random

_RAID_RESULT_NAMES = {1: 'win', 2: 'lose', 3: 'timeout'}

@name('魔女召唤')
@default(False)
@texttype('start_raid_damage_min', '伤害下限', '900000')
@texttype('start_raid_damage_max', '伤害上限', '1100000')
@texttype('start_raid_party', '队伍名/id', '30')
@texttype('start_raid_result', '手动战斗结果(1:win, 2:lose, 3:timeout)', '3')
@booltype('start_raid_auto_result', '自动判断战斗结果（这一刀够斩杀就记 win）', True)
@texttype('start_raid_difficulty', '目标难度(1~20，留空=自动打下一档)', '')
@inttype('start_raid_times', '自动召唤次数', 1, [1, 2, 3, 4, 5, 6])
@booltype('start_raid_continue_open', '有未结束的团战时先把它打完', True)
@booltype('start_raid_receive', '发车前自动领取已结束的奖励', True)
@booltype('start_raid_queue', '将召唤后的战斗放入待秒列表中', True)
@inttype('raid_recovery_count', "Raid氪体数", 0, [0, 1, 2, 3])
@description('使用给定伤害记录发车；有未结束的团战会先打完，并自动补领奖励')
class self_raid(RaidLPModule):
    """魔女召唤。

    一次运行按「自动召唤次数」循环，每一轮只处理一件事：

    1. 自己还有没打完的团战 → 接着把它打完（`start_raid_continue_open` 关掉则跳过）
    2. 否则先补领所有已结束未领取的奖励（`start_raid_receive`）
    3. 然后按「目标难度」发一车新的

    战斗结果默认按「这一刀够不够把 boss 打掉」自动判断，不用再手填 1/2/3。
    """

    async def do_task(self, client: pcrclient):
        await super().do_task(client)

        team = self._resolve_team(client)
        damage_min = self._int_config('start_raid_damage_min', 900000)
        damage_max = self._int_config('start_raid_damage_max', 1100000)
        if damage_max < damage_min:
            damage_min, damage_max = damage_max, damage_min
        auto_result = bool(self.get_config('start_raid_auto_result'))
        manual_result = self.get_config('start_raid_result')
        difficulty_raw = self.get_config('start_raid_difficulty')
        times = parse_raid_times(self.get_config('start_raid_times'))
        continue_open = bool(self.get_config('start_raid_continue_open'))
        receive = bool(self.get_config('start_raid_receive'))
        queue = bool(self.get_config('start_raid_queue'))

        opening_raid = await self._opening_raid()
        if opening_raid is None:
            self._log("当前没有开放的团战")
            return

        worker = raidworker.from_client(client, 'Self Raid Worker')

        # 本次运行里被服务端拒掉的补领房间，避免每轮重复请求同一个房间
        self._rejected_rewards = set()
        # 本次运行里自己结算过的房间。**不再补领** —— 见 `_receive_pending` 的说明。
        self._shipped_rooms = set()

        for index in range(times):
            if index:
                self._log(f"—— 第 {index + 1}/{times} 次召唤 ——")
                await self.refresh_top(client)

            # 1) 自己还有没打完的团战：先把它打完
            stage = self._my_open_stage(client)
            if stage is not None:
                if not continue_open:
                    self._log("已经有未结束的团战，无法发车")
                    return
                if not await self._finish_open_raid(
                    client, worker, stage,
                    damage_min, damage_max, auto_result, manual_result, queue
                ):
                    return
                continue

            # 2) 补领所有已结束但没领的奖励
            if receive:
                await self._receive_pending(client)

            # 3) 今日发车次数上限
            season_data = self.raid_top.multiRaidUserSeasonData
            max_play = client.data.config.multiRaidConfig.maxPlayCountPerDay
            if season_data.todayClearedCount >= max_play:
                self._log(f"今日发车次数已达上限 ({season_data.todayClearedCount}/{max_play})，无法发车")
                return

            # 4) 算难度，找关卡
            difficulty, note = parse_raid_difficulty(
                difficulty_raw, season_data.clearedDifficulty
            )
            raid_id = opening_raid.seasonId * 100 + difficulty
            record = next((
                x for x in await db.mst(MstApiGetMultiRaidStageMstListRequest())
                if x.multiRaidStageMstId == raid_id
            ), None)
            if record is None:
                self._log(f"找不到关卡 {raid_id}（{note}）")
                return

            # 5) 体力
            now_stamina = client.raid_stamina(self.raid_top.multiRaidUserData)
            if record.useStaminaForPlay > now_stamina:
                now_stamina += await self.stamina_recovery(
                    client, record.useStaminaForPlay - now_stamina
                )
            if record.useStaminaForPlay > now_stamina:
                self._log(f"体力不足，无法发车 (当前体力 {now_stamina}，需要 {record.useStaminaForPlay})")
                return

            # 6) 开房 → 发伤害 → 结算
            quest_data_id, hp, units = await worker.open_room(raid_id, team, 1)
            damage = random.randint(damage_min, damage_max)
            result = resolve_battle_result(auto_result, manual_result, damage, hp)
            await worker.send_damage(quest_data_id, damage)
            resp = await worker.finalize_room(quest_data_id, units, result)
            self._shipped_rooms.add(quest_data_id)
            self._log(
                f"已发车团战 (关卡 {raid_id}，{note}) {damage} 伤害，"
                f"结果 {result}（{_RAID_RESULT_NAMES.get(result, '未知')}）"
            )
            self._enqueue(queue, client, resp)

    # -- 辅助 --------------------------------------------------------------
    def _int_config(self, key: str, fallback: int) -> int:
        try:
            return int(self.get_config(key))
        except (TypeError, ValueError):
            return fallback

    def _resolve_team(self, client: pcrclient) -> int:
        """把「队伍名/id」解析成 partyDataId。"""
        team = self.get_config('start_raid_party')
        try:
            return int(team)
        except (TypeError, ValueError):
            pass
        parties = client.data.resp.partyDataList or []
        found = next((p.partyDataId for p in parties if p.name == team), None)
        if found is None:
            raise AbortError(f"队伍 '{team}' 未找到，请检查队伍ID或名称。")
        return found

    async def _opening_raid(self):
        """当前开放中的团战赛季；没有就返回 None。"""
        now = datetime.now(timezone.utc).astimezone(user_tz)
        for row in await db.mst(MstApiGetMultiRaidMstListRequest()):
            try:
                start = datetime.fromisoformat(row.startTime).astimezone(user_tz)
                end = datetime.fromisoformat(row.endTime).astimezone(user_tz)
            except (TypeError, ValueError):
                continue
            if start <= now <= end:
                return row
        return None

    def _my_open_stage(self, client: pcrclient):
        """自己发车、还没结束的那一场；没有就返回 None。"""
        my_id = client.data.resp.userParamData.userId
        return next((
            stage for stage in self.raid_top.multiRaidStageDataList
            if not stage.isClosed and stage.hostUserId == my_id
        ), None)

    def _my_room(self, client: pcrclient, stage):
        """自己那场未结束团战对应的房间。"""
        my_id = client.data.resp.userParamData.userId
        return next((
            room for room in self.raid_top.multiRaidRoomDataList
            if room.multiRaidStageDataId == stage.multiRaidStageDataId
            and room.userId == my_id
            and room.questDataId
        ), None)

    def _enqueue(self, queue: bool, client: pcrclient, resp) -> None:
        """打完之后如果 boss 还有血，就丢进待秒列表。"""
        stage = resp.multiRaidStageData
        if queue and stage is not None and not stage.isClosed and stage.hp > 0:
            queue_raid(stage, client.session.sdk.region)

    async def _finish_open_raid(self, client, worker, stage, damage_min, damage_max,
                                auto_result, manual_result, queue) -> bool:
        """把上一场没打完的团战接着打完，成功返回 True。"""
        room = self._my_room(client, stage)
        if room is None:
            self._log(f"团战 {stage.multiRaidStageDataId} 未结束，但读不到房间编号，跳过")
            return False
        hp, units = await worker.sync_room(room.questDataId)
        damage = random.randint(damage_min, damage_max)
        result = resolve_battle_result(auto_result, manual_result, damage, hp)
        await worker.send_damage(room.questDataId, damage)
        resp = await worker.finalize_room(room.questDataId, units, result)
        self._shipped_rooms.add(room.questDataId)
        self._log(
            f"已把未结束的团战打完 (关卡 {stage.multiRaidStageMstId}，剩余 {hp}) "
            f"{damage} 伤害，结果 {result}（{_RAID_RESULT_NAMES.get(result, '未知')}）"
        )
        self._enqueue(queue, client, resp)
        return True

    async def _receive_pending(self, client: pcrclient) -> int:
        """把已结束但还没领奖的、**自己**的房间全部补领掉，返回领到的个数。

        `multiRaidRoomDataList` 里含别人的房间，领别人的会被服务端拒掉
        （「報酬の受け取りに失敗しました。」），所以按 `userId` 过滤。

        ⚠️ **本次运行自己结算过的房间（`_shipped_rooms`）不补领**：
        打赢的 `finalize_stage_for_user` 可能**已经把奖励发掉了**，之后
        `get_top` 里那个房间却还挂着 `isReceivedReward=False`，再领一次就是重复领取，
        服务端回「報酬の受け取りに失敗しました。」。RustMadoka 在
        `group_public.rs:945-947` 明确记过这一点（"Winning finalize may already
        grant the reward and remove that quest from the pending list"），
        它的做法是领奖前重读一次 `get_top`、房间不在待领列表里就跳过。
        我们的对应做法更简单：自己刚结算的房间直接跳过，留到下一次运行
        （或「魔女舔盒」）再领 —— 上游 autopcr 和 RustMadoka 也都只在
        **一次运行的开始**补领，从不领自己几秒前刚打完的房间。

        被拒的房间记进 `_rejected_rewards`，本次运行不再重试 —— 服务端在一次运行
        内不会改口，重复请求只是白跑 + 刷日志。
        """
        claimed = 0
        for stage, room in pending_rewards(
            self.raid_top.multiRaidStageDataList,
            self.raid_top.multiRaidRoomDataList,
            client.data.resp.userParamData.userId,
            skip=self._rejected_rewards | self._shipped_rooms,
        ):
            try:
                await client.request(MultiRaidApiReceiveRewardRequest(
                    questDataId=room.questDataId
                ))
            except ApiException as error:
                # 单个房间领不了不该把整轮召唤带停，记下来继续。
                self._rejected_rewards.add(room.questDataId)
                self._log(
                    f"补领团战 {stage.multiRaidStageDataId} "
                    f"(关卡 {stage.multiRaidStageMstId}) 失败：{error}"
                    f"{_claim_error(error)}"
                    f"（{_room_state(room)}，stageHp={getattr(stage, 'hp', None)}），"
                    f"本次运行不再重试"
                )
                continue
            self._log(f"已补领团战 {stage.multiRaidStageDataId} (关卡 {stage.multiRaidStageMstId}) 奖励")
            claimed += 1
        if claimed:
            await asyncio.sleep(3)  # 等服务器更新数据
        return claimed

@name('魔女援助')
@default(False)
@texttype('support_raid_damage_min', '伤害下限', '900000')
@texttype('support_raid_damage_max', '伤害上限', '1100000')
@texttype('support_raid_id', '关卡id（逗号分隔）', '120')
@texttype('support_raid_party', '队伍名/id', '30')
@texttype('support_raid_result', '战斗结果(1:win, 2:lose, 3:timeout)', '3')
@texttype('support_raid_max', '不超过多少人时进入战斗', '2')
@texttype('support_raid_time_max', '剩余多少分钟内进入战斗', '10')
@booltype('support_guild', '同时支援公会内的团战', True)
@inttype('support_search_times', '搜索列表内的团战次数', 0, [0, 1, 2, 3])
@booltype('support_queue', '将支援后的战斗放入待秒列表中', True)
@inttype('raid_recovery_count', "Raid氪体数", 0, [0, 1, 2, 3])
@description('查询团战池内的团战并进行支援（十分钟内的）')
class support_raid(RaidLPModule):

    async def do_task(self, client: pcrclient):
        await super().do_task(client)
        raid_id = set(
            int(x) % 100 for x in self.get_config('support_raid_id').split(',')
        )
        raid_damage = random.randint(
            int(self.get_config('support_raid_damage_min')),
            int(self.get_config('support_raid_damage_max'))
        )
        raid_result = int(self.get_config('support_raid_result'))
        team = self.get_config('support_raid_party')
        time_max = int(self.get_config('support_raid_time_max'))

        try:
            team = int(team)
        except ValueError:
            parties = client.data.resp.partyDataList
            team = next((party.partyDataId for party in parties if party.name == team), None)
        
        if team is None:
            raise AbortError(f"队伍 '{team}' 未找到，请检查队伍ID或名称。")
        
        times = self.get_config('support_search_times')
        if times == 0 and not self.get_config('support_guild'):
            self._log(f"团战池内没有可支援的团战")
            return
        
        now_time = datetime.now(user_tz)
        threshold = now_time - timedelta(minutes=time_max)

        max_num = int(self.get_config('support_raid_max'))

        client2 = raidworker.from_client(client, 'Self Raid Worker')
        stamina = client.raid_stamina(self.raid_top.multiRaidUserData)

        async def raid_iter():
            if self.get_config('support_guild'):
                for raid in self.raid_top.multiRaidStageDataList:
                    if raid.isClosed: continue
                    yield raid, [
                        r.userId for r in self.raid_top.multiRaidRoomDataList
                        if r.multiRaidStageDataId == raid.multiRaidStageDataId
                    ]
            for i in range(times):
                raid_search = await client.request(MultiRaidApiGetMultiRaidStageDataListRequest(
                    isRescue=True
                ))
                await asyncio.sleep(3)
                for raid in raid_search.multiRaidStageDataList:
                    if raid.isClosed: continue
                    yield raid, [
                        r.userId for r in raid_search.multiRaidRoomDataList
                        if r.multiRaidStageDataId == raid.multiRaidStageDataId
                    ]

        async def distincted_raid():
            seen = set()
            async for raid, user_list in raid_iter():
                if raid.multiRaidStageDataId not in seen:
                    seen.add(raid.multiRaidStageDataId)
                    yield raid, user_list


        attending = len(self.raid_top.multiRaidRoomDataList)

        async for raid, user_list in distincted_raid():
            
            if len(user_list) > max_num or len(user_list) >= client.data.config.multiRaidConfig.maxJoinUserCount:
                self._log(f"跳过团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 因为已经有 {user_list} 人支援")
                continue

            if client.data.resp.userParamData.userId in user_list:
                self._log(f"跳过团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 因为已经支援过了")
                continue

            if raid.multiRaidStageMstId % 100 not in raid_id:
                self._log(f"跳过团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 因为关卡ID不符")
                continue
        
            if datetime.fromisoformat(raid.createdTime).astimezone(user_tz) < threshold:
                self._log(f"跳过团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 因为已经超过10分钟")
                continue
            
            record = next(
                x for x in 
                await db.mst(MstApiGetMultiRaidStageMstListRequest())
                if x.multiRaidStageMstId == raid.multiRaidStageMstId
            )

            if not record:
                self._log(f"找不到关卡 {raid_id}")
                return
            
            if attending >= client.data.config.multiRaidConfig.maxJoinRoomCount:
                self._log(f"支援人数已达上限，尝试进行收取 (当前支援数 {attending})")

                await asyncio.sleep(3)
                await self.refresh_top(client)
                
                any_reward = await self.receive_rewards(client)

                if any_reward:
                    await self.refresh_top(client)
                    attending = len(self.raid_top.multiRaidRoomDataList)
                    self._log(f"收取完成，当前支援数 {attending}")
                else:
                    self._log(f"没有可收取的奖励，停止支援")
                    return

            if record.useStaminaForRescue > stamina:
                stamina += await self.stamina_recovery(client, record.useStaminaForRescue - stamina)
            
            if record.useStaminaForRescue > stamina:
                self._log(f"体力不足，无法支援 (当前体力 {stamina}，需要 {record.useStaminaForRescue})")
                return
        
            try:
                _, _, resp = await client2.support_clear(raid, team, 0, raid_damage, raid_result)
            except ApiException as e:
                self._log(f"支援团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 失败: {str(e)} (code={e.result_code})")
                continue

            stamina -= record.useStaminaForRescue

            if resp.multiRaidStageData.isClosed or resp.multiRaidStageData.hp <= 0:
                self._log(f"已支援并结束团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) {raid_damage} 伤害 by {raid.hostUserName} 当前体力 {stamina}")
            else:
                self._log(f"已支援团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) {raid_damage} 伤害 by {raid.hostUserName} 当前体力 {stamina}")
                attending += 1

            if self.get_config('support_queue'):
                queue_raid(resp.multiRaidStageData, client.session.sdk.region)

@name('魔女点赞')
@inttype('search_times', '搜索列表内的团战次数', 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
@default(True)
class like_raid(Module):
    """给团战池里的其他参与者点赞，换好友勋章。

    和上游相比改了三处（前两处对齐 RustMadoka 的 `run_link_like`）：

    1. **跳过 `isLiked` 已经是 true 的人**。服务端已经在 `joinUserInfoList` 里
       标好了，再点一次只会回 `result=false`；上游没看这个字段，于是重复点赞既
       拿不到勋章、又不打任何日志，看起来就是「点赞失效」。
    2. **勋章数按响应实时读**，不再用登录快照。`todayFriendMedalCount` 由
       `handlers.py` 里 `LikeApiExecLikeListResponse.update` 在每次点赞后累加，
       上游把它缓存在循环外，导致「勋章已满」永远不会触发。
    3. **一条赞都没点出去时给一行日志**。上游在这种情况下完全静默，
       分不清「没有可点的目标」还是「模块挂了」。
    """

    async def do_task(self, client: pcrclient):
        times = self.get_config('search_times')
        my_id = client.data.resp.userParamData.userId
        max_num = client.data.config.friendConfig.gainTodayFriendMedalMaxNum

        def medals() -> int:
            return client.data.resp.userParamData.todayFriendMedalCount or 0

        if medals() >= max_num:
            self._log(f"好友勋章已满 ({medals()}/{max_num})，无法继续点赞")
            return

        liked = set()      # 本次运行已经点过的 (用户, 房间)
        already = 0        # 服务端标记为已点赞、直接跳过的条数
        accepted = 0       # 服务端确认接受的条数

        for _ in range(times):
            raid_search = await client.request(MultiRaidApiGetMultiRaidStageDataListRequest(
                isRescue=True
            ))
            await asyncio.sleep(3)

            for user in raid_search.joinUserInfoList or []:
                if not user.userId or user.userId == my_id or not user.multiRaidStageDataId:
                    continue

                key = (user.userId, user.multiRaidStageDataId)
                if key in liked:
                    continue
                liked.add(key)

                if user.isLiked:
                    already += 1
                    continue

                res = await client.request(LikeApiExecLikeListRequest(
                    targetUserIdList=[user.userId],
                    value=user.multiRaidStageDataId
                ))

                for item in res.resultList or []:
                    if item.targetUserId != user.userId:
                        continue

                    if item.result:
                        accepted += 1
                        self._log(
                            f"已点赞用户 {user.userName} "
                            f"(关卡 {user.multiRaidStageDataId}) "
                            f"({medals()}/{max_num})"
                        )

                    if medals() >= max_num:
                        self._log(f"好友勋章已满 ({medals()}/{max_num})，无法继续点赞")
                        return

        if accepted == 0:
            if already:
                self._log(f"没有可点赞的团战参与者（{already} 条服务端已标记为已点赞）")
            else:
                self._log("没有可点赞的团战参与者")
