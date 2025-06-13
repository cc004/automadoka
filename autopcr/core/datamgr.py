from .base import Component, RequestHandler
from .apiclient import apiclient
from ..model.responses import *
from ..model.modelbase import *
from typing import Dict, Tuple

class datamgr(Component[apiclient]):
    ready: bool = False
    user_name: str = ''
    resp: UserApiGetInitDataListResponse = None
    config: ConfigApiGetConfigResponse = None
    collection: Dict[Tuple[ObjectObjectType, int], CollectionCollectionDataRecord] = None

    async def request(self, request: RequestBase[TResponse], next: RequestHandler) -> TResponse:
        resp = await next.request(request)
        if resp:
            await resp.update(self, request)
        return resp

