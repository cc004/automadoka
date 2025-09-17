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
        ).useStamina

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
