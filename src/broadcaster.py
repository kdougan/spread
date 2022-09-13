import asyncio
import json
from time import time
from time import sleep
from pydantic.json import pydantic_encoder
import orjson


class Broadcaster:
    def __init__(self, manager, interval: float = 1):
        self.manager = manager
        self.data = {}
        self.interval = interval
        self.running = False

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.running = True
        start = time()
        while self.running:
            if time() - start > self.interval:
                start = time()
                loop.run_until_complete(self.broadcast())
            sleep(0.001)
        loop.close()

    async def broadcast(self):
        json_data = json.dumps(self.data, default=pydantic_encoder)
        await self.manager.broadcast(json_data)
