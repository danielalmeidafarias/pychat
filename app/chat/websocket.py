from flask_socketio import SocketIO
from flask import request, Flask
from ..auth.util import AuthFunctions
from typing import List
from ..chat.repository import ChatRepository
from flask_sqlalchemy import SQLAlchemy


class ChatWebsocket(SocketIO):
    def __init__(self, app: Flask, cors_allowed_origins, db: SQLAlchemy):
        super().__init__(app=app, cors_allowed_origins=cors_allowed_origins)

        self.register_handlers()

        self.connected = {}
        self.auth_functions = AuthFunctions()
        self.chat_repository = ChatRepository(db)

    def register_handlers(self):
        @self.on('connect')
        def on_connect():
            socketio_id = request.sid

            authorization_header = request.headers.get('Auth')
            user_id = self.auth_functions.decode_jwt(authorization_header)['user_id']

            self.connected[user_id] = socketio_id

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

            chat = self.chat_repository.get(chat_id)

            for member in chat['members']:
                if member['id'] in self.connected:
                    self.send(data['content'], to=self.connected[member['id']])

            print(f"message received: {data['content']}")

