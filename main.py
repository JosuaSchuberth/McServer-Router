from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import time

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "FastAPI WebSocket Ping/Pong läuft 🚀"}


@app.websocket("/ws")
async def websocket_ping_pong(websocket: WebSocket):
    await websocket.accept()
    print("Client verbunden")

    try:
        while True:
            message = await websocket.receive_text()
            if not message.startswith("ping:"):
                continue

            parts = message.split(":", 1)
            try:
                client_ts = float(parts[1])
            except (IndexError, ValueError):
                continue

            server_ts = time.time()
            await websocket.send_text(f"pong:{client_ts}:{server_ts}")

    except WebSocketDisconnect:
        print("Client getrennt")
