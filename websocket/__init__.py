import asyncio
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK, ConnectionClosedError
from urllib.parse import urlparse, parse_qs

connected = {}


async def handle_connection(websocket: WebSocketServerProtocol):
    user_id = websocket.request_headers.get('id')
    path = websocket.path

    recipient_id = parse_qs(urlparse(path).query).get('recipient_id')

    if user_id in connected:
        return await websocket.close(1008, f"user {user_id} already connected")

    connected[user_id] = websocket

    try:
        async for message in websocket:
            if recipient_id in connected:
                recipient_websocket = connected[recipient_id]
                await recipient_websocket.send(message)
            else:
                await websocket.send('Salvar no db')
    except ConnectionClosed:
        print(f"Connection closed for user_id: {user_id}")
    finally:
        if user_id in connected:
            del connected[user_id]


async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
