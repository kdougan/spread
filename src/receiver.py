import asyncio
import websockets
import json
from multiprocessing import Queue

from src.schema import Kline


class Receiver:
    def __init__(self, queue: Queue):
        self.uri = 'wss://fstream.binance.com/ws'
        self.queue = queue
        self.running = False
        self.payload = {
            'method': 'SUBSCRIBE',
            'params':
            [
                'btcusdt@kline_15m',
                'btcusdt@kline_1h',
                'btcusdt@kline_4h',
                'btcusdt@kline_1w',
                'btcusdt@kline_1M'
            ],
            'id': 1
        }

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.receive())

    async def receive(self):
        async with websockets.connect(self.uri, ssl=True) as sock:
            await sock.send(json.dumps(self.payload))
            try:
                while True:
                    async for message in sock:
                        try:
                            kline = Kline(**json.loads(message))
                            self.queue.put(kline)
                        except Exception as e:
                            print(e)
            except websockets.ConnectionClosed as e:
                print('ERR', e)
