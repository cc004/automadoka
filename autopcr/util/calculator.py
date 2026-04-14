from ..model.models import *
from ..db.database import db
from .linq import flow
import json

class param:
    hp: int
    atk: int
    _def: int
    speed: int
    ctr: int
    ctd: int

async def generate_battle_log(self, party: PartyPartyDataRecord):
    styleMst = {
        x.styleMstId: x for x in await db.mst(MstApiGetStyleMstListRequest())
    }
    styleDict = {
        x.styleMstId: x for x in self.resp.styleDataList
    }
    cardMst = {
        x.cardMstId: x for x in await db.mst(MstApiGetCardMstListRequest())
    }
    cardDict = {
        x.cardMstId: x for x in self.resp.cardDataList
    }
    figureMst = {
        x.styleFigureMstId: x for x in await db.mst(MstApiGetStyleFigureMstListRequest())
    }
    characterMst = {
        x.characterMstId: x for x in await db.mst(MstApiGetCharacterMstListRequest())
    }
    characterDict = {
        x.characterMstId: x for x in self.resp.characterDataList
    }

    levelUpMst = (
        flow(await db.mst(MstApiGetStyleLevelUpMstListRequest()))
        .group_by(lambda x: x.styleMstId)
        .to_dict(lambda g: g.key, lambda g: list(sorted(g, key=lambda x: x.level)))
    )

    heartMst = {
        x.characterMstId: x
        for x in await db.mst(MstApiGetCharacterHeartMstListRequest())
    }
    heartParamUpMst = (
        flow(await db.mst(MstApiGetCharacterHeartParamUpGroupMstListRequest()))
        .group_by(lambda x: x.paramUpGroupId)
        .to_dict(lambda g: g.key, lambda g: list(sorted(g, key=lambda x: x.heartLevel)))
    )

    paramUpEffectMst = {
        x.styleParamUpEffectMstId: x
        for x in await db.mst(MstApiGetStyleParamUpEffectMstListRequest())
    }

    paramUpMst = (
        flow(await db.mst(MstApiGetStyleParamUpMstListRequest()))
        .group_by(lambda x: x.groupId)
        .to_dict(lambda g: g.key, lambda g: list(sorted(g, key=lambda x: x.priority)))
    )

    limitBreakMst = (
        flow(await db.mst(MstApiGetStyleLimitBreakMstListRequest()))
        .group_by(lambda x: x.styleMstId)
        .to_dict(lambda g: g.key, lambda g: list(sorted(g, key=lambda x: x.limitBreakCount)))
    )

    limitBreakEffectMst = {
        x.styleLimitBreakEffectMstId: x
        for x in await db.mst(MstApiGetStyleLimitBreakEffectMstListRequest())
    }

    def styleParam(mst: StyleStyleMstRecord, data: StyleStyleDataRecord,
                    cmst: CharacterCharacterMstRecord, cdata: CharacterCharacterDataRecord) -> param:
        levelUpBase = StyleStyleLevelUpMstRecord(
            level=1,
            maxAtk=mst.atk,
            maxDef=mst._def,
            maxHp=mst.hp,
        )
        for level in levelUpMst.get(mst.styleMstId, []):
            if level.level > data.level:
                levelUpEnd = level
                break
            levelUpBase = level
        
        paramUpEffectList: List[StyleStyleParamUpEffectMstRecord] = []

        paramUpEffectList.extend(
            paramUpEffectMst[x.styleParamUpEffectMstId]
            for x in heartParamUpMst[heartMst[cmst.characterMstId].paramUpGroupId]
            if x.heartLevel >= cdata.heartLevel
        )

        paramUpEffectList.extend(
            paramUpEffectMst[x.styleParamUpEffectMstId]
            for x in paramUpMst[mst.paramUpGroupId]
            if data.lastParamUpPriority >= x.priority
        )

        for x in limitBreakMst[mst.styleMstId]:
            if x.limitBreakCount > data.limitBreakCount: continue
            for effect in [
                limitBreakEffectMst[x.styleLimitBreakEffectMstId1],
                limitBreakEffectMst[x.styleLimitBreakEffectMstId2]
            ]:
                if effect.targetType == 1:
                    paramUpEffectList.append(StyleStyleParamUpEffectMstRecord(
                        targetType=effect.targetType,
                        abilityEffectType=effect.abilityEffectType,
                        value1=effect.value1,
                        value2=effect.value2,
                    ))
        
        ratio: float = (data.level-  levelUpBase.level) / (levelUpEnd.level - levelUpBase.level)
        result = param()
        result.hp = int(levelUpBase.maxHp + (levelUpEnd.maxHp - levelUpBase.maxHp) * ratio)
        result.atk = int(levelUpBase.maxAtk + (levelUpEnd.maxAtk - levelUpBase.maxAtk) * ratio)
        result._def = int(levelUpBase.maxDef + (levelUpEnd.maxDef - levelUpBase.maxDef) * ratio)
        result.speed = mst.speed
        result.ctr= mst.criticalRate
        result.ctd = mst.criticalDamageRate
        
        specialUpRatio = sum(
            effect.value1 for effect in paramUpEffectList
            if effect.targetType == 1 and effect.abilityEffectType == 'UP_HP_ATK_DEF_RATIO'
        ) / 1000 + 1

        result.hp = int(result.hp * specialUpRatio)
        result.atk = int(result.atk * specialUpRatio)
        result._def = int(result._def * specialUpRatio)

        return result



    units = []

    for i, style_id, sub_id, card_id in [
        (1, party.member1, int(party.subStyleMstIds1), party.cardMstId1),
        (2, party.member2, int(party.subStyleMstIds2), party.cardMstId2),
        (3, party.member3, int(party.subStyleMstIds3), party.cardMstId3),
        (4, party.member4, int(party.subStyleMstIds4), party.cardMstId4),
        (5, party.member5, int(party.subStyleMstIds5), party.cardMstId5)
    ]:
        if style_id == 0:
            continue
        
        style = styleMst[style_id]
        styleData = styleDict[style_id]
        characterId = figureMst[style.styleFigureMstId].characterMstId

        mainParam = styleParam(
            style,
            styleData,
            characterMst[characterId],
            characterDict[characterId]
        )







        units.append({
            "serializeBattleParameter": {
                "StyleMstId": style.styleMstId,
                "Speed": style.speed
            },
            "Id": i,
            "SkillSet": {
                "specialAttackMstId": styleData.specialAttackSkillInfo.skillMstId,
                "normalAttackMstId": styleData.normalAttackInfo.skillMstId,
                "activeSkillMstIds": [s.skillMstId for s in styleData.skillInfoList]
            }
        })

    return json.dumps({
        "Commands": [],
        "ResultBattleUnits": units,
        "ResultRound": 1
    })