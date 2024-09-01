from flask_sqlalchemy import SQLAlchemy
from .model import friendship_table
from sqlalchemy import and_


class FriendshipRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, user_id: str, friend_id: str):
        self.db.session.execute(friendship_table.insert().values(user_id=user_id, friend_id=friend_id))
        self.db.session.execute(friendship_table.insert().values(user_id=friend_id, friend_id=user_id))
        self.db.session.commit()

    def get(self, user_id: str, friend_id: str):
        friendship = (self.db.session.execute(
            friendship_table.select().where(and_(
                friendship_table.c.user_id == user_id,
                friendship_table.c.friend_id == friend_id)
            )
        ).one_or_none())

        return friendship

    def get_all(self):
        pass

    def update(self, friendship_id: str):
        pass

    def delete(self, friendship_id: str):
        pass

