from . import responses
from .common import *
from ..core.datamgr import datamgr
from .registry import register_handler

def handles(cls):
    register_handler(cls.__base__._name, cls.update)
    return None

@handles
class UserApiGetInitDataListResponse(responses.UserApiGetInitDataListResponse):
    async def update(self, mgr: datamgr, request):
        mgr.resp = self

@handles
class ConfigApiGetConfigResponse(responses.ConfigApiGetConfigResponse):
    async def update(self, mgr: datamgr, request):
        mgr.config = self

@handles
class CollectionApiGetCollectionDataListRequestResponse(responses.CollectionApiGetCollectionDataListResponse):
    async def update(self, mgr: datamgr, request):
        mgr.collection = {
            (x.objectType, x.objectId) : x for x in self.collectionDataList
        }

@handles
class CollectionApiUpdateAlreadyViewResponse(responses.CollectionApiUpdateAlreadyViewResponse):
    async def update(self, mgr: datamgr, request):
        for record in self.collectionDataList:
            mgr.collection[(record.objectType, record.objectId)] = record

@handles
class UserApiSetStaminaRecoverResponse(responses.UserApiSetStaminaRecoverResponse):
    async def update(self, mgr: datamgr, request):
        mgr.resp.userParamData = self.userParamData

@handles
class LikeApiExecLikeListResponse(
    responses.LikeApiExecLikeListResponse
):
    async def update(self, mgr: datamgr, request):
        for item in self.resultList or []:
            if not item.isFriendMedalAcquired:
                continue

            medal_once = next(
                x.num
                for x in mgr.config.friendConfig.friendMedal
                # Older generated caches store this field as type_ with alias 'type'.
                if x.dict(by_alias=True)['type'] == 'ExecLike'
            )

            medal_total = (
                mgr.config.friendConfig.gainTodayFriendMedalMaxNum
            )

            mgr.resp.userParamData.todayFriendMedalCount = min(
                medal_total,
                mgr.resp.userParamData.todayFriendMedalCount + medal_once
            )
