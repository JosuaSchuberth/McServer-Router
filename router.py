from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio


app = FastAPI()
host_ws = None
client_ws = None
pair_event = asyncio.Event()

async def pipe(server, client):
    async def server_to_client():
        async for data in server:
            await client.send(data)

    async def client_to_server():
        async for data in client:
            await server.send(data)

    await asyncio.gather(server_to_client(), client_to_server())                

@app.websocket("/host")
async def host_endpoint(ws: WebSocket):
    global host_ws
    await ws.accept()
    host_ws = ws
    if client_ws is not None:
        pair_event.set()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        pass

    
@app.websocket("/client")
async def client_endpoint(ws: WebSocket):
    global client_ws
    await ws.accept()
    client_ws = ws
    if host_ws is not None:
        pair_event.set()

    await pair_event.wait()
    await pipe(host_ws, client_ws)

