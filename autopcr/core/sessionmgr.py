from .base import Component, RequestHandler
from .apiclient import apiclient, ApiException
from .sdkclient import sdkclient
import os
from ..model.models import *
from ..constants import CACHE_DIR, APP_VER
from ..util.logger import instance as logger
from ..db.database import db
import hashlib

class sessionmgr(Component[apiclient]):
    def __init__(self, sdk: sdkclient):
        super().__init__()
        self.cacheDir = os.path.join(CACHE_DIR, 'token')
        self.sdk = sdk
        self._logged = False
        self.auto_relogin = True
        self._sdkaccount = None
        self.session_expire_time = 0
        self.id = hashlib.md5( self.sdk.account.encode('utf-8')).hexdigest()
        if not os.path.exists(self.cacheDir):
            os.makedirs(self.cacheDir)

    async def _bililogin(self):
        privateKey, uuid = await self.sdk.login()
        self._sdkaccount = privateKey, uuid

    async def _ensure_token(self, next: RequestHandler):
        try:
            if self._sdkaccount is None:
                await self._bililogin()
            
            privateKey, uuid = self._sdkaccount
            req = LoginApiLoginRequest(
                appVersion=APP_VER,
                urlParam=None,
                deviceModel="Asus ASUS_I003DD",
                osType=2,
                osVersion="Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)",
                storeType=2,
                graphicsDeviceId=0,
                graphicsDeviceVendorId=0,
                processorCount=4,
                processorType="x86-64 SSE3 SSE4.1 SSE4.2 AVX",
                supportedRenderTargetCount=8,
                supports3DTextures=True,
                supportsAccelerometer=True,
                supportsComputeShaders=True,
                supportsGyroscope=True,
                supportsImageEffects=True,
                supportsInstancing=True,
                supportsLocationService=True,
                supportsRenderTextures=True,
                supportsRenderToCubemap=True,
                supportsShadows=True,
                supportsSparseTextures=False,
                supportsStencil=1,
                supportsVibration=False,
                uuid=None,
                xuid=0
            )
            self._container.privateKey = privateKey
            self._container.uuid = uuid
            resp = await next.request(req)
            self._container.sessionId = resp.sessionId
            self._container.userId = resp.userId
        except Exception as e:
            logger.exception(e)
            raise PanicError(f"登录出错: {e}")
        finally:
            await self.sdk.invoke_post_login()

    async def _login(self, next: RequestHandler):
        while True:
            try:
                self._container.servers = [self.sdk.apiroot]
                self._container.active_server = 0
                
                await self._ensure_token(next)
                
                await db.update(next)
                
                await next.request(UserApiGetInitDataListRequest())
                await next.request(PartyApiGetCharacterBuildDataListRequest())
                await next.request(CharacterApiGetCharacterListRequest())
                await next.request(CollectionApiGetCollectionParamUpAchieveDataListRequest())
                await next.request(CollectionApiGetCollectionDataListRequest())
                await next.request(StyleApiGetStyleDataListRequest())
                await next.request(UserApiGetUserParamDataRequest())
                await next.request(ConfigApiGetConfigRequest())
                await next.request(UserApiLoadOptionRequest())
                await next.request(WebPayApiCancelLatestRequest())
                await next.request(TermsApiGetUpdatedTermsRequest(storeType=2))
                self._logged = True
                
                break
            except ApiException as e:
                raise

    @property
    def is_session_expired(self):
        raise NotImplementedError

    async def request(self, request: RequestBase[TResponse], next: RequestHandler) -> TResponse:
        if not self._logged:
            await self._login(next)
        try:
            return await next.request(request)
        except ApiException as ex:
            self._logged = False
            raise

    async def clear_session(self):
        self._logged = False
