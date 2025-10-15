import asyncio
from autopcr.core.bootstrap import create_new
from autopcr.sdk.sdkclients import qsdkclient

asyncio.run(create_new('12345678', qsdkclient))