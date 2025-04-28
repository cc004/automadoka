from .base import Component, RequestHandler
from .apiclient import apiclient
from ..model.modelbase import *

class datamgr(Component[apiclient]):
    ready: bool = False
    user_name: str = None

    async def request(self, request: Request[TResponse], next: RequestHandler) -> TResponse:
        resp = await next.request(request)
        if resp:
            await resp.update(self, request)
        return resp

