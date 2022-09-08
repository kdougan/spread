import asyncio
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from src.sockets import ConnectionManager
from threading import Thread
from src.broadcaster import Broadcaster
# from src.models import db

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


manager = ConnectionManager()
global_data = {}

broadcaster = Broadcaster(manager)


@app.on_event('startup')
async def create_scheduler():
    t = Thread(target=broadcaster.run)
    t.daemon = True
    t.start()

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
        await manager.broadcast(f'Client #{client_id} left the chat')
