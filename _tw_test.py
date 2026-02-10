
from autopcr.core.pcrclient import pcrclient
from typing import Type
from autopcr.core.sdkclient import account, platform, sdkclient
from autopcr.sdk.sdkclients import sonetsdkclient
from autopcr.model.models import *

async def create_new() -> pcrclient:
    sdk = sonetsdkclient()
    await sdk.register('12345678')
    
    client = pcrclient(sdk)

    await client.login()

    return client

def pretty_print(data: ObjectStyleGainViewData) -> Tuple[str, int]:
    style = style_dict[data.styleMstId]
    character = char_dict[data.styleMstId // 10000]
    rarity = int(style.rarity)
    sb = []
    sb.append(' ' * (5 - rarity))
    sb.append('*' * rarity)
    sb.append("    ")

    sb.append(f"[{style.name}] {character.name}")

    if data.isNew:
        sb.append(" new!")

    return (''.join(sb), rarity)

async def main():
    client = await create_new()
    global style_dict, char_dict
    logger = open('tw_users.txt', 'a', encoding='utf-8')

    style_dict = {
        x.styleMstId: x
        for x in (await client.request(MstApiGetStyleMstListRequest())).mstList
    }
    char_dict = {
        x.characterMstId: x
        for x in (await client.request(MstApiGetCharacterMstListRequest())).mstList
    }

    async def work_once():
        client = await create_new()
        info = []
        cnt = 0
        gacha_result = await client.clear_tutorial_gacha()
        assert client.session.sdk._account is not None

        for data in gacha_result:
            s, r = pretty_print(data)
            if r == 5:
                info.append(s + ',')
                cnt += 1
        
        if cnt > 2:
            print('got 5 starts: ', cnt)
            info = [client.session.sdk._account.username + ',', f'{cnt},'] + info
            logger.write(''.join(info) + '\n')
            logger.flush()
    
    async def worker():
        while True:
            try:
                await work_once()
            except Exception as e:
                print('Error occurred:', e)
    
    workers = [asyncio.create_task(worker()) for _ in range(64)]

    await asyncio.gather(*workers)

import asyncio

asyncio.run(main())