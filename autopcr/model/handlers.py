from . import responses
from .common import *
from ..core.datamgr import datamgr
from ..db.database import db

def handles(cls):
    cls.__base__.update = cls.update
    return None

@handles
class LoginApiLoginResponse(responses.LoginApiLoginResponse):
    async def update(self, mgr: datamgr, request):
        pass
