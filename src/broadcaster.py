import asyncio
from time import time
from time import sleep
from pydantic.json import pydantic_encoder
import orjson

from src.schema import Ticker, Kline


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
        json_data = orjson.dumps(
            self.data, default=pydantic_encoder).decode('utf-8')
        await self.manager.broadcast(json_data)

    def update_data(self, data: dict):
        if 's' in data:
            kline = Kline(**data)
            self.data.setdefault(
                kline.symbol,
                Ticker(symbol=kline.symbol, kline={})
            )
            self.data[kline.symbol].kline[kline.data.interval] = kline.data
