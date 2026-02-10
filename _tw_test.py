from autopcr.core.bootstrap import create_new
from autopcr.sdk.sdkclients import sonetsdkclient
from autopcr.model.requests import *

async def main():
    client = await create_new('12345678', sonetsdkclient)

    resp = await client.request(StyleApiGetStyleDataListRequest())
    print('characters:' + ','.join(
        str(x.styleMstId) for x in resp.styleDataList
    ))

    assert client.session.sdk._account is not None

    print(client.session.sdk._account.username)

import asyncio

asyncio.run(main())