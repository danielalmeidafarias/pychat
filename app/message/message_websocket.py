import asyncio
import json

import websockets

async def handler(websocket):
    while True:
        message = await websocket.recv()
        print(message)
        await websocket.send(json.dumps({
            "test": 'testing'
        }))


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
