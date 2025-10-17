from ..model.models import *
from .apiclient import apiclient
from .sdkclient import sdkclient
from .sessionmgr import sessionmgr
from .misc import errorhandler, mutexhandler
from .datamgr import datamgr
from enum import Enum
from ..db.database import db
from datetime import datetime, timedelta, timezone
from ..constants import USER_TZ as user_tz

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

    async def clear_tutorial(self):
        await self.login()
        # 注意：原 C# 中 client.AccessHome() 是同步方法，这里保留同名调用
        self.access_home()

        await self.request(TutorialApiSkipTutorialToGachaRequest())

        gacha_result = await self.request(GachaApiGachaExecRequest(
            gachaMstId=240925001
        ))

        await self.request(TutorialApiUpdateTutorialStepRequest(tutorialStep=1900))

        present = await self.request(PresentApiGetPresentDataListRequest(
            expireTimeType=0,
            isOrderNewest=False
        ))

        # 收礼物 id 列表并接收
        present_ids = [d.presentDataId for d in present.presentDataList]
        if present_ids:
            await self.request(PresentApiReceiveRequest(
                presentDataIds=present_ids
            ))

        await self.request(TutorialApiUpdateTutorialStepRequest(tutorialStep=1950))

        recommend = await self.request(PartyApiGetRecommendPartyDataRequest(
            selectedStyleElement=0,
            selectedParameter=0,
            isSettingCard=True,
            isSettingSubStyle=True,
            sameCharacterInParty=True
        ))

        # 保存推荐队伍（把 recommend.recommendPartyData 的字段映射过去）
        rp = recommend.recommendPartyData
        await self.request(PartyApiSavePartyForRecommendRequest(
            partyType=1,
            partyDataId=0,
            partyIndex=0,
            styleMstId1=rp.member1,
            styleMstId2=rp.member2,
            styleMstId3=rp.member3,
            styleMstId4=rp.member4,
            styleMstId5=rp.member5,
            cardMstId1=rp.cardMstId1,
            cardMstId2=rp.cardMstId2,
            cardMstId3=rp.cardMstId3,
            cardMstId4=rp.cardMstId4,
            cardMstId5=rp.cardMstId5,
            subStyleMstIds1=[0],
            subStyleMstIds2=[0],
            subStyleMstIds3=[0],
            subStyleMstIds4=[0],
            subStyleMstIds5=[0],
        ))

        # 一系列教程进度更新
        await self.request(TutorialApiUpdateTutorialStepRequest(tutorialStep=2000))
        await self.request(TutorialApiUpdateTutorialStepRequest(tutorialStep=2030))
        await self.request(TutorialApiUpdateTutorialStepRequest(tutorialStep=2060))

        await self.request(UserApiSetNameRequest(name='木谷高明'))

        await self.request(TutorialApiUpdateTutorialStepRequest(tutorialStep=2100))
        await self.request(TutorialApiUpdateTutorialStepRequest(tutorialStep=2200))

        await self.request(HomeApiGetHomeInfoRequest())

    def raid_stamina(self, staminaData: MultiRaidMultiRaidUserDataRecord) -> int:
        config = self.data.config.multiRaidConfig
        if staminaData.stamina >= config.maxStamina:
            return staminaData.stamina
        now = datetime.now(tz=user_tz)
        update = datetime.fromisoformat(staminaData.staminaUpdatedTime).astimezone(user_tz)
        delta = now - update
        v40 = int(delta.total_seconds()) // config.staminaRecoverSec
        v42 = (config.maxStamina - staminaData.stamina) // config.staminaRecoverNum
        if v40 <= v42: v42 = v40
        return staminaData.stamina + v42 * config.staminaRecoverNum

    def stamina(self, userParamData: Optional[UserUserParamDataRecord] = None) -> int:
        config = self.data.config.userConfig
        if userParamData is None:
            userParamData = self.data.resp.userParamData
        if userParamData.stamina >= config.staminaUpperLimit:
            return userParamData.stamina
        now = datetime.now(tz=user_tz)
        update = datetime.fromisoformat(userParamData.staminaUpdatedTime).astimezone(user_tz)
        delta = now - update
        recover_times = int(delta.total_seconds()) // config.staminaRecoverSec
        return min(userParamData.stamina + recover_times, config.staminaUpperLimit)
