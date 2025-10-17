from ..config import *
from ..modulebase import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import ApiException
from ...db.database import db
from ...model.models import *

from raid.raidworker import raidworker

from datetime import datetime, timedelta, timezone

from raid.raidrunner import queue_raid

from ...constants import USER_TZ as user_tz

LP_RECOVER_COUNT = 20

class RaidLPModule(Module):
    async def do_task(self, client: pcrclient):
        self.raid_top = await client.request(MultiRaidApiGetTopRequest())
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
        stage_map = {
            raid.multiRaidStageDataId: raid
            for raid in self.raid_top.multiRaidStageDataList
        }

        any_reward = False

        for raid in self.raid_top.multiRaidRoomDataList:
            stage = stage_map[raid.multiRaidStageDataId]
            if not stage.isClosed:
                self._log(f"跳过团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 因为未结束")
                continue
            if self_only and stage.hostUserId != client.data.resp.userParamData.userId:
                self._log(f"跳过团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 因为不是自己开的")
                continue
            await client.request(MultiRaidApiReceiveRewardRequest(
                questDataId=raid.questDataId
            ))
            self._log(f"已收取团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 奖励")
            any_reward = True
        
        if any_reward:
            await asyncio.sleep(3) # 等待服务器更新数据
            

import random

@name('魔女召唤')
@default(False)
@texttype('start_raid_log', '战斗日志', '')
@texttype('start_raid_damage_min', '伤害下限', '900000')
@texttype('start_raid_damage_max', '伤害上限', '1100000')
@texttype('start_raid_id', '关卡id', '120')
@texttype('start_raid_party', '队伍名/id', '30')
@texttype('start_raid_result', '战斗结果(1:win, 2:lose, 3:timeout)', '3')
@booltype('start_raid_receive', '如果上一奖励未领取导致无法发车，则自动领取', True)
@booltype('start_raid_queue', '将召唤后的战斗放入待秒列表中', True)
@inttype('raid_recovery_count', "Raid氪体数", 0, [0, 1, 2, 3])
@description('使用给定伤害记录发车')
class self_raid(RaidLPModule):

    def config_string(self) -> str:
        return '\n'.join([
            f"{self.config[key].desc}: {self.get_config_str(key)}" for key in self.config
            if key != 'start_raid_log'
            ])
    
    async def do_task(self, client: pcrclient):
        await super().do_task(client)

        raid_id = int(self.get_config('start_raid_id'))
        raid_damage = random.randint(
            int(self.get_config('start_raid_damage_min')),
            int(self.get_config('start_raid_damage_max'))
        )
        log = self.get_config('start_raid_log')
        raid_result = int(self.get_config('start_raid_result'))
        team = self.get_config('start_raid_party')
        receive = self.get_config('start_raid_receive')

        try:
            team = int(team)
        except ValueError:
            parties = client.data.resp.partyDataList
            team = next((party.partyDataId for party in parties if party.name == team), None)
        
        if team is None:
            raise AbortError(f"队伍 '{team}' 未找到，请检查队伍ID或名称。")
        
        record = next(
            x for x in 
            await db.mst(MstApiGetMultiRaidStageMstListRequest())
            if x.multiRaidStageMstId == raid_id
        )

        if not record:
            self._log(f"找不到关卡 {raid_id}")
            return
        
        for raid in self.raid_top.multiRaidStageDataList:
            if raid.hostUserId == client.data.resp.userData.userId:
                if raid.isClosed and receive:
                    my_quest = next(
                        r for r in self.raid_top.multiRaidRoomDataList
                        if r.multiRaidStageDataId == raid.multiRaidStageDataId
                        and r.userId == client.data.resp.userParamData.userId
                    )
                    await client.request(MultiRaidApiReceiveRewardRequest(
                        questDataId=my_quest.questDataId
                    ))
                    self._log(f"已收取团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 奖励")
                else:
                    self._log(f"已经有未结束的团战，无法发车")
                    return
        
        if self.raid_top.multiRaidUserSeasonData.todayClearedCount >= client.data.config.multiRaidConfig.maxPlayCountPerDay:
            self._log(f"今日发车次数已达上限，无法发车")
            return

        client2 = raidworker.from_client(client, 'Self Raid Worker')

        now_stamina = client.raid_stamina(self.raid_top.multiRaidUserData)
        
        if record.useStaminaForPlay > now_stamina:
            now_stamina += await self.stamina_recovery(client, record.useStaminaForPlay - now_stamina)
        
        if record.useStaminaForPlay > now_stamina:
            self._log(f"体力不足，无法发车 (当前体力 {now_stamina}，需要 {record.useStaminaForPlay})")
            return
        
        _, _, resp = await client2.start_clear(raid_id, team, 2, 0, raid_damage, log, raid_result)
        
        self._log(f"已发车团战 (关卡 {raid_id}) {raid_damage} 伤害")
        if not resp.multiRaidStageData.isClosed and resp.multiRaidStageData.hp > 0:
            if self.get_config('start_raid_queue'):
                queue_raid(resp.multiRaidStageData, client.session.sdk.region)

@name('魔女援助')
@default(False)
@texttype('support_raid_log', '战斗日志', '')
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

    def config_string(self) -> str:
        return '\n'.join([
            f"{self.config[key].desc}: {self.get_config_str(key)}" for key in self.config
            if key != 'support_raid_log'
            ])
    
    async def do_task(self, client: pcrclient):
        await super().do_task(client)
        raid_id = set(
            int(x) for x in self.get_config('support_raid_id').split(',')
        )
        raid_damage = random.randint(
            int(self.get_config('support_raid_damage_min')),
            int(self.get_config('support_raid_damage_max'))
        )
        log = self.get_config('support_raid_log')
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
        stamina = await client2.now_stamina()

        async def raid_iter():
            if self.get_config('support_guild'):
                for raid in self.raid_top.multiRaidStageDataList:
                    if raid.isClosed: continue
                    yield raid, [
                        r.userId for r in self.raid_top.multiRaidRoomDataList
                        if r.multiRaidStageDataId == raid.multiRaidStageDataId
                    ]
            for i in range(times):
                if i > 0:
                    await asyncio.sleep(3)
                raid_search = await client.request(MultiRaidApiGetMultiRaidStageDataListRequest(
                    isRescue=True
                ))
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

        async for raid, user_list in distincted_raid():
            
            if len(user_list) > max_num or len(user_list) >= client.data.config.multiRaidConfig.maxJoinUserCount:
                self._log(f"跳过团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 因为已经有 {user_list} 人支援")
                continue

            if client.data.resp.userParamData.userId in user_list:
                self._log(f"跳过团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 因为已经支援过了")
                continue

            if raid.multiRaidStageMstId not in raid_id:
                self._log(f"跳过团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 因为关卡ID不符")
                continue
        
            if datetime.fromisoformat(raid.createdTime).astimezone(user_tz) < threshold:
                self._log(f"跳过团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 因为已经超过10分钟")
                continue
            
            record = next(
                x for x in 
                await db.mst(MstApiGetMultiRaidStageMstListRequest())
                if x.multiRaidStageMstId in raid_id
            )

            if not record:
                self._log(f"找不到关卡 {raid_id}")
                return
            
            if record.useStaminaForRescue > stamina:
                stamina += await self.stamina_recovery(client, record.useStaminaForRescue - stamina)
            
            if record.useStaminaForRescue > stamina:
                self._log(f"体力不足，无法支援 (当前体力 {stamina}，需要 {record.useStaminaForRescue})")
                return
        
            try:
                _, _, resp = await client2.support_clear(raid, team, 0, raid_damage, log, raid_result)
            except ApiException as e:
                self._log(f"支援团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) 失败: {str(e)} (code={e.result_code})")
                continue
            if resp.multiRaidStageData.isClosed or resp.multiRaidStageData.hp <= 0:
                self._log(f"已支援并结束团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) {raid_damage} 伤害 by {raid.hostUserName}")
            else:
                self._log(f"已支援团战 {raid.multiRaidStageDataId} (关卡 {raid.multiRaidStageMstId}) {raid_damage} 伤害 by {raid.hostUserName}")
            
            if self.get_config('support_queue'):
                queue_raid(resp.multiRaidStageData, client.session.sdk.region)
            stamina -= record.useStaminaForRescue
