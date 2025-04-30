import datetime
from ..core.apiclient import apiclient
from ..core.base import RequestHandler
from typing import TypeVar, List, Any
from ..model import models
from ..model.modelbase import MstRequestBase
import re

TMstType = TypeVar('TMstType', bound=Any, covariant=True)
T = TypeVar("T")

class database():
    def __init__(self):
        self._data_revision = {}
        self._data_cache = {}
        self._current_revision = {}
        self._client: apiclient = None
        
    async def update(self, client: RequestHandler):
        data_revision = {
            x.name: x.revision for x in 
            (await client.request(models.GetResourceMasterDataMstListRequest())).mstList
        }
        
        self._current_revision = data_revision
        self._client = client
        
    @staticmethod
    def _get_mst_key(url: str) -> str:
        # convert snake case to camel case
        last = url.split('/')[-1]
        return re.sub(r'_(\w)', lambda x: x.group(1).upper(), last)
    
    async def mst(self, request: MstRequestBase[TMstType]) -> List[TMstType]:
        mstName = database._get_mst_key(request.url)
        if mstName in self._data_cache:
            if self._data_revision[mstName] == self._current_revision[mstName]:
                return self._data_cache[mstName]
        mst = (await self._client.request(request)).mstList
        self._data_cache[mstName] = mst
        self._data_revision[mstName] = self._current_revision[mstName]
        return mst
    
    def is_clan_battle_time(self):
        return False

    def format_time(self, time: datetime.datetime) -> str:
        return time.strftime("%Y/%m/%d %H:%M:%S")

    def format_date(self, time: datetime.datetime) -> str:
        return time.strftime("%Y/%m/%d")

    def format_time_safe(self, time: datetime.datetime) -> str:
        return time.strftime("%Y%m%d%H%M%S")

    def format_second(self, total_seconds: int) -> str:
        time_delta = datetime.timedelta(seconds=total_seconds)
        hours, remainder = divmod(time_delta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"


db = database()
