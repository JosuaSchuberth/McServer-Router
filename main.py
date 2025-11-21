from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

connections: List[WebSocket] = []


@app.get("/")
async def root():
    return {"message": "FastAPI WebSocket-Server läuft 🚀"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast an alle verbundenen Clients
            for conn in connections:
                await conn.send_text(f"Client sagt: {data}")
    except WebSocketDisconnect:
        connections.remove(websocket)
