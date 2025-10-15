from ..sdk.sdkclients import bsdkclient, sdkclientbase
from .pcrclient import pcrclient
from typing import Type
from .sdkclient import account, platform

def create_client(usr: str, pwd: str, client_type: Type[sdkclientbase]=bsdkclient) -> pcrclient:
    sdk = client_type(account(
        usr=usr,
        pwd=pwd,
        type=platform.Android
    ))

    return pcrclient(sdk)

async def create_new(pwd: str, client_type: Type[sdkclientbase]=bsdkclient) -> pcrclient:
    sdk = client_type(None)
    await sdk.register('12345678')
    
    client = pcrclient(sdk)

    await client.login()

    await client.clear_tutorial()

    return client