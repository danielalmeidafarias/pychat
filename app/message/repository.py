from flask_sqlalchemy import SQLAlchemy


class MessageRepository():
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, message_id: str):
        pass

    def get(self, message_id: str):
        pass

    def get_all(self):
        pass

    def update(self, message_id: str):
        pass

    def delete(self, message_id: str):
        pass

