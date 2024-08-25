from flask_socketio.namespace import Namespace
from flask_socketio import SocketIO
import urllib.parse as urlparse
from flask import request, Flask
from ..auth.util import AuthFunctions
from typing import List
from ..chat.repository import ChatRepository
from flask_sqlalchemy import SQLAlchemy
from ..middlewares.auth_middleware import auth_middleware


class ChatWebsocket(SocketIO):
    def __init__(self, app: Flask, cors_allowed_origins, db: SQLAlchemy):
        super().__init__(app=app, cors_allowed_origins=cors_allowed_origins)

        self.register_handlers()

        self.connected = {}
        self.auth_functions = AuthFunctions()
        self.chat_repository = ChatRepository(db)
        self.chat = {
            "chat_id": "30509cb1-8786-487e-8a3a-cd1c449a4be5",
            "chat_members": [
                {"id": "1a98fb06-cafd-44a9-8edf-61315f578189"},
                {"id": "b5184898-44ed-4867-bcf4-26b152e822a1"}
            ]
        }

    def register_handlers(self):
        @self.on('connect')
        def on_connect():
            socketio_id = request.sid

            authorization_header = request.headers.get('Auth')
            user_id = self.auth_functions.decode_jwt(authorization_header)['user_id']

            self.connected[user_id] = socketio_id

            print(self.connected)

            print(f"{request.sid} connected successfully")
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

            print(self.connected)
            print(f"{request.sid} disconnected successfully")

        @self.on('message')
        def on_message(data):
            # 1. midleware para autenticação
            # 2. validação dos dados recebidos
            # 3. verificar se o usuário destino está conectado
            # se sim: enviar a mensagem e depois salvar no banco de dados
            # se não apenas salvar no banco

            authorization_header = request.headers.get('Auth')
            user_id = self.auth_functions.decode_jwt(authorization_header)['user_id']

            chat_id = data['chat_id']

            # chat = self.chat_repository.get(chat_id)
            chat = self.chat

            for member in chat['chat_members']:
                if self.connected[member['id']] is not None and member['id'] != user_id:
                    self.send(data['content'], to=self.connected[member['id']])

            print(f"message received: {data['content']}")

