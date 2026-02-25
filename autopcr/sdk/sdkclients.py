from autopcr.model.modelbase import RequestBase
from ..core.sdkclient import sdkclient, account, platform, region
from ..constants import BSDK, QSDK, BSDKRSA, QSDKRSA, SONET
import base64
import json
import os, re
from ..constants import CACHE_DIR
from requests import HTTPError
from typing import Type
from .greeclient import GreeClient, JpGreeClient, UsGreeClient
from ..core.crypto import PKLB_HASH_KEY, SONET_HASH_KEY

from ..core import crypto

class sdkclientbase(sdkclient):

    def get_crypto_key(self) -> str:
        return PKLB_HASH_KEY
    @property
    def clientType(self) -> Type[GreeClient]: ...

    @property
    def cacheFile(self):
        if not re.match('^[A-Za-z0-9]{16}$', self._account.username):
            raise RuntimeError('引继码格式不正确')
        return os.path.join(os.path.join(CACHE_DIR, 'token'), self._account.username + '.json')

    async def register(self, password: str):
        gclient = self.clientType()
        await gclient.register()
        await gclient.login()

        code = await gclient.get_migration_code()

        await gclient.register_password(password)

        self._account = account(
            code,
            password,
            platform.Android
        )

        assert gclient.private_key is not None
        
        with open(self.cacheFile, 'w') as fp:
            json.dump({
                'privateKey': base64.b64encode(gclient.private_key).decode('utf8'),
                'uuid': gclient.uuid
            }, fp)
        
        self.gclient = gclient

    async def login(self) -> str:
        for _ in range(5):
            try:
                with open(self.cacheFile, 'r') as fp:
                    account = json.load(fp)
                gclient = self.clientType(base64.b64decode(account['privateKey']), account['uuid'])
                await gclient.login()
                break
            except (RuntimeError, FileNotFoundError):
                gclient = self.clientType()
                await gclient.register()
                await gclient.migrate_from(self._account.username, self._account.password)
                await gclient.login()

                assert gclient.private_key is not None

                with open(self.cacheFile, 'w') as fp:
                    json.dump({
                        'privateKey': base64.b64encode(gclient.private_key).decode('utf8'),
                        'uuid': gclient.uuid
                    }, fp)
            except HTTPError:
                pass
        else:
            raise ConnectionError

        self.gclient = gclient
        assert gclient.uuid is not None
        return gclient.uuid

class bsdkclient(sdkclientbase):
    
    async def post_sign(self, data: bytes) -> str:
        assert self.gclient.private_key is not None
        return crypto.ApiCrypto.sign(data, private_key_bytes=self.gclient.private_key)

    @property
    def region(self):
        return region.Japan
    
    @property
    def clientType(self) -> Type[GreeClient]:
        return JpGreeClient
    
    @property
    def apiroot(self):
        return 'https://api.mmme.pokelabo.jp'

class qsdkclient(sdkclientbase):

    async def post_sign(self, data: bytes) -> str:
        assert self.gclient.private_key is not None
        return crypto.ApiCrypto.sign(data, private_key_bytes=self.gclient.private_key)

    @property
    def region(self):
        return region.Global
    
    @property
    def clientType(self) -> Type[GreeClient]:
        return UsGreeClient

    @property
    def apiroot(self):
        return 'https://api-gl.mmme.pokelabo.jp'
        
class bsdkrsaclient(sdkclient):

    async def post_sign(self, data: bytes) -> str:
        assert self._account is not None
        return crypto.ApiCrypto.sign(data, private_key_bytes=base64.b64decode(self._account.password))

    @property
    def region(self):
        return region.Japan
    
    async def login(self):
        assert self._account is not None
        return self._account.username

    @property
    def apiroot(self):
        return 'https://api.mmme.pokelabo.jp'
       
class qsdkrsaclient(sdkclient):

    async def post_sign(self, data: bytes) -> str:
        assert self._account is not None
        return crypto.ApiCrypto.sign(data, private_key_bytes=base64.b64decode(self._account.password))

    @property
    def region(self):
        return region.Global
    
    async def login(self):
        assert self._account is not None
        return self._account.username

    @property
    def apiroot(self):
        return 'https://api-gl.mmme.pokelabo.jp'

from ..model.requests import LoginApiLoginRequest
from .sonetclient import SonetClient

class sonetsdkclient(sdkclient):

    def get_crypto_key(self) -> str:
        return SONET_HASH_KEY

    async def get_jwt_token(self) -> str:
        return await self.gclient.get_jwt_token()

    async def post_sign(self, data: bytes) -> str:
        return await self.get_jwt_token()

    async def modify_request(self, request: RequestBase):
        if type(request) is LoginApiLoginRequest:
            request.jwttoken = await self.get_jwt_token()

    @property
    def region(self):
        return region.Sonet
    
    @property
    def apiroot(self):
        return 'https://app-mme.so-net.tw'

    @property
    def cacheFile(self):
        if not re.match('^[A-Za-z0-9]{10}$', self._account.username):
            raise RuntimeError('引继码格式不正确')
        return os.path.join(os.path.join(CACHE_DIR, 'token'), self._account.username + '.json')

    async def register(self, password: str):
        gclient = SonetClient()
        await gclient.register()
        await gclient.register_password(password)

        assert gclient.handoverid is not None

        self._account = account(
            gclient.handoverid,
            password,
            platform.Android
        )

        with open(self.cacheFile, 'w') as fp:
            json.dump({
                'deviceid': gclient.deviceid,
                'uuid': gclient.uuid,
                'token': gclient.token
            }, fp)
        
        self.gclient = gclient

    async def login(self):
        for _ in range(5):
            try:
                with open(self.cacheFile, 'r') as fp:
                    account = json.load(fp)
                gclient = SonetClient(
                    deviceid=account['deviceid'],
                    uuid=account['uuid'],
                    token=account['token']
                )
                break
            except (RuntimeError, FileNotFoundError):
                gclient = SonetClient()
                await gclient.register()
                await gclient.migrate_from(self._account.username, self._account.password)

                with open(self.cacheFile, 'w') as fp:
                    json.dump({
                        'deviceid': gclient.deviceid,
                        'uuid': gclient.uuid,
                        'token': gclient.token
                    }, fp)
            except HTTPError:
                pass
        else:
            raise ConnectionError

        self.gclient = gclient
        return gclient.uuid

sdkclients = {
    BSDK: bsdkclient,
    QSDK: qsdkclient,
    BSDKRSA: bsdkrsaclient,
    QSDKRSA: qsdkrsaclient,
    SONET: sonetsdkclient,
}

from ..util.logger import instance as logger

def create(channel, *args, **kwargs) -> sdkclient:
    if channel not in sdkclients:
        logger.warning(f'未知的 SDK 类型 {channel}，使用默认 BSDK')
        channel = BSDK
    return sdkclients[channel](*args, **kwargs)
