from re import search

from .base import Container
from ..model.modelbase import *
from asyncio import Lock
from typing import TypeVar, Any
from ..util import aiorequests, freqlimiter
from ..constants import DEBUG_LOG, MAX_API_RUNNING
import time, datetime
import json
from ..util.logger import instance as logger
from .sdkclient import sdkclient
from . import crypto
from ..util import type_utils

class ApiException(Exception):

    def __init__(self, message, status, result_code):
        super().__init__(message)
        self.status = status
        self.result_code = result_code

class NetworkException(Exception):
    pass

TResponse = TypeVar('TResponse', bound=ResponseBase, covariant=True)
TMstType = TypeVar('TMstType', bound=Any, covariant=True)


class staticproperty:
    def __init__(self, func):
        self.fget = func
    def __get__(self, instance, owner):
        return self.fget()

class apiclient(Container["apiclient"]):
    servers: list = [] #['https://l3-prod-all-gs-gzlj.bilibiligame.net/']
    active_server: int = 0
    userId: int = 0
    sessionId: str = None
    lastHomeAccessTime: str = '0'
    uuid: str = '' 
    privateKey: bytes = b''

    def __init__(self, sdk: sdkclient):
        super().__init__()
        self._headers = sdk.header()
        self._lck = Lock()

    def actionTime(self) -> int:
        # Windows FILETIME 纪元（1601-01-01）到 Unix 纪元（1970-01-01）之间的秒数
        EPOCH_DIFFERENCE_SECONDS = 11644473600
        # 当前 UTC 时间
        now = datetime.datetime.utcnow()
        # Unix 时间戳（秒，浮点数）
        unix_seconds = now.timestamp()
        # 转成 100 纳秒刻度数
        filetime = int((unix_seconds + EPOCH_DIFFERENCE_SECONDS) * 10**7)
        return filetime

    def access_home(self):
        self.lastHomeAccessTime = str(int(time.time()))
    
    @freqlimiter.RunningLimiter(MAX_API_RUNNING)
    async def _request_internal(self, request: RequestBase[TResponse]) -> TResponse:
        if not request: return None
        # logger.info(f'{self.user_name} requested {request.__class__.__name__} at /{request.url}')
        request.lastHomeAccessTime = self.lastHomeAccessTime
        req = Request(
            payload=request,
            actionTime=self.actionTime(),
            sessionId=self.sessionId,
            userId=self.userId,
            actionToken=None,
            uuid=self.uuid,
            ctag=None
        )

        urlroot = self.servers[self.active_server]
        crypted = crypto.PackHelper.pack(req.dict(by_alias=True), crypto.PackHelper.get_iv())

        self._headers['x-post-signature'] = crypto.ApiCrypto.sign(crypted, private_key_bytes=self.privateKey)

        try:
            resp = await aiorequests.post(urlroot + request.url, data=crypted, headers=self._headers, timeout=10)

            if resp.status_code != 200:
                raise ApiException('', -1, resp.status_code)

            response = await resp.content

            response = crypto.PackHelper.unpack(response)
        except:
            raise NetworkException

        cls = type_utils.find_type_base(request.__class__, RequestBase)

        if DEBUG_LOG:
            with open('req.log', 'a') as fp:
                # fp.write(f'{self.user_name} requested {request.__class__.__name__} at /{request.url}\n')
                fp.write(json.dumps(self._headers, indent=4, ensure_ascii=False) + '\n')
                fp.write(json.dumps(json.loads(request.json(by_alias=True)), indent=4, ensure_ascii=False) + '\n')
                fp.write(f'response from {urlroot}\n')
                fp.write(json.dumps(dict(resp.headers), indent=4, ensure_ascii=False) + '\n')
                fp.write(json.dumps(response, indent=4, ensure_ascii=False) + '\n')
        
        response: Response[TResponse] = Response[cls].parse_obj(response)

        if response.errors is not None:
            raise ApiException('\n'.join(err.reason for err in response.errors), status=response.status, result_code=resp.status_code)

        assert response.payload is not None

        if (request.url == '/api/home/get_home_info'):
            self.access_home()

        return response.payload

    async def request(self, request: RequestBase[TResponse]) -> TResponse:
        async with self._lck:
            return await self._request_internal(request)
    
