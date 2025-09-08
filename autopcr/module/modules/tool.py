from typing import List, Set

from ..config import *
from ..modulebase import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient, ApiException
from ...core.sdkclient import account, platform
from ...db.database import db
from ...model.models import *
import random
import itertools
from collections import Counter

@name('快速刷图')
@default(False)
@inttype('force_battle_repeat_times', '重复次数', 1, [i for i in range(1, 100)])
@texttype('force_battle_quest_id', '关卡ID', '411105')
@texttype('force_battle_team', '队伍ID/名称', '20')
@texttype('force_battle_log', '战斗日志', '')
@inttype('force_battle_auto_mode', '自动模式', 0, [0, 1, 2])
@description('开了就是开了？')
class super_sweep(Module):
    async def do_task(self, client: pcrclient):
        quest_id = int(self.get_config('force_battle_quest_id'))
        team = self.get_config('force_battle_team')
        repeat_times = self.get_config('force_battle_repeat_times')

        try:
            team = int(team)
        except ValueError:
            parties = client.data.resp.partyDataList
            team = next((party.partyDataId for party in parties if party.name == team), None)
        
        if team is None:
            raise AbortError(f"队伍 '{team}' 未找到，请检查队伍ID或名称。")
        
        samst = {
            x.selectionAbilityMstId : x.name
            for x in await db.mst(MstApiGetSelectionAbilityMstListRequest())
        }

        styleMst = {
            x.styleMstId : x.name
            for x in await db.mst(MstApiGetStyleMstListRequest())
        }

        acquires = {}

        for _ in range(repeat_times):
            try:
                req = QuestBattleApiInitializeStageRequest()
                req.questStageMstId = quest_id
                req.partyDataId = team
                req.repeatNum = 0
                req.backGroundPlay = False
                req.isArchiveEvent = False

                await client.request(req)

                req = QuestBattleApiFinalizeStageForUserRequest()
                req.autoMode = self.get_config('force_battle_auto_mode')
                req.battleLog = self.get_config('force_battle_log')
                req.result = 1

                res = await client.request(req)
            except ApiException as e:
                self._log(f"战斗失败: {str(e)} (code={e.result_code})")
                break
            
            with open('temp.log', 'a') as fp:
                fp.write(res.json())
                fp.write('\n')

            for sa in res.acquiredSelectionAbilityInfoList + res.selectionAbilityConversionItemDataList:
                sname = styleMst.get(sa.styleMstId, '未知风格')
                if sname not in acquires:
                    lst = acquires[sname] = []
                else:
                    lst = acquires[sname]
                
                lst.append(samst.get(sa.selectionAbilityMstId, '未知技能'))

        self._log(f"战斗完成，获得的技能石：")

        for style, abilities in acquires.items():
            self._log(f"{style}:")
            ability_counts = Counter(abilities)
            for ability, count in ability_counts.items():
                ability_str = f"{ability} x{count}"
                self._log(f"  - {ability_str}")

from raid.raidworker import raidworker

@name('魔女救世')
@default(False)
@texttype('raid_support_account', '小号引继码', '')
@texttype('raid_support_password', '小号密码', '')
@booltype('raid_suppport_ignore_host', '忽略本人为房主的房间', True)
@description('秒掉当前参与的所有团战')
class raid_support(Module):
    async def do_task(self, client: pcrclient):
        raid_top = await client.request(MultiRaidApiGetTopRequest())

        sdktype = client.session.sdk.__class__

        client2 = raidworker(
            self.get_config('raid_support_account'),
            self.get_config('raid_support_password'),
            'Raid Worker'
        )

        await client2.prepare()
        stamina = await client2.now_stamina()
        
        stamina_cost = {
            stage.multiRaidStageMstId: stage.useStaminaForRescue
            for stage in await db.mst(MstApiGetMultiRaidStageMstListRequest())
        }

        ignore = self.get_config('raid_suppport_ignore_host')

        for raid in raid_top.multiRaidStageDataList:
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
