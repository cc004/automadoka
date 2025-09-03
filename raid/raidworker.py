from autopcr.core import pcrclient
from autopcr.core.sdkclient import account, platform
from autopcr.sdk.sdkclients import bsdkclient
from autopcr.model.models import *
from typing import Tuple

class raidworker:
    def __init__(self, code, password, alias):
        self.client = pcrclient(
            bsdkclient(account(code, password, platform.Android))
        )
        self.alias = alias
        self.logger = lambda x: print(x)
    
    async def prepare(self):
        self.logger(f"[{self.alias}] Logging in...")
        await self.client.login()
        self.logger(f"[{self.alias}] Logged in.")
    
    async def now_stamina(self) -> int:
        resp = await self.client.request(MultiRaidApiGetTopRequest())
        return resp.multiRaidUserData.stamina

    async def do_monitor(self) -> List[MultiRaidMultiRaidStageDataRecord]:
        resp = await self.client.request(MultiRaidApiGetTopRequest())
        return resp.multiRaidStageDataList

    async def add_damage(self, multiRaidStageDataRecord: MultiRaidMultiRaidStageDataRecord, damage: int) -> Tuple[
        MultiRaidApiInitializeStageResponse,
        MultiRaidApiAddDamageResponse,
        MultiRaidApiRetireResponse
    ]:
        resp = await self.client.request(MultiRaidApiInitializeStageRequest(
            partyDataId=1,
            rescueType=0,
            multiRaidStageMstId=multiRaidStageDataRecord.multiRaidStageMstId,
            multiRaidStageDataId=multiRaidStageDataRecord.multiRaidStageDataId
        ))
        resp2 = await self.client.request(MultiRaidApiAddDamageRequest(
            questDataId=resp.multiRaidRoomData.questDataId,
            damage=damage
        ))
        resp3 = await self.client.request(MultiRaidApiRetireRequest(
            questDataId=resp.multiRaidRoomData.questDataId,
            battleLog=''
        ))
        return (resp, resp2, resp3)