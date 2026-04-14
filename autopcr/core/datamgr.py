from .base import Component, RequestHandler
from .apiclient import apiclient
from typing import Dict, List, Tuple
import json
from ..model.common import QuestBattleBattleUnit, ObjectObjectType, CollectionCollectionDataRecord
from ..model.responses import UserApiGetInitDataListResponse, ConfigApiGetConfigResponse
from ..model.modelbase import RequestBase, TResponse

class datamgr(Component[apiclient]):
    ready: bool = False
    user_name: str = ''
    resp: UserApiGetInitDataListResponse
    config: ConfigApiGetConfigResponse
    collection: Dict[Tuple[ObjectObjectType, int], CollectionCollectionDataRecord]

    async def request(self, request: RequestBase[TResponse], next: RequestHandler) -> TResponse:
        resp = await next.request(request)
        if resp:
            await resp.update(self, request)
        return resp

    async def generate_battle_log(self, units: List[QuestBattleBattleUnit]) -> str:
        
        return json.dumps({
            "Commands": [],
            "ResultBattleUnits": [
                {
                    "serializeBattleParameter": {
                        "StyleMstId": unit.styleMstId,
                        "ATK": unit.atk,
                        "Speed": unit.speed,
                    },
                    "Id": unit.battleUnitDataId,
                    "SkillSet": {
                        "specialAttackMstId": unit.specialAttackInfo.skillMstId,
                        "normalAttackMstId": unit.normalAttackInfo.skillMstId,
                        "activeSkillMstIds": [s.skillMstId for s in unit.attackInfoList]
                    }
                }
                for unit in units
            ],
            "ResultRound": 1
        })