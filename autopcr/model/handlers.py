from . import responses
from .common import *
from ..core.datamgr import datamgr
from ..db.database import db

def handles(cls):
    cls.__base__.update = cls.update
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

