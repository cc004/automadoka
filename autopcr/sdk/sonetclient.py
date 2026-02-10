from typing import Optional
from ..util.aiorequests import post
import hashlib
import random
import string
import uuid
import jwt
import time

def randomhex(length: int) -> str:
    return ''.join(random.choices(string.hexdigits.lower(), k=length))

class SonetClient:
    HEADERS = {
        'User-Agent': 'UnityPlayer/2022.3.62f3 (UnityWebRequest/1.0, libcurl/8.10.1-DEV)',
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'X-Unity-Version': '2022.3.62f3'
    }

    def __init__(self, deviceid: Optional[str] = None,
                 uuid: Optional[str] = None, token: Optional[str] = None):
        if deviceid is None:
            self.deviceid = randomhex(32)
        else:
            self.deviceid = deviceid
        self.uuid = uuid
        self.token = token
        self.handoverid = None

        self._jwt = None
        self._jwt_expire = 0
    
    @staticmethod
    def sign(data: dict):
        data.pop('sign', None)
        s = ''

        for k, v in sorted(data.items(), key=lambda item: item[0]):
            s += f'{k}={v}&'

        s += 'sonet'

        data['sign'] = hashlib.md5(s.encode('utf-8')).hexdigest()

    async def _request(self, url: str, data: dict, headers: Optional[dict] = None) -> dict:
        SonetClient.sign(data)

        if headers is None:
            headers = {}

        headers.update(SonetClient.HEADERS)

        resp = await post('https://mme-sdk.so-net.tw' + url, json=data
                          ,headers=headers, timeout=15)

        obj = await resp.json()
        assert obj['status'] == 0, str(obj)

        return obj
    
    async def register(self):
        resp = await self._request('/api/register', {
            'gameid': 2601,
            'version': '1.0.1',
            'guid': str(uuid.uuid4()),
            'deviceid': self.deviceid,
            'localcountry_code': 'CN',
            'birthyear': 0,
            'birthmonth': 0,
            'platform': 2
        })
        self.uuid = resp['uuid']
        self.token = resp['token']
        self.handoverid = resp['handoverid']

    async def register_password(self, password: str):
        token = await self.get_jwt_token()        
        await self._request('/api/login/sethandoverpassword', {
            'handoverpw': password
        }, headers={
            'Authorization': f'Bearer {token}'
        })

    async def migrate_from(self, username: str, password: str):
        pass

    async def get_jwt_token(self) -> str:
        now = int(time.time())

        if now > self._jwt_expire - 120 or self._jwt is None:
            resp = await self._request('/api/login/game', {
                'gameid': 2601,
                'version': '1.0.1',
                'uuid': self.uuid,
                'token': self.token,
                'deviceid': self.deviceid,
                'platform': 2,
                'localcountry_code': 'CN'
            })

            self._jwt = resp['jwtToken']
            decoded = jwt.decode(self._jwt, options={"verify_signature": False})

            self._jwt_expire = decoded['exp']

        return self._jwt