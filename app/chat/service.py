from ..user.repository import UserRepository
from .repository import ChatRepository
from flask_sqlalchemy import SQLAlchemy
from ..auth.util import AuthFunctions
from flask import request, make_response, render_template, url_for

class ChatService:
    def __init__(self, db: SQLAlchemy):
        self.user_repository = UserRepository(db)
        self.chat_repository = ChatRepository(db)
        self.auth_functions = AuthFunctions()
        pass

    def get_chats(self):
        authorization_header = request.cookies.get('authorization')
        user_id = self.auth_functions.decode_jwt(authorization_header)['user_id']

        user = self.user_repository.get_one(user_id)

        chat_id = request.args.get('id')

        if chat_id is not None:
            chat = self.chat_repository.get(chat_id)
            response = make_response(render_template(f"chat.html", messages=chat['messages'],chat=chat, chats=user['chats'], user=user), 200)
            return response
        else:
            response = make_response(render_template('chat.html', user=user, chats=user['chats']), 200)
            return response
