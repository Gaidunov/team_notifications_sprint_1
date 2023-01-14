import asyncio
import websockets

uri = "ws://localhost:8765"

async def spammer():
    async with websockets.connect(uri) as websocket:
        name = await websocket.recv()
        print(f"Моё имя на сервере: {name}")
        while True:
            await websocket.send("Хулиганское сообщение")
            await asyncio.sleep(0.1)

loop = asyncio.get_event_loop()
loop.run_until_complete(spammer())
