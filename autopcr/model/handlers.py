from . import responses
from .common import *
from ..core.datamgr import datamgr
from .registry import register_handler
from ..util.raidoption import medal_per_like

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

            medal_once = medal_per_like(mgr.config.friendConfig.friendMedal)
            if not medal_once:
                # 配置里没有 ExecLike 这一行（或数量是 0）。
                # ⚠️ 这里原来写的是 `next(...)` 且没给默认值 —— 一旦配置变了就抛
                # `StopIteration`，从协程里逃出来会变成 `RuntimeError`，
                # 「魔女点赞」整个模块直接报错。宁可少算计数也不能炸。
                continue

            medal_total = (
                mgr.config.friendConfig.gainTodayFriendMedalMaxNum
            )

            mgr.resp.userParamData.todayFriendMedalCount = min(
                medal_total,
                mgr.resp.userParamData.todayFriendMedalCount + medal_once
            )
