from ..model.models import *
from .apiclient import apiclient
from .sdkclient import sdkclient
from .sessionmgr import sessionmgr
from .misc import errorhandler, mutexhandler
from .datamgr import datamgr
from enum import Enum
from ..db.database import db

class eLoginStatus(Enum):
    NOT_LOGGED = 0
    LOGGED = 1
    NEED_REFRESH = 2

class pcrclient(apiclient):
    def __init__(self, sdk: sdkclient):
        self._base_keys = {}
        self._keys = {}
        super().__init__(sdk)
        self.data = datamgr()
        self.session = sessionmgr(sdk)
        self.register(errorhandler())
        self.register(self.data)
        self.register(self.session)
        self.register(mutexhandler())

    def set_config(self, config: dict):
        self._base_keys = config
        self._keys = {}

    @property
    def id(self) -> str:
        return self.session.id

    @property
    def user_name(self) -> str:
        return self.data.user_name

    @property
    def logged(self) -> eLoginStatus:
        if not self.session._logged: return eLoginStatus.NOT_LOGGED
        else: return eLoginStatus.LOGGED

    async def login(self):
        await self.request(None)

    async def logout(self):
        await self.session.clear_session()
        self.need_refresh = False

    def _get_key(self, key, default=None):
        return self._keys.get(key, self._base_keys.get(key, default))

    @property
    def stamina_recover_cnt(self) -> int:
        return self._get_key('stamina_recover_times', 0)

    def is_stamina_consume_not_run(self):
        return self._get_key('stamina_consume_not_run', False)

    def is_stamina_get_not_run(self):
        return self._get_key('stamina_get_not_run', False)

    def is_star_cup_sweep_not_run(self):
        return self._get_key('star_cup_sweep_not_run', False)

    def is_heart_sweep_not_run(self):
        return self._get_key('heart_sweep_not_run', False)

    def is_cron_run(self):
        return self._get_key('cron_run', False)

    def set_stamina_recover_cnt(self, value: int):
        self._keys['stamina_recover_times'] = value

    def set_stamina_consume_not_run(self):
        self._keys['stamina_consume_not_run'] = True

    def set_stamina_get_not_run(self):
        self._keys['stamina_get_not_run'] = True

    def set_star_cup_sweep_not_run(self):
        self._keys['star_cup_sweep_not_run'] = True

    def set_heart_sweep_not_run(self):
        self._keys['heart_sweep_not_run'] = True

    def set_cron_run(self):
        self._keys['cron_run'] = True
