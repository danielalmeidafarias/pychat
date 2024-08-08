from flask_sqlalchemy import SQLAlchemy


class Friendship_requestRepository():
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, friendship_request_id: str):
        pass

    def get(self, friendship_request_id: str):
        pass

    def get_all(self):
        pass

    def update(self, friendship_request_id: str):
        pass

    def delete(self, friendship_request_id: str):
        pass

