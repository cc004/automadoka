from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.models import *
from datetime import datetime, timedelta, timezone

@description('阅读全部活动剧情')
@name('阅读活动剧情')
@default(True)
class eventscenario(Module):
    async def do_task(self, client: pcrclient):
        story_event = {
            m.storyEventMstId: m for m in
            await db.mst(MstApiGetStoryEventMstListRequest())
        }
        scenario_list = {
            x.storyEventScenarioMstId: x for x in
            await db.mst(MstApiGetStoryEventScenarioMstListRequest())
        }

        story_top = await client.request(StoryEventApiGetTopRequest())

        cleared_stage = set(
            x.questStageMstId for x in story_top.userQuestStageDataList
        )

        for scenario_id in story_top.storyEventScenarioMstIdList:
            if scenario_id in story_top.clearStoryEventScenarioMstIdList:
                continue
            record = scenario_list[scenario_id]
            if not record.conditionQuestStageMstId in cleared_stage:
                continue

            request = CollectionApiUpdateAlreadyViewRequest()
            request.objectType = ObjectObjectType.Adv
            request.objectIds = [record.advMstId]
            await client.request(request)

            request = StoryEventApiScenarioReadRequest()
            request.storyEventScenarioMstId = record.storyEventScenarioMstId
            await client.request(request)

            self._log(f'已阅读活动剧情: {story_event[record.storyEventMstId].name} ({record.storyEventScenarioMstId})')

@description('去除所有光之间红点')
@name('阅读光之间内容')
@default(True)
class collection(Module):
    async def do_task(self, client: pcrclient):
        for collection in [
            v for v in client.data.collection.values()
            if v.isGet and not v.isAlreadyView
        ]:
            request = CollectionApiUpdateAlreadyViewRequest()
            request.objectType = collection.objectType
            request.objectIds = [collection.objectId]
            await client.request(request)

            self._log(f'已阅读光之间内容: {collection.objectType}::{collection.objectId}')



