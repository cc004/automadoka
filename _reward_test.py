#from autopcr.core.bootstrap import create_client

#client = create_client('KQEQPETWNARVHYA2', '12345678')

from autopcr.core.pcrclient import pcrclient
from autopcr.core.sdkclient import account, platform

from autopcr.sdk.sdkclients import bsdkclient, JpGreeClient
from autopcr.core.bootstrap import create_client, create_new

from autopcr.model.models import *

FIELD_CLEAR = 612001

async def main(client: pcrclient):

    await client.login()

    invite_top = await client.request(InvitationApiGetTopRequest())

    if not invite_top.inviterPlayerId:
        await client.request(InvitationApiInviteRequest(
            invitationCampaignMstId=1,
            inviterPlayerId='77464662337J'
        ))

    stratum = (await client.request(MstApiGetFieldStratumMstListRequest())).mstList
    point = (await client.request(MstApiGetFieldPointMstListRequest())).mstList
    field_mst = {
        x.fieldStageMstId: x for x in (await client.request(MstApiGetFieldStageMstListRequest())).mstList
    }

    top = await client.request(ExplorationApiGetFieldStageCollectionInfoListRequest())
    cleared_field = set(x.fieldStageMstId for x in top.fieldStageCollectionInfoList if x.isClear)

    async def clear_field(field: int):
        mst = field_mst[field]
        if field in cleared_field:
            print(f"跳过已通关篇章 {field} ({mst.name})")
            return
        if mst.prevFieldStageMstId != 0:
            await clear_field(mst.prevFieldStageMstId)
        print(f"开始清理 {field} ({mst.name})")
        top = await client.request(ExplorationApiGetTopInfoV4Request(
            fieldStageMstId=field
        ))
    
        if top.fieldStageUserData.clearFieldPointMstIdCsv:
            cleared_points = set(int(x) for x in top.fieldStageUserData.clearFieldPointMstIdCsv.split(','))
        else:
            cleared_points = set()
        
        stratums = [x for x in stratum if x.fieldStageMstId == field]

        for s in stratums:
            points = [x for x in point if x.fieldStratumMstId == s.fieldStratumMstId]
            for p in points:
                if p.fieldPointMstId in cleared_points:
                    print(f"跳过已通关点 {p.fieldPointMstId} ({mst.name}-{p.name})")
                    continue
                reach = await client.request(ExplorationApiReachFieldPointRequest(
                    fieldPointMstId=p.fieldPointMstId
                ))
                print(f"到达点 {p.fieldPointMstId} ({mst.name}-{p.name})")

                if p.pointType == 1: # dungeon
                    start = await client.request(ExplorationApiDungeonStartRequest(
                        fieldStageMstId=s.fieldStageMstId,
                        dungeonMstId=p.pointValue1
                    ))
                    finish = await client.request(ExplorationApiDungeonGoalRequest(
                        fieldStageMstId=s.fieldStageMstId,
                        dungeonMstId=p.pointValue1
                    ))
                    print(f"完成副本点 {p.fieldPointMstId} ({mst.name}-{p.name})")
                elif p.pointType == 2 or p.pointType == 3 or p.pointType == 4: # start
                    quest = await client.request(ExplorationBattleApiInitializeStageV4Request(
                        fieldPointMstId=p.fieldPointMstId,
                        fieldStageMstId=s.fieldStageMstId,
                        dungeonEventMstId=0,
                        dungeonRoomMstId=0,
                        bossDirectionMstId=0,
                        presetEventIndex=0,
                        partyDataId=1
                    ))
                    await asyncio.sleep(2)
                    finish = await client.request(ExplorationBattleApiFinalizeStageForUserV4Request(
                        autoMode=1,
                        battleLog="",
                        result=1
                    ))
                    print(f"完成战斗点 {p.fieldPointMstId} ({mst.name}-{p.name})")

    await clear_field(FIELD_CLEAR)



import asyncio


async def run():
    client = await create_new('12345678')

    with open('acc.txt', 'a', encoding='utf8') as fp:
        fp.write(f'{client.session.sdk.account}\n')
    
    await main(client)

with open('acc.txt', 'r', encoding='utf8') as fp:
    lines = fp.read().splitlines()
for line in lines:
    client = create_client(line, '12345678')
    print(f'使用账号 {line}')
    asyncio.run(main(client))

#for _ in range(10):
#    asyncio.run(run())