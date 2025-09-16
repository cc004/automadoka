from autopcr.core import pcrclient
from autopcr.core.sdkclient import account, platform
from autopcr.sdk.sdkclients import bsdkclient
from autopcr.model.models import *
from typing import Tuple
from .utils import stamina_calc
import asyncio

class raidworker:
    def __init__(self, code, password, alias):
        self.client = pcrclient(
            bsdkclient(account(code, password, platform.Android))
        )
        self.alias = alias
        self.logger = lambda x: print(x)
        self.prepared = False
    
    @staticmethod
    def from_client(client: pcrclient, alias: str):
        worker = raidworker('', '', alias)
        worker.client = client
        worker.prepared = True
        return worker
    
    async def prepare(self):
        if self.prepared:
            return
        self.logger(f"[{self.alias}] Logging in...")
        await self.client.login()
        self.logger(f"[{self.alias}] Logged in.")
    
    async def now_stamina(self) -> int:
        resp = await self.client.request(MultiRaidApiGetTopRequest())
        return stamina_calc(resp.multiRaidUserData.stamina, resp.multiRaidUserData.staminaUpdatedTime,
                            self.client.data.config.multiRaidConfig)

    async def do_monitor(self) -> List[MultiRaidMultiRaidStageDataRecord]:
        resp = await self.client.request(MultiRaidApiGetTopRequest())
        return resp.multiRaidStageDataList

    async def ensure_exited(self):
        top = await self.client.request(MultiRaidApiGetTopRequest())
        my_room = next(
            (
                room for room in top.multiRaidRoomDataList
                if room.userId == self.client.data.resp.userParamData.userId and not room.isClosed
            ),
            None
        )
        if my_room is not None:
            await self.client.request(MultiRaidApiRetireRequest(
                questDataId=my_room.questDataId,
                battleLog=''
            ))
            self.logger(f"[{self.alias}] Exited raid room {my_room.questDataId}.")

    async def add_damage(self, multiRaidStageDataRecord: MultiRaidMultiRaidStageDataRecord, damage: int) -> Tuple[
        MultiRaidApiInitializeStageResponse,
        MultiRaidApiAddDamageResponse,
        MultiRaidApiRetireResponse
    ]:
        await self.ensure_exited()
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
    async def start_clear(self, multiRaidStageMstId: int, partyDataId: int, rescueType: int, waitTime: int, damage: int, battleLog: str,
                          result: int) -> Tuple[
        MultiRaidApiInitializeStageResponse,
        MultiRaidApiAddDamageResponse,
        MultiRaidApiFinalizeStageForUserResponse
    ]:
        # await self.ensure_exited()
        resp = await self.client.request(MultiRaidApiInitializeStageRequest(
            partyDataId=partyDataId,
            rescueType=rescueType,
            multiRaidStageMstId=multiRaidStageMstId,
            multiRaidStageDataId=0
        ))
        resp2 = await self.client.request(MultiRaidApiAddDamageRequest(
            questDataId=resp.multiRaidRoomData.questDataId,
            damage=damage
        ))
        resp3 = await self.client.request(MultiRaidApiFinalizeStageForUserRequest(
            questDataId=resp.multiRaidRoomData.questDataId,
            battleLog=battleLog,
            autoMode=0,
            result=result
        ))
        return (resp, resp2, resp3)
    async def support_clear(self, multiRaidStageDataRecord: MultiRaidMultiRaidStageDataRecord, partyDataId: int,
                          waitTime: int, damage: int, battleLog: str, result: int) -> Tuple[
        MultiRaidApiInitializeStageResponse,
        MultiRaidApiAddDamageResponse,
        MultiRaidApiFinalizeStageForUserResponse
    ]:
        # await self.ensure_exited()
        resp = await self.client.request(MultiRaidApiInitializeStageRequest(
            partyDataId=partyDataId,
            rescueType=0,
            multiRaidStageMstId=multiRaidStageDataRecord.multiRaidStageMstId,
            multiRaidStageDataId=multiRaidStageDataRecord.multiRaidStageDataId
        ))
        resp2 = await self.client.request(MultiRaidApiAddDamageRequest(
            questDataId=resp.multiRaidRoomData.questDataId,
            damage=damage
        ))
        if damage >= multiRaidStageDataRecord.hp:
            result = 1 # force to win if overkill
        resp3 = await self.client.request(MultiRaidApiFinalizeStageForUserRequest(
            questDataId=resp.multiRaidRoomData.questDataId,
            battleLog=battleLog,
            autoMode=0,
            result=result
        ))
        return (resp, resp2, resp3)