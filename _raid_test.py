from autopcr.sdk.sdkclients import bsdkclient
from autopcr.core import pcrclient
from autopcr.core.sdkclient import account, platform
from autopcr.model.models import *
import asyncio


async def main():
    client = pcrclient(bsdkclient(account(
        '856NFGFHDG52YJ3X',
        '12345678',
        platform.Android
    )))

    await client.login()

    resuced = await client.request(MultiRaidApiGetMultiRaidStageDataListRequest(isRescue=False))

    print(resuced)

asyncio.run(main())