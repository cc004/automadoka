import asyncio
loop = asyncio.get_event_loop()

from raid.raidrunner import main

loop.run_until_complete(main())