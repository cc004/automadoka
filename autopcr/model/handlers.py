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
