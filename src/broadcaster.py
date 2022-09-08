import asyncio
from time import time
from time import sleep

import orjson


class Broadcaster:
    def __init__(self, manager):
        self.manager = manager
        self.data = {}
        self.running = False

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.running = True
        start = time()
        while self.running:
            if time() - start > 1:
                start = time()
                loop.run_until_complete(self.broadcast())
            sleep(0.001)
        loop.close()

    async def broadcast(self):
        json_data = orjson.dumps(self.data, option=orjson.OPT_NAIVE_UTC)
        await self.manager.broadcast(json_data.decode('utf-8'))
