import asyncio
import time

import websockets  # pip install websockets


SERVER_URL = "ws://127.0.0.1:8000/ws"


async def ping_loop():
    async with websockets.connect(SERVER_URL) as websocket:
        print("Mit WebSocket verbunden")

        while True:
            client_ts = time.time()
            await websocket.send(f"ping:{client_ts}")
            msg = await websocket.recv()
            try:
                msg_type, client_ts_str, server_ts_str = msg.split(":")
                if msg_type != "pong":
                    continue
            except ValueError:
                continue

            client_ts_recv = float(client_ts_str)
            server_ts = float(server_ts_str)
            now = time.time()

            rtt = now - client_ts_recv
            upstream = server_ts - client_ts_recv
            downstream = now - server_ts

            print(
                f"RTT: {rtt * 1000:.1f} ms | "
                f"up: {upstream * 1000:.1f} ms | "
                f"down: {downstream * 1000:.1f} ms"
            )
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(ping_loop())
