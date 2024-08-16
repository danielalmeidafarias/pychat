from send_message import send_message
from websockets import WebSocketServerProtocol


async def producer_handler(websocket: WebSocketServerProtocol):
    while True:
        message = await send_message()
        await websocket.send(message)
