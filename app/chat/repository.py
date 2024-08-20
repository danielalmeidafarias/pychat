from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4 as uuid
from .model import Chat


class ChatRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self):
        chat = Chat(chat_id=str(uuid()))

        self.db.session.add(chat)
        self.db.session.commit()

        return {
            "chat_id": chat.id
        }

    def get(self, chat_id: str):
        pass

    def get_all(self):
        pass

    def update(self, chat_id: str):
        pass

    def delete(self, chat_id: str):
        pass

