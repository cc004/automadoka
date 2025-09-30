from ..core.sdkclient import sdkclient, account, platform
from ..constants import BSDK, QSDK, BSDKRSA, QSDKRSA
import base64
import hashlib
import hmac
import json
import random
import time
from collections import OrderedDict
from typing import Optional, Dict, Any
from urllib.parse import quote
from ..core.version import version_info

from ..util import aiorequests  # 你给的异步 requests 封装
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils

# —— PEM 导出扩展 —— #
def export_subject_public_key_info_pem(key: rsa.RSAPrivateKey) -> str:
    pub_bytes = key.public_key().public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )
    b64 = base64.encodebytes(pub_bytes).decode("ascii")
    return f"-----BEGIN PUBLIC KEY-----\n{b64}-----END PUBLIC KEY-----"


# —— ROT13 与 “B” 编解码 —— #
def rot13(s: str) -> str:
    def _r(c):
        o = ord(c)
        if 65 <= o <= 90:
            return chr((o - 65 + 13) % 26 + 65)
        if 97 <= o <= 122:
            return chr((o - 97 + 13) % 26 + 97)
        return c
    return "".join(_r(c) for c in s)

def B_encode(input_str: str) -> str:
    b64 = base64.b64encode(input_str.encode("utf-8")).decode("ascii")
    rev = b64[::-1]
    return rot13(rev)


# —— URL 与 参数签名帮助 —— #
class Util:
    @staticmethod
    def encode(s: Optional[str]) -> Optional[str]:
        if s is None:
            return None
        out = []
        for ch in s:
            if ch.isalnum() or ch in "-._~":
                out.append(ch)
            else:
                for b in ch.encode("latin-1"):
                    out.append(f"%{b:02X}")
        return "".join(out)

    @staticmethod
    def base_url(url: str) -> str:
        from urllib.parse import urlparse
        u = urlparse(url)
        netloc = u.hostname
        if u.port and not ((u.scheme=="http" and u.port==80) or (u.scheme=="https"and u.port==443)):
            netloc += f":{u.port}"
        path = u.path or "/"
        return f"{u.scheme}://{netloc}{path}"

    @staticmethod
    def normalize(method: str, url: str, params: Dict[str,str]) -> str:
        from urllib.parse import urlparse, parse_qsl
        parsed = urlparse(url)
        for k,v in parse_qsl(parsed.query, keep_blank_values=True):
            params[k] = v
        items = [
            f"{Util.encode(k)}={Util.encode(v)}"
            for k,v in sorted(params.items())
            if k != "oauth_signature"
        ]
        param_str = "&".join(items)
        return f"{Util.encode(method)}&{Util.encode(Util.base_url(url))}&{Util.encode(param_str)}"

    
class GreeClient:
    GOOGLE_ID = '466108416650-d4805jtr6idhgs25ahbqu9en4ik02b45.apps.googleusercontent.com'
    GOOGLE_PWD = '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'
    @property
    def APP_ID(self) -> str: ...

    @property
    def APP_SECRET(self) -> str: ...

    @property
    def BASE_URL(self) -> str: ...
    
    @staticmethod
    def generate_device_id() -> str:
        buf = bytes([random.randint(0, 255) for _ in range(8)])
        return buf.hex()

    def __init__(self,
                 private_key: Optional[bytes] = None,
                 uuid: Optional[str] = None):
        self.private_key = private_key
        self.uuid = uuid
        self.public_key_pem: Optional[str] = None
        self.device_id = B_encode(self.generate_device_id())
        if private_key:
            key = serialization.load_der_private_key(private_key, password=None)
            self.public_key_pem = export_subject_public_key_info_pem(key)
        

    async def login(self):
        try:
            await self.post("/auth/authorize")
        except Exception as ex:
            # 假设 aiorequests 抛的异常 message 中包含响应 body
            if "Inactive Device" in str(ex):
                await self.post("/linked/active/update")
                await self.post("/auth/authorize")

    async def login(self):
        
    async def register(self):
        key = rsa.generate_private_key(public_exponent=65537, key_size=512)
        priv_bytes = key.private_bytes(
            serialization.Encoding.DER,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        )
        self.public_key_pem = export_subject_public_key_info_pem(key)

        payload = {
            "appVersion": version_info.version,
            "urlParam": None,
            "deviceModel": "Asus ASUS_I003DD",
            "osType": 2,
            "osVersion": "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)",
            "storeType": 2,
            "graphicsDeviceId": 0,
            "graphicsDeviceVendorId": 0,
            "processorCount": 4,
            "processorType": "x86-64 SSE3 SSE4.1 SSE4.2 AVX",
            "supportedRenderTargetCount": 8,
            "supports3DTextures": True,
            "supportsAccelerometer": True,
            "supportsComputeShaders": True,
            "supportsGyroscope": True,
            "supportsImageEffects": True,
            "supportsInstancing": True,
            "supportsLocationService": True,
            "supportsRenderTextures": True,
            "supportsRenderToCubemap": True,
            "supportsShadows": True,
            "supportsSparseTextures": False,
            "supportsStencil": 1,
            "supportsVibration": False,
            "uuid": None,
            "xuid": 0,
            "sm": version_info.sm
        }
        result = await self.post("/auth/initialize", body={
            "device_id": self.device_id,
            "token": self.public_key_pem,
            "payload": json.dumps(payload)
        })
        self.private_key = priv_bytes
        self.uuid = result["uuid"]

    async def post(self, route: str, body: Optional[Dict[str,Any]] = None) -> Dict[str,Any]:
        return await self._request("POST", route, body)

    async def get(self, route: str) -> Dict[str,Any]:
        return await self._request("GET", route, None)

    async def _request(self, method: str, route: str, body: Optional[Dict[str,Any]]):
        url = f"{self.BASE_URL}{route}"
        raw = "" if body is None else json.dumps(body, separators=(",",":"))
        ts = str(int(time.time()))
        oauth = OrderedDict({
            "oauth_body_hash": base64.b64encode(hashlib.sha1(raw.encode('utf8')).digest()).decode('utf8').strip(),
            "oauth_consumer_key": self.APP_ID,
            "oauth_nonce": str(random.getrandbits(64)),
            "oauth_timestamp": ts,
            "oauth_version": "1.0",
        })
        if self.private_key:
            oauth["oauth_signature_method"] = "RSA-SHA1"

            key: rsa.RSAPrivateKey = serialization.load_der_private_key(self.private_key, password=None)

            # 1) xoauth_as_hash 签名 APP_SECRET + ts
            v6 = (self.APP_SECRET + ts).encode("utf-8")
            hash1 = hashlib.sha1(v6).digest()
            sig1 = key.sign(
                hash1,
                padding.PKCS1v15(),
                utils.Prehashed(hashes.SHA1())
            )
            oauth["xoauth_as_hash"] = base64.b64encode(sig1).decode().strip()

            oauth["xoauth_requestor_id"] = self.uuid

            # 2) oauth_signature 签名规范化后的 base-string
            norm = Util.normalize(method, url, oauth.copy()).encode("utf-8")
            hash2 = hashlib.sha1(norm).digest()
            sig2 = key.sign(
                hash2,
                padding.PKCS1v15(),
                utils.Prehashed(hashes.SHA1())
            )
            oauth["oauth_signature"] = base64.b64encode(sig2).decode().strip()
        else:
            oauth["oauth_signature_method"] = "HMAC-SHA1"
            norm = Util.normalize(method, url, dict(oauth))
            hm = hmac.new(self.APP_SECRET.encode(), norm.encode('utf8'), hashlib.sha1).digest()
            oauth["oauth_signature"] = base64.b64encode(hm).decode('utf8').strip()

        auth_header = "OAuth " + ",".join(
            f'{k}="{quote(v)}"' for k,v in oauth.items()
        )

        common_headers = {
            "X-GREE-GAMELIB": (
                f"authVersion%3D1.5.28%26billing%3D3%26storeType%3Dgoogle"
                f"%26appVersion%3D{version_info.version}%26uaType%3Dandroid-app"
                "%26carrier%3DChina+Mobile+GSM%26compromised%3Dfalse"
                "%26countryCode%3DCN%26currencyCode%3DCNY"
                "%26model%3DAndroid-Phone"
            ),
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                "Chrome/68.0.3440.70 Mobile Safari/537.36"
            )
        }

        # 发起请求
        if method == "POST":
            resp = await aiorequests.post(
                url, data=raw.encode(), headers={
                    "Content-Type":"application/json",
                    "Authorization": auth_header,
                    **common_headers
                })
        else:
            resp = await aiorequests.get(url, headers={
                "Authorization": auth_header,
                **common_headers
            })

        result = await resp.json()
        if result.get("result") != "OK":
            raise RuntimeError(json.dumps(result))
        resp.raise_for_status()
        return result

    async def register_password(self, password: str):
        await self.post("/migration/password/register", {
            "migration_password": B_encode(password),
            "device_id": self.device_id,
        })

    async def get_migration_code(self) -> str:
        r = await self.get("/migration/code")
        return r["migration_code"]

    async def migrate_from(self, migration_code: str, password: str):
        migrated = await self.post("/migration/code/verify", {
            "migration_code": migration_code,
            "migration_password": B_encode(password),
        })
        await self.post("/migration", {
            "migration_token": migrated["migration_token"],
            "src_uuid": migrated["src_uuid"],
            "device_id": self.device_id,
            "token": self.public_key_pem,
            "dst_uuid": self.uuid,
        })
        self.uuid = migrated["src_uuid"]

    async def registerGoogleCode(self, code: str, url: str, platform: int):
        auth = base64.b64encode(f"{self.GOOGLE_ID}:{self.GOOGLE_PWD}".encode('utf8')).decode('utf8')
        token = await aiorequests.post("https://www.googleapis.com/oauth2/v4/token", data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": url,
            "scope": "profile"
        }, headers={
            'Authorization': 'Basic ' + auth
        })
        
        token = (await token.json())['access_token']
        
        profile = await aiorequests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers={
            'Authorization': 'Bearer ' + token
        })
        
        profile = (await profile.json())
        
        await self.register3rdparty(profile['sub'], token, platform)

    async def register3rdparty(self, sub: str, token: str, platform: int):
        hashed_account_id= hashlib.sha256(sub.encode('utf8')).digest()
        hashed_account_id = base64.b64encode(hashed_account_id).decode('utf8')
        
        await self.post("/migration/3rd/user/register", {
            "access_token": token,
            "hashed_account_id": hashed_account_id,
            "platform": platform
        })

    async def unregister3rdparty(self, platform: int):
        await self.post("/migration/3rd/user/unregister", {
            "platform": platform
        })

class JpGreeClient(GreeClient):
    @property
    def APP_ID(self) -> str:
        return '863165203288142'

    @property
    def APP_SECRET(self) -> str:
        return '858931807c393c548db2a5f725bb6b45'

    @property
    def BASE_URL(self) -> str:
        return 'https://gl-pkl-jp-payment.gree-apps.net/v1.0'


class UsGreeClient(GreeClient):
    @property
    def APP_ID(self) -> str:
        raise NotImplementedError("US client not supported")

    @property
    def APP_SECRET(self) -> str:
        raise NotImplementedError("US client not supported")

    @property
    def BASE_URL(self) -> str:
        return 'https://gl-pkl-us-payment.gree-apps.net/v1.0'


import os, re
from ..constants import CACHE_DIR
from requests import HTTPError
from typing import Type

class sdkclientbase(sdkclient):

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

        with open(self.cacheFile, 'w') as fp:
            json.dump({
                'privateKey': base64.b64encode(gclient.private_key).decode('utf8'),
                'uuid': gclient.uuid
            }, fp)
        
        self.gclient = gclient

    async def login(self):
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
        return gclient.private_key, gclient.uuid



class bsdkclient(sdkclientbase):
    
    @property
    def clientType(self) -> Type[GreeClient]:
        return JpGreeClient
    
    @property
    def apiroot(self):
        return 'https://api.mmme.pokelabo.jp'

class qsdkclient(bsdkclient):
    @property
    def clientType(self) -> Type[GreeClient]:
        return UsGreeClient

    @property
    def apiroot(self):
        return 'https://api-gl.mmme.pokelabo.jp'
        
class bsdkrsaclient(sdkclient):

    async def login(self):
        return self._account.password, self._account.username

    @property
    def apiroot(self):
        return 'https://api.mmme.pokelabo.jp'
       
class qsdkrsaclient(sdkclient):

    async def login(self):
        return self._account.password, self._account.username

    @property
    def apiroot(self):
        return 'https://api-gl.mmme.pokelabo.jp'
       
sdkclients = {
    BSDK: bsdkclient,
    QSDK: qsdkclient,
    BSDKRSA: bsdkrsaclient,
    QSDKRSA: qsdkrsaclient
}

def create(channel, *args, **kwargs) -> sdkclient:
    if channel not in sdkclients:
        raise ValueError(f"Invalid channel {channel}")
    return sdkclients[channel](*args, **kwargs)
