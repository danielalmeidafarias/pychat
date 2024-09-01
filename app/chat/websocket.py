from flask_socketio import SocketIO
from flask import request, Flask
from ..auth.util import AuthFunctions
from typing import List
from ..chat.repository import ChatRepository
from ..message.repository import MessageRepository
from ..user.repository import UserRepository
from flask_sqlalchemy import SQLAlchemy
from ..message.schemas import CreateMessageSchema
from marshmallow.exceptions import ValidationError
from ..middlewares.auth_ws_middleware import auth_ws_middleware


class ChatWebsocket(SocketIO):
    def __init__(self, app: Flask, cors_allowed_origins, db: SQLAlchemy):
        super().__init__(app=app, cors_allowed_origins=cors_allowed_origins)

        self.register_handlers()

        self.connected = {}
        self.auth_functions = AuthFunctions()
        self.chat_repository = ChatRepository(db)
        self.message_repository = MessageRepository(db)
        self.user_repository = UserRepository(db)

    def register_handlers(self):
        @self.on('connect')
        @auth_ws_middleware
        def on_connect():
            socketio_id = request.sid

            authorization_cookies = request.cookies.get('authorization')
            user_id = self.auth_functions.decode_jwt(authorization_cookies)['user_id']

            self.connected[user_id] = socketio_id

            self.emit("connected successfully")

        @self.on('disconnect')
        def on_disconnect():
            self.emit("disconnected successfully")

            self.connected = {
                user_id: socketio_id for user_id, socketio_id in self.connected.items() if socketio_id != request.sid
            }

            connected_values: List = self.connected.values()
            connected_key: List = self.connected.items()

            for value in connected_values:
                if value == request.sid:
                    index = connected_values.index(value)
                    self.connected.pop(connected_key[index])

        @self.on('message')
        def on_message(data):
            authorization_cookies = request.cookies.get('Auth')

            user_id = self.auth_functions.decode_jwt(authorization_cookies)['user_id']
            user = self.user_repository.get_one(user_id)

            chat_id = data['chat_id']

            schema = CreateMessageSchema()

            validated_data = schema.dump(data)

            try:
                schema.load(validated_data)
            except ValidationError as err:
                return {"message": "Data Validation Error!", "errors": err.messages}, 400

            chat = self.chat_repository.get(chat_id)

            for member in chat['members']:
                if member['id'] in self.connected and member['id'] != user_id:
                    self.send({
                        "content": validated_data['content'],
                        "user_id": user_id,
                        "user_name": user['name']
                    }, to=self.connected[member['id']])

            self.message_repository.create(
                chat_id=validated_data['chat_id'],
                user_id=user_id,
                content=validated_data['content'])

            print(f"message received: {data['content']}")
