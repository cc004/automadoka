from ..sdk.sdkclients import bsdkclient
from .pcrclient import pcrclient
from .sdkclient import account, platform

def create_client(usr: str, pwd: str):
    sdk = bsdkclient(account(
        usr=usr,
        pwd=pwd,
        type=platform.Android
    ))

    return pcrclient(sdk)

async def create_new(pwd: str):
    sdk = bsdkclient(None)
    await sdk.register('12345678')
    
    client = pcrclient(sdk)

    await client.login()

    await client.clear_tutorial()

    return client