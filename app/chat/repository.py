from flask_sqlalchemy import SQLAlchemy


class ChatRepository():
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, chat_id: str):
        pass

    def get(self, chat_id: str):
        pass

    def get_all(self):
        pass

    def update(self, chat_id: str):
        pass

    def delete(self, chat_id: str):
        pass

