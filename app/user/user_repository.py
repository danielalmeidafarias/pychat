from .user_model import User
from ..chat_members.chat_members_model import chat_members
from ..chat.model import Chat
from ..friendship.friendship_model import friendship_table
from ..friendship_request.friendship_request_model import FriendshipRequest
from ..message.message_model import Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, and_
from .user_schemas import UpdateUserSchema
from .interfaces.user_repository_interface import UserRepositoryInterface, UserResponse
from typing import Optional

class UserRepository(UserRepositoryInterface):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db)

    def create(self, user_id: str, email: str, password: bytes, name: str):
        new_user = User(
            user_id=user_id,
            email=email,
            password=password,
            name=name
        )

        self.db.session.add(new_user)
        self.db.session.commit()

        return new_user

    def get_one(self, user_id: str):
        user = self.db.session.execute(select(User).where(User.id == user_id)).scalar_one()
        return {
                "id": user_id,
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "friends": user.friends,
                "chats": user.chats,
                "received_requests": user.received_requests,
                "sent_requests": user.sent_requests,
        }

    def get_one_by_email(self, email):
        user = self.db.session.execute(self.db.select(User).filter_by(email=email)).scalar_one()
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "friends": user.friends,
        }

    def get_all(self):
        data = self.db.session.execute(self.db.select(User)).scalars().all()
        users = [{"id": user.id, "name": user.name} for user in data]
        return users

    def update(self, user_id: str, data):
        (self.db.session.query(User).where(User.id == user_id).update(data))

        self.db.session.commit()

    def delete(self, user_id: str):
        self.db.session.execute(
            friendship_table.delete().where(
                friendship_table.c.user_id == user_id
            ).where(
                friendship_table.c.friend_id == user_id
            ))

        self.db.session.execute(
            chat_members.delete().where(
                chat_members.c.user_id == user_id
            )
        )

        self.db.session.query(FriendshipRequest).where(FriendshipRequest.sender_id == user_id).delete()
        self.db.session.query(FriendshipRequest).where(FriendshipRequest.receiver_id == user_id).delete()

        self.db.session.query(Message).where(Message.user_id == user_id).delete()

        self.db.session.query(User).where(User.id == user_id).delete()

        self.db.session.commit()

    def search(self, user_id: str, name: str):
        users = self.db.session.execute(select(User).where(User.name.like(f"%{name}%"))).all()

        return [
            {
                "id": user[0].id,
                "name": user[0].name,
                "email": user[0].email,
                "password": user[0].password,
                "friends": user[0].friends,
                "chats": user[0].chats,
                "received_requests": user[0].received_requests,
                "sent_requests": user[0].sent_requests,
            } for user in users if user[0].id != user_id
        ]

