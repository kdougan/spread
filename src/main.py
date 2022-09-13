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

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


manager = ConnectionManager()
queue = Queue()
broadcaster = Broadcaster(manager, 0.25)
receiver = Receiver(queue)


def process_queue():
    while True:
        while not queue.empty():
            message = queue.get()
            broadcaster.data = message


@app.on_event('startup')
async def startup():
    t1 = Thread(target=broadcaster.run)
    t1.daemon = True
    t1.start()

    t2 = Thread(target=receiver.run)
    t2.daemon = True
    t2.start()

    t3 = Thread(target=process_queue)
    t3.daemon = True
    t3.start()

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
