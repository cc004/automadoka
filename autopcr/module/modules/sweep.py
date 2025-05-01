from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.models import *
from datetime import datetime, timedelta, timezone

@description('自动使用最高加成扫荡当前已通关活动')
@name('扫荡活动')
@default(True)
class event(Module):
    async def do_task(self, client: pcrclient):
        party_data_list = [p for p in client.data.resp.partyDataList if p.partyType == 1]
        
        story_event = {
            m.storyEventMstId: m for m in
            await db.mst(MstApiGetStoryEventMstListRequest())
        }
        story_quest = {
            x.questStageMstId: x.eventItemNum for x in
            await db.mst(MstApiGetStoryEventQuestStageMstListRequest())
        }
        bonus_list = await db.mst(MstApiGetStoryEventBonusRateMstListRequest())
        story_bonus: Dict[int, Dict[int, List[int]]] = {}
        for b in bonus_list:
            story_bonus.setdefault(b.storyEventMstId, {})[b.bonusMstId] = [
                b.limitBreakCount0Rate,
                b.limitBreakCount1Rate,
                b.limitBreakCount2Rate,
                b.limitBreakCount3Rate,
                b.limitBreakCount4Rate,
                b.limitBreakCount5Rate,
            ]

        # 限定破解锁次数
        limit_break_count = {
            **{c.cardMstId: c.limitBreakCount for c in client.data.resp.cardDataList},
            **{s.styleMstId: s.limitBreakCount for s in client.data.resp.styleDataList}
        }
        
        story_top = await client.request(StoryEventApiGetTopRequest())
        
        for info in story_top.storyEventDataList:
            mst = story_event[info.storyEventMstId]
            to_sweep = sorted(
                [x for x in story_top.userQuestStageDataList
                if x.questGroupMstId == mst.storyQuestGroupId],
                key=lambda x: story_quest[x.questStageMstId],
                reverse=True
            )
            if not to_sweep or story_quest[to_sweep[0].questStageMstId] != 1000:
                self._log(f"活动 {mst.name} 未完全通关.")
                continue

            if info.todayPlayableCount == 0:
                self._log(f"活动{mst.name}没有剩余扫荡次数.")
                continue

            quest_id = to_sweep[0].questStageMstId
            bonus_data = story_bonus[mst.storyEventMstId]

            def party_bonus(p: PartyPartyDataRecord):
                ids = [
                    p.member1,p.member2,p.member3,p.member4,p.member5,
                    p.cardMstId1,p.cardMstId2,p.cardMstId3,p.cardMstId4,p.cardMstId5
                ]
                return sum(
                    bonus_data.get(i, [0, 0, 0, 0, 0, 0])[limit_break_count.get(i,0)]
                    for i in ids
                ), p

            max_bonus, best_party = max(map(party_bonus, party_data_list), key=lambda x: x[0])
            self._log(f"活动 {mst.name} 最高加成队伍： {best_party.name} - {max_bonus/10}%")

            req_skip_new = QuestBattleApiSkipQuestBattleRequest()
            req_skip_new.isArchiveEvent = False
            req_skip_new.partyDataId = best_party.partyDataId
            req_skip_new.questStageMstId = quest_id
            req_skip_new.repeatNum = info.todayPlayableCount
            await client.request(req_skip_new)
            
            self._log(f"扫荡了活动 {mst.name} ({quest_id}){info.todayPlayableCount}次")


@description('自动使用最高加成扫荡当前档案活动')
@name('扫荡档案活动')
@default(True)
class archive(Module):
    async def do_task(self, client: pcrclient):
        
        party_data_list = [p for p in client.data.resp.partyDataList if p.partyType == 1]
        
        story_event = {
            m.storyEventMstId: m for m in
            await db.mst(MstApiGetStoryEventMstListRequest())
        }
        story_quest = {
            x.questStageMstId: x.eventItemNum for x in
            await db.mst(MstApiGetStoryEventQuestStageMstListRequest())
        }
        
        bonus_list = await db.mst(MstApiGetStoryEventBonusRateMstListRequest())
        story_bonus: Dict[int, Dict[int, List[int]]] = {}
        for b in bonus_list:
            story_bonus.setdefault(b.storyEventMstId, {})[b.bonusMstId] = [
                b.limitBreakCount0Rate,
                b.limitBreakCount1Rate,
                b.limitBreakCount2Rate,
                b.limitBreakCount3Rate,
                b.limitBreakCount4Rate,
                b.limitBreakCount5Rate,
            ]

        # 限定破解锁次数
        limit_break_count = {
            **{c.cardMstId: c.limitBreakCount for c in client.data.resp.cardDataList},
            **{s.styleMstId: s.limitBreakCount for s in client.data.resp.styleDataList}
        }

        # Archive 事件首页
        req_archive = StoryEventApiGetArchiveEventListRequest()
        archive_top = await client.request(req_archive)

        max_sweep_quest_id = -1
        max_sweep_bonus = -1
        max_sweep_bonus_party = -1
        max_sweep_bonus_event = None
        sweep_count = archive_top.storyEventDataList[0].todayPlayableCount

        if sweep_count <= 0:
            raise SkipError('档案活动已无剩余次数')
        
        for info in archive_top.storyEventInfoList:
            mst = story_event[info.storyEventMstId]
            to_sweep = sorted(
                [x for x in archive_top.userQuestStageDataList
                if x.questGroupMstId == mst.storyQuestGroupId],
                key=lambda x: story_quest[x.questStageMstId],
                reverse=True
            )
            
            if not to_sweep or story_quest[to_sweep[0].questStageMstId] != 1000:
                self._log(f"档案活动 {mst.name} 未完全通关.")
                continue

            quest_id = to_sweep[0].questStageMstId
            bonus_data = story_bonus[mst.storyEventMstId]

            # 计算最优队伍
            def party_bonus(p):
                ids = [
                    p.member1,p.member2,p.member3,p.member4,p.member5,
                    p.cardMstId1,p.cardMstId2,p.cardMstId3,p.cardMstId4,p.cardMstId5
                ]
                return sum(
                    bonus_data.get(i, [0, 0, 0, 0, 0, 0])[limit_break_count.get(i,0)]
                    for i in ids
                ), p

            max_bonus, best_party = max(map(party_bonus, party_data_list), key=lambda x: x[0])
            self._log(f"档案活动 {mst.name} 最高加成队伍{best_party.name} - {max_bonus/10}%")

            if max_bonus > max_sweep_bonus:
                max_sweep_bonus = max_bonus
                max_sweep_quest_id = quest_id
                max_sweep_bonus_party = best_party.partyDataId
                max_sweep_bonus_event = mst

        # sweep archive
        if max_sweep_quest_id <= 0:
            raise SkipError('没有可以扫荡的档案活动')
        
        req_skip_arch = QuestBattleApiSkipQuestBattleRequest()
        req_skip_arch.isArchiveEvent = True
        req_skip_arch.partyDataId = max_sweep_bonus_party
        req_skip_arch.questStageMstId = max_sweep_quest_id
        req_skip_arch.repeatNum = sweep_count
        await client.request(req_skip_arch)
        
        self._log(f"扫荡了档案活动 {max_sweep_bonus_event.name} ({max_sweep_quest_id}) {sweep_count} 次 (加成{max_sweep_bonus/10}%)")

    
@description('扫荡最高经验获得的露娜塔层')
@name('扫荡露娜塔')
@default(True)
class tower(Module):
    async def do_task(self, client: pcrclient):
        quest_mst = await db.mst(MstApiGetQuestStageMstListRequest())
        quest_group_mst = await db.mst(MstApiGetQuestGroupMstListRequest())
        
        party_data_list = [p for p in client.data.resp.partyDataList if p.partyType == 1]
        tower_list = await db.mst(MstApiGetTowerMstListRequest())
        now = datetime.now().astimezone()
        open_towers = [t for t in tower_list if now < datetime.fromisoformat(t.endTime) and now > datetime.fromisoformat(t.startTime)]
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
        quest_mst = await db.mst(MstApiGetQuestStageMstListRequest())

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
        mission_mst = {m.missionMstId: m for m in (await db.mst(MstApiGetMissionMstListRequest()))}

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
        