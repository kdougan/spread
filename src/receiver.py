import asyncio
import itertools
import websockets
import orjson
from multiprocessing import Queue


class Receiver:
    def __init__(self, symbols: list[str], queue: Queue):
        self.uri = 'wss://fstream.binance.com/ws'
        self.queue = queue
        self.running = False

        self.payload = orjson.dumps({
            'method': 'SUBSCRIBE',
            'params': symbols,
            'id': 1
        }).decode('utf-8')

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.receive())

    async def receive(self):
        async with websockets.connect(self.uri, ssl=True) as sock:
            await sock.send(self.payload)
            try:
                while True:
                    async for message in sock:
                        try:
                            self.queue.put(orjson.loads(message))
                        except Exception as e:
                            print(e, message)
            except websockets.ConnectionClosed as e:
                print('ERR', e)
