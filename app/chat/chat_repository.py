from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4 as uuid
from .model import Chat


class ChatRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, chat_name: None | str):
        chat = Chat(chat_id=str(uuid()), chat_name=chat_name)

        self.db.session.add(chat)
        self.db.session.commit()

        return {
            "id": chat.id
        }

    def get(self, chat_id: str):
        chat = self.db.session.execute(self.db.select(Chat).where(Chat.id == chat_id)).scalar_one_or_none()

        return {
            "chat_id": chat.id,
            "members": [
                {"id": member.id} for member in chat.chat_members
            ],
            "messages": chat.messages
        }

    def update(self, chat_id: str):
        pass

    def delete(self, chat_id: str):
        pass

