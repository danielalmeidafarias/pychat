from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4 as uuid
from .model import friendship_table


class FriendshipRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, user_id: str, friend_id: str):
        self.db.session.execute(friendship_table.insert().values(user_id=user_id, friend_id=friend_id))
        self.db.session.execute(friendship_table.insert().values(user_id=friend_id, friend_id=user_id))
        self.db.session.commit()

    def get(self, user_id: str, friend_id: str):
        # friendship = (self.db.session.execute(friendship_table.select().where(user_id == user_id and friend_id == friend_id))
        #               .one_or_none())

        friendship = (
                self.db.session.execute(friendship_table.select().where(user_id == 'b178edee-df43-4f83-b6c3-8520d893cddb')).all())

        print(friendship)

        return friendship

    def get_all(self):
        pass

    def update(self, friendship_id: str):
        pass

    def delete(self, friendship_id: str):
        pass

