from flask_sqlalchemy import SQLAlchemy
from .chat_members_model import chat_members


class ChatMemberRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, chat_id: str, user_id: str):
        self.db.session.execute(chat_members.insert().values(chat_id=chat_id, user_id=user_id))
        self.db.session.commit()

    def delete(self, chat_members_id: str):
        pass

