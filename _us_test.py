import asyncio
from autopcr.core.bootstrap import create_client
from autopcr.sdk.sdkclients import qsdkclient

client = create_client('MW8T67FVCQWMKL5D', '187385qq', qsdkclient)

async def main():
    await client.login()
    print(client.data.resp.userParamData.userId)

asyncio.run(main())