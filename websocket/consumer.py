from get_message import get_message
from websockets import WebSocketServerProtocol


async def consumer_handler(websocket: WebSocketServerProtocol):
    async for message in websocket:
        await get_message(message)
