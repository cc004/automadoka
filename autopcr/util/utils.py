from typing import List
from ..model.models import StyleStyleDataRecord
import json

def generate_battle_log(units: List[StyleStyleDataRecord]):
    obj = {
            "Commands": [],
            "ResultBattleUnits": [
                {
                    "serializeBattleParameter": {
                        "StyleMstId": x.styleMstId,
                    },
                    "Id": i + 1,
                    "SkillSet": {
                        "specialAttackMstId": x.specialAttackSkillInfo.skillMstId,
                        "normalAttackMstId": x.normalAttackInfo.skillMstId
                    }
                }
                for i, x in enumerate(units)
            ],
            "ResultRound": 1
    }
    
    return json.dumps(obj)