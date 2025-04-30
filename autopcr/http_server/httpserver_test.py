import asyncio

from .httpserver import HttpServer
from ..constants import SERVER_PORT
from ..module.crons import queue_crons

server = HttpServer(port=SERVER_PORT)

queue_crons()

server.run_forever(asyncio.get_event_loop())
