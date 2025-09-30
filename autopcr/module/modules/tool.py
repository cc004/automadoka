from datetime import datetime, timedelta, timezone
from ..config import *
from ..modulebase import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import ApiException
from ...db.database import db
from ...model.models import *
from collections import Counter

user_tz = timezone(timedelta(hours=8))
def stamina_calc(current: int, update_time: str, config: UserUserConfig) -> int:
    now = datetime.now(tz=user_tz)
    update = datetime.fromisoformat(update_time).astimezone(user_tz)
    delta = now - update
    if delta.total_seconds() < 0 or current >= config.staminaUpperLimit:
        return current
    recover_times = delta.total_seconds() // config.staminaRecoverSec * config.staminaRecoverGemInfoRecoverAmount
    return min(current + int(recover_times), config.staminaUpperLimit)

@name('快速刷图')
@default(False)
@inttype('force_battle_repeat_times', '重复次数', 1, [i for i in range(1, 100)])
@texttype('force_battle_quest_id', '关卡ID', '411105')
@texttype('force_battle_team', '队伍ID/名称', '20')
@texttype('force_battle_log', '战斗日志', '')
@inttype('force_battle_auto_mode', '自动模式', 0, [0, 1, 2])
@description('开了就是开了？')
class super_sweep(Module):
    
    def config_string(self) -> str:
        return '\n'.join([
            f"{self.config[key].desc}: {self.get_config_str(key)}" for key in self.config
            if key != 'force_battle_log'
            ])
    
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

        stamina = stamina_calc(
            client.data.resp.userParamData.stamina,
            client.data.resp.userParamData.staminaUpdatedTime,
            client.data.config.userConfig
        )

        once_cost = next(
            x for x in await db.mst(MstApiGetQuestStageMstListRequest())
            if x.questStageMstId == quest_id
        ).useStamina // 2

        if repeat_times * once_cost > stamina:
            self._log(f"体力不足，当前体力 {stamina}，单次消耗 {once_cost}，最多可刷 {stamina // once_cost} 次")
            repeat_times = stamina // once_cost

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

import asyncio

FIELD_CLEAR = 612001

@name('神秘新功能')
@default(False)
@description('什么时候出蓓蓓呜呜呜我要死了')
@texttype('inviter_player_id', '邀请者账号', '12345678901J')
class secret:
    async def do_task(self, client: pcrclient):
        
        invite_top = await client.request(InvitationApiGetTopRequest())

        if not invite_top.inviterPlayerId:
            await client.request(InvitationApiInviteRequest(
                invitationCampaignMstId=1,
                inviterPlayerId=self.get_config('inviter_player_id')
            ))

        stratum = (await client.request(MstApiGetFieldStratumMstListRequest())).mstList
        point = (await client.request(MstApiGetFieldPointMstListRequest())).mstList
        field_mst = {
            x.fieldStageMstId: x for x in (await client.request(MstApiGetFieldStageMstListRequest())).mstList
        }

        top = await client.request(ExplorationApiGetFieldStageCollectionInfoListRequest())
        cleared_field = set(x.fieldStageMstId for x in top.fieldStageCollectionInfoList if x.isClear)

        async def clear_field(field: int):
            mst = field_mst[field]
            if field in cleared_field:
                print(f"跳过已通关篇章 {field} ({mst.name})")
                return
            if mst.prevFieldStageMstId != 0:
                await clear_field(mst.prevFieldStageMstId)
            print(f"开始清理 {field} ({mst.name})")
            top = await client.request(ExplorationApiGetTopInfoV4Request(
                fieldStageMstId=field
            ))
        
            if top.fieldStageUserData.clearFieldPointMstIdCsv:
                cleared_points = set(int(x) for x in top.fieldStageUserData.clearFieldPointMstIdCsv.split(','))
            else:
                cleared_points = set()
            
            stratums = [x for x in stratum if x.fieldStageMstId == field]

            for s in stratums:
                points = [x for x in point if x.fieldStratumMstId == s.fieldStratumMstId]
                for p in points:
                    if p.fieldPointMstId in cleared_points:
                        print(f"跳过已通关点 {p.fieldPointMstId} ({mst.name}-{p.name})")
                        continue
                    reach = await client.request(ExplorationApiReachFieldPointRequest(
                        fieldPointMstId=p.fieldPointMstId
                    ))
                    print(f"到达点 {p.fieldPointMstId} ({mst.name}-{p.name})")

                    if p.pointType == 1: # dungeon
                        start = await client.request(ExplorationApiDungeonStartRequest(
                            fieldStageMstId=s.fieldStageMstId,
                            dungeonMstId=p.pointValue1
                        ))
                        finish = await client.request(ExplorationApiDungeonGoalRequest(
                            fieldStageMstId=s.fieldStageMstId,
                            dungeonMstId=p.pointValue1
                        ))
                        print(f"完成副本点 {p.fieldPointMstId} ({mst.name}-{p.name})")
                    elif p.pointType == 2 or p.pointType == 3 or p.pointType == 4: # start
                        quest = await client.request(ExplorationBattleApiInitializeStageV4Request(
                            fieldPointMstId=p.fieldPointMstId,
                            fieldStageMstId=s.fieldStageMstId,
                            dungeonEventMstId=0,
                            dungeonRoomMstId=0,
                            bossDirectionMstId=0,
                            presetEventIndex=0,
                            partyDataId=1
                        ))
                        await asyncio.sleep(2)
                        finish = await client.request(ExplorationBattleApiFinalizeStageForUserV4Request(
                            autoMode=1,
                            battleLog="",
                            result=1
                        ))
                        print(f"完成战斗点 {p.fieldPointMstId} ({mst.name}-{p.name})")

        await clear_field(FIELD_CLEAR)
