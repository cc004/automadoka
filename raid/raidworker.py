from autopcr.core import pcrclient
from autopcr.core.sdkclient import account, platform, sdkclient
from autopcr.model.models import *
from typing import List, Tuple, Type
import asyncio

# 单次 MultiRaidApiAddDamageRequest 能提交的伤害上限，超了要拆成几包
DAMAGE_ONCE = 1000_0000

class raidworker:
    def __init__(self, code, password, alias, sdkclient: Type[sdkclient]):
        self.client = pcrclient(
            sdkclient(account(code, password, platform.Android))
        )
        self.alias = alias
        self.logger = lambda x: print(x)
        self.prepared = False
    
    @staticmethod
    def from_client(client: pcrclient, alias: str):
        worker = raidworker('', '', alias, client.session.sdk.__class__)
        worker.client = client
        worker.prepared = True
        return worker
    
    async def prepare(self):
        if self.prepared:
            return
        try:
            self.logger(f"[{self.alias}] Logging in...")
            await self.client.login()
            self.logger(f"[{self.alias}] Logged in.")
        except Exception as e:
            self.logger(f"[{self.alias}] Login failed.")
            import traceback
            traceback.print_exc()
            raise
    
    async def now_stamina(self) -> int:
        return self.client.raid_stamina(
            (await self.client.request(MultiRaidApiGetTopRequest())).multiRaidUserData
        )

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
        while damage > 0:
            dmg = min(damage, DAMAGE_ONCE)
            damage -= dmg
            resp2 = await self.client.request(MultiRaidApiAddDamageRequest(
                questDataId=resp.multiRaidRoomData.questDataId,
                damage=dmg
            ))
        resp3 = await self.client.request(MultiRaidApiRetireRequest(
            questDataId=resp.multiRaidRoomData.questDataId,
            battleLog=''
        ))
        return (resp, resp2, resp3)
    async def start_clear(self, multiRaidStageMstId: int, partyDataId: int, rescueType: int, waitTime: int, damage: int,
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
        info = await self.client.request(MultiRaidApiGetMultiRaidInfoRequest(
            questDataId=resp.multiRaidRoomData.questDataId
        ))
        resp2 = await self.client.request(MultiRaidApiAddDamageRequest(
            questDataId=resp.multiRaidRoomData.questDataId,
            damage=damage
        ))
        resp3 = await self.client.request(MultiRaidApiFinalizeStageForUserRequest(
            questDataId=resp.multiRaidRoomData.questDataId,
            battleLog=await self.client.data.generate_battle_log(info.allyBattleUnitList),
            autoMode=0,
            result=result
        ))
        return (resp, resp2, resp3)

    # ------------------------------------------------------------------
    # 下面三个是「魔女召唤」重写时拆出来的原子步骤：
    # 新开房间 / 接手已有房间 / 发伤害 / 结算，分开就能复用同一套结算逻辑。
    # ------------------------------------------------------------------
    async def open_room(self, stage_mst_id: int, party_data_id: int, rescue_type: int) -> Tuple[
        int, int, List
    ]:
        """新开一个团战房间（不结算）。

        返回 ``(questDataId, boss 剩余 HP, 己方战斗单位)``。
        """
        resp = await self.client.request(MultiRaidApiInitializeStageRequest(
            partyDataId=party_data_id,
            rescueType=rescue_type,
            multiRaidStageMstId=stage_mst_id,
            multiRaidStageDataId=0
        ))
        quest_data_id = resp.multiRaidRoomData.questDataId
        info = await self.client.request(MultiRaidApiGetMultiRaidInfoRequest(
            questDataId=quest_data_id
        ))
        return quest_data_id, resp.multiRaidStageData.hp, info.allyBattleUnitList

    async def sync_room(self, quest_data_id: int) -> Tuple[int, List]:
        """接手一个已经存在的房间，返回 ``(boss 剩余 HP, 己方战斗单位)``。"""
        info = await self.client.request(MultiRaidApiGetMultiRaidInfoRequest(
            questDataId=quest_data_id
        ))
        return info.multiRaidStageData.hp, info.allyBattleUnitList

    async def send_damage(self, quest_data_id: int, damage: int) -> None:
        """分块把伤害打进去：单包上限 `DAMAGE_ONCE`，超了就拆开。"""
        remaining = int(damage)
        while remaining > 0:
            chunk = min(remaining, DAMAGE_ONCE)
            remaining -= chunk
            await self.client.request(MultiRaidApiAddDamageRequest(
                questDataId=quest_data_id,
                damage=chunk
            ))

    async def finalize_room(self, quest_data_id: int, ally_units: List, result: int) -> \
            MultiRaidApiFinalizeStageForUserResponse:
        """结算房间，battleLog 按己方战斗单位现推。"""
        return await self.client.request(MultiRaidApiFinalizeStageForUserRequest(
            questDataId=quest_data_id,
            battleLog=await self.client.data.generate_battle_log(ally_units),
            autoMode=0,
            result=result
        ))
    async def support_clear(self, multiRaidStageDataRecord: MultiRaidMultiRaidStageDataRecord, partyDataId: int,
                          waitTime: int, damage: int, result: int) -> Tuple[
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
        info = await self.client.request(MultiRaidApiGetMultiRaidInfoRequest(
            questDataId=resp.multiRaidRoomData.questDataId
        ))
        
        resp2 = await self.client.request(MultiRaidApiAddDamageRequest(
            questDataId=resp.multiRaidRoomData.questDataId,
            damage=damage
        ))
        if damage >= multiRaidStageDataRecord.hp:
            result = 1 # force to win if overkill
            
        resp3 = await self.client.request(MultiRaidApiFinalizeStageForUserRequest(
            questDataId=resp.multiRaidRoomData.questDataId,
            battleLog=await self.client.data.generate_battle_log(info.allyBattleUnitList),
            autoMode=0,
            result=result
        ))
        return (resp, resp2, resp3)