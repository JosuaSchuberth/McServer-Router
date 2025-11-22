import asyncio
import websockets

MC_SERVER_HOST = "127.0.0.1"
MC_SERVER_PORT = 25565

WS_URL = "wss://DEIN-RELAY-URL_HIER/host"


async def run_tunnel():
    reader, writer = await asyncio.open_connection(MC_SERVER_HOST, MC_SERVER_PORT)
    print("[TCP] Connected to Minecraft-Server")

    try:
        async with websockets.connect(
            WS_URL,
            ping_interval=None,
            max_size=None
        ) as ws:
            print("[WS] Connected with relay")

            async def tcp_to_ws():
                try:
                    while True:
                        data = await reader.read(4096)
                        await ws.send(data)
                except Exception as e:
                    print(f"[tcp_to_ws] Error: {e}")
                    await ws.close()

            async def ws_to_tcp():
                try:
                    async for message in ws:
                        data = message
                        writer.write(data)
                        await writer.drain()
                except websockets.ConnectionClosed:
                    print("[WS] Relay connection closed")
                except Exception as e:
                    print(f"[ws_to_tcp] Error: {e}")
                finally:
                    writer.close()
                    await writer.wait_closed()
            await asyncio.gather(tcp_to_ws(), ws_to_tcp())

    except Exception as e:
        print(f"[run_tunnel] Error: {e}")
        writer.close()
        await writer.wait_closed()


async def main():
    while True:
        try:
            await run_tunnel()
        except Exception as e:
            print(f"[MAIN] Error: {e}")
        print("[MAIN] Retry...")
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
