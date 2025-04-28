from collections import Counter
from .base import Component, RequestHandler
from .apiclient import apiclient
from ..model.modelbase import *
from typing import Callable, Set, Dict, Tuple, Union
import typing
from ..model.common import *
import json, base64, gzip
from ..db.dbmgr import instance as dbmgr
from ..db.database import db
from ..util.linq import flow
from asyncio import Lock

_data_lck = Lock()

class datamgr(BaseModel, Component[apiclient]):
    ready: bool = False
    username: str = None

    async def request(self, request: Request[TResponse], next: RequestHandler) -> TResponse:
        resp = await next.request(request)
        if resp:
            await resp.update(self, request)
        self.data_time = apiclient.time
        return resp

