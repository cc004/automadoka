#from autopcr.core.bootstrap import create_client

from autopcr.core.pcrclient import pcrclient
from autopcr.core.sdkclient import account, platform

from autopcr.sdk.sdkclients import bsdkclient, JpGreeClient
from autopcr.core.bootstrap import create_client, create_new

from autopcr.model.models import *

FIELD_CLEAR = 612001

async def main(client: pcrclient):

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

import urllib.parse
from quart import Quart, Blueprint, request

quart_ = Quart('server')
app = Blueprint('app', 'server')

loop = asyncio.get_event_loop()

sema = asyncio.Semaphore(0)

code = None

@app.route('/')
async def callback():
    global code
    code = request.args['code']
    sema.release()
    return ''

quart_.register_blueprint(app)

PORT = 38475

query = {
    'response_type': 'code',
    'client_id': JpGreeClient.GOOGLE_ID,
    'redirect_uri' : f'http://127.0.0.1:{PORT}/',
    'state': f'{PORT}',
    'scope': 'profile',
    'service': 'lso',
    'o2v': '2',
    'flowName': 'GeneralOAuthFlow'
}

callback_url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(query)

import os
os.system(f'start "" "{callback_url}"')

async def real_main():
    try:
        print('waiting for callback...')
        await sema.acquire()
        
        sub, token = None, None
        with open('acc.txt', 'r', encoding='utf8') as fp:
            lines = fp.read().splitlines()
        for line in lines:
            client = create_client(line, '12345678')
            print(f'使用账号 {line}')
            await client.login()
            
            assert isinstance(client.session.sdk, bsdkclient)
            
            if sub is None or token is None:
                sub, token = await client.session.sdk.gclient.getGoogleToken(
                    code, f'http://127.0.0.1:{PORT}/'
                )
            
            info = await client.session.sdk.gclient.get3rdPartyInfo()
            
            if info and int(info[0]['status']):
                print('已经过，解除注册')
                await client.session.sdk.gclient.unregister3rdparty()
            
            await client.session.sdk.gclient.register3rdparty(
                sub, token
            )
            
            print('请进行网页端操作，结束后按回车键>')
            input()
            
            await client.session.sdk.gclient.unregister3rdparty()
            await main(client)
    except:
        import traceback
        traceback.print_exc()

loop.create_task(real_main())
quart_.run(port=PORT, loop=loop)

#for _ in range(10):
#    asyncio.run(run())