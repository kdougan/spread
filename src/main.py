import itertools
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from src.receiver import Receiver
from src.sockets import ConnectionManager
from threading import Thread
from multiprocessing import Queue
from src.broadcaster import Broadcaster

from src.util import get_symbol_list


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

manager = ConnectionManager()
queue = Queue()
broadcaster = Broadcaster(manager, 0.25)

symbols = get_symbol_list()
intervals = ['kline_15m', 'kline_1h',
             'kline_4h', 'kline_1w', 'kline_1M']
pairs = [f'{sym}@{interval}' for sym, interval
         in itertools.product(symbols, intervals)]

receivers = [Receiver(pairs[i: i + 200], queue)
             for i in range(0, len(pairs), 200)]


def process_queue():
    while True:
        while not queue.empty():
            broadcaster.update_data(queue.get())


@app.on_event('startup')
async def startup():
    b = Thread(target=broadcaster.run)
    b.daemon = True
    b.start()

    for receiver in receivers:
        r = Thread(target=receiver.run)
        r.daemon = True
        r.start()

    p = Thread(target=process_queue)
    p.daemon = True
    p.start()

html = open('static/index.html').read()


@app.get('/')
async def get():
    return HTMLResponse(html)


@app.websocket('/ws/{client_id}')
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            broadcaster.data.setdefault(str(client_id), []).append(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
