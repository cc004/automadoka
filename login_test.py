from autopcr.core.bootstrap import create_client, qsdkclient

import asyncio


async def main():
    client = create_client('PP8SV3YJKH2W8CFY', 'qwopas123', qsdkclient)

    await client.login()

asyncio.run(main())