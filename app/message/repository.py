from flask_sqlalchemy import SQLAlchemy
from .model import Message
from uuid import uuid4 as uuid


class MessageRepository():
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, user_id: str, chat_id: str, content: str):
        message = Message(
            message_id=str(uuid()),
            chat_id=chat_id,
            user_id=user_id,
            content=content,
        )

        self.db.session.add(message)
        self.db.session.commit()

        return {
                "message_id": message.id,
                "chat_id": message.chat_id,
                "user_id": message.user_id,
                "content": message.content
        }

    def get_one(self, message_id: str):
        message = self.db.session.execute(self.db.select(Message).where(
            Message.id == message_id
        )).scalar_one()

        return {
            "message_id": message.id,
            "user_id": message.user_id,
            "content": message.content,
            "created_at": message.created_at,
            "updated_at": message.updated_at
        }


    def get_by_chat(self):
        pass

    def get_by_chat_and_user(self):
        pass

    def get_all(self):
        pass

    def update(self, message_id: str):
        pass

    def delete(self, message_id: str):
        pass

