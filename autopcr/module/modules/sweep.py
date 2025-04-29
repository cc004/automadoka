from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.models import *
from datetime import datetime, timedelta, timezone

@description('扫荡最高经验获得的露娜塔层')
@name('扫荡露娜塔')
@default(True)
class tower(Module):
    async def do_task(self, client: pcrclient):
        quest_mst = (await client.mst(MstApiGetQuestStageMstListRequest())).mstList
        quest_group_mst = (await client.mst(MstApiGetQuestGroupMstListRequest())).mstList
        
        party_data_list = [p for p in client.data.resp.partyDataList if p.partyType == 1]
        tower_list = await client.mst(MstApiGetTowerMstListRequest())
        now = datetime.now().astimezone()
        open_towers = [t for t in tower_list.mstList if now < datetime.fromisoformat(t.endTime) and now > datetime.fromisoformat(t.startTime)]
        if not open_towers:
            raise SkipError("露娜塔未开启")

        tower_group_id = next(q.questGroupMstId for q in quest_group_mst if q.questCategoryMstId == 5)
        last_floor = max([q for q in quest_mst if q.questGroupMstId == tower_group_id], key=lambda q: q.questStageMstId)
        req_tower_top = TowerApiGetTowerTopRequest()
        tower_top = await client.request(req_tower_top)
        if tower_top.userTowerData.skipNum == 0:
            raise SkipError("露娜塔没有剩余扫荡次数")
        if tower_top.userTowerData.maxQuestStageMstId != last_floor.questStageMstId:
            raise SkipError("露娜塔最后一层尚未通关")
        
        req_skip_tower = TowerApiSkipQuestBattleRequest()
        req_skip_tower.partyDataId = max(party_data_list, key=lambda p: p.partyPower).partyDataId
        req_skip_tower.repeatNum = tower_top.userTowerData.skipNum
        req_skip_tower.questStageMstId = tower_top.userTowerData.maxQuestStageMstId
        await client.request(req_skip_tower)
        self._log(f"扫荡了{tower_top.userTowerData.skipNum}次露娜塔")

@description('扫荡最高好感的心之器')
@name('扫荡心之器')
@default(True)
class heart(Module):
    async def do_task(self, client: pcrclient):
        quest_mst = (await client.mst(MstApiGetQuestStageMstListRequest())).mstList

        party_data_list = [p for p in client.data.resp.partyDataList if p.partyType == 1]
        config = client.data.config

        req_heart = QuestOutGameApiGetUserQuestCharacterHeartListRequest()
        heart_record = await client.request(req_heart)
        # 判断是否跨天（4 点算新一天）
        if heart_record.userQuestCharacterHeartData.userId is None:
            raise SkipError("未解锁心之器")
        last_time = datetime.fromisoformat(heart_record.userQuestCharacterHeartData.dailyClearCountUpdatedTime)
        is_next_day = (datetime.now() - timedelta(hours=4)).timetuple().tm_yday != (
            last_time - timedelta(hours=4)
        ).timetuple().tm_yday
        used = 0 if is_next_day else heart_record.userQuestCharacterHeartData.dailyClearCount
        remaining = config.questConfig.characterHeartDailyBattleClearLimit - used

        if remaining <= 0:
            raise SkipError("心之器没有剩余次数")
        
        max_exp_quest = max(
            [q for q in quest_mst if q.questGroupMstId == 301],
            key=lambda q: q.characterHeartExp
        )
        rec = next(
            (r for r in heart_record.userQuestCharacterHeartPartySaveDataList
            if r.questStageMstId == max_exp_quest.questStageMstId),
            None
        )
        if rec is None:
             raise SkipError("最高经验的心之器尚未通关")
        
        req_skip_heart = QuestBattleApiSkipQuestBattleRequest()
        req_skip_heart.isArchiveEvent = False
        req_skip_heart.partyDataId = max(party_data_list, key=lambda p: p.partyPower).partyDataId
        req_skip_heart.questStageMstId = rec.questStageMstId
        req_skip_heart.repeatNum = remaining
        await client.request(req_skip_heart)
        self._log(f"扫荡了{remaining}次心之器")

@description('收集首页宝箱')
@name('收集宝箱')
@default(True)
class gather(Module):
    async def do_task(self, client: pcrclient):
        req_gather = GatheringApiGetGatheringTopRequest()
        gathering_top = await client.request(req_gather)
        if gathering_top.userGatheringData.shortcutCount == 0:
            await client.request(GatheringApiShortcutGatheringRequest())
            self._log(f"收集了每日第一次免费加速")

        now = datetime.now(timezone.utc).astimezone()
        gather_time = now - datetime.fromisoformat(gathering_top.userGatheringData.gatheringTime)

        if gather_time < timedelta(hours=5):
            raise SkipError("宝箱时间未超过5小时，不收取")
        await client.request(GatheringApiReceiveRewardRequest())
        self._log(f"收集了当前宝箱")

@description('领取已经完成的任务奖励')
@name('领取任务')
@default(True)
class mission(Module):
    async def do_task(self, client: pcrclient):
        mission_mst = {m.missionMstId: m for m in (await client.mst(MstApiGetMissionMstListRequest())).mstList}

        for mission_type in (1,2,3,4):
            req_mission = MissionApiGetMissionDataListRequest()
            req_mission.missionType = mission_type
            mission = await client.request(req_mission)

            to_receive: List[int] = []
            for m in mission.missionDataList:
                mst = mission_mst[m.missionMstId]
                if not m.isClear and m.count >= mst.conditionCount:
                    to_receive.append(mst.missionMstId)
                    self._log(f"收集了{mst.title}的任务奖励")
            if to_receive:
                req_recv = MissionApiReceiveRequest()
                req_recv.missionMstIds = to_receive
                await client.request(req_recv)
        
@description('领取礼物的所有礼物')
@name('领取礼物')
@default(True)
class present(Module):
    async def do_task(self, client: pcrclient):
        req_present = PresentApiGetPresentDataListRequest()
        present = await client.request(req_present)
        cnt = len(present.presentDataList)
        if cnt <= 0:
            raise SkipError("没有礼物可以收取")
        req_receive = PresentApiReceiveRequest()
        req_receive.presentDataIds = [p.presentDataId for p in present.presentDataList]
        await client.request(req_receive)
        self._log(f"收集了{cnt}个礼物")
        