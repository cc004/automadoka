from enum import Enum
from typing import Tuple, Coroutine, Any, List, Callable, Optional
from abc import abstractmethod
from copy import deepcopy
from ..constants import DEFAULT_HEADERS, IOS_HEADERS
from ..util.logger import instance as logger
from ..model.modelbase import RequestBase

class platform(Enum):
    Android = 0,
    IOS = 1

class account:
    type: platform
    username: str
    password: str
    
    def __init__(self, usr: str, pwd: str, type: platform):
        self.username = usr
        self.password = pwd
        self.type = type

class region(Enum):
    Japan = 0,
    Global = 1,
    Sonet = 2

class sdkclient:

    def __init__(self, info: Optional[account] = None, captchaVerifier=None, logger=logger):
        self.captchaVerifier = captchaVerifier
        self.logger = logger
        self._account = info
        self.post_login_evts: List[Callable[[], Coroutine[Any, Any, None]]] = []
    
    def append_post_login(self, evt: Callable[[], Coroutine[Any, Any, None]]):
        self.post_login_evts.append(evt)

    @abstractmethod
    async def register(self, password: str) -> str: ...

    '''
    returns: uuid
    '''
    @abstractmethod
    async def login(self) ->str: ...

    @abstractmethod
    def get_crypto_key(self) -> str: ...

    @abstractmethod
    async def post_sign(self, data: bytes) -> str: ...

    async def modify_request(self, request: RequestBase):
        pass

    async def invoke_post_login(self):
        for evt in self.post_login_evts:
            await evt()
        self.post_login_evts.clear()

    def header(self):
        assert self._account is not None
        if self._account.type == platform.Android:
            headers = deepcopy(DEFAULT_HEADERS)
        elif self._account.type == platform.IOS:
            headers = deepcopy(IOS_HEADERS)
        else:
            raise ValueError(f"Invalid platform {self._account.type}")
        headers['x-game-server-url'] = self.apiroot
        return headers

    @property
    def region(self) -> region:
        ...

    @property
    def apiroot(self) -> str:
        ...

    @property
    def channel(self):
        return '1'

    @property
    def account(self):
        assert self._account is not None
        return self._account.username
