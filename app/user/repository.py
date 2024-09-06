from .model import User
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from .schemas import UpdateUserSchema
from .service import UserRepositoryInterface
from typing import Optional

class UserRepository(UserRepositoryInterface):
    def __init__(self, db: SQLAlchemy):
        self.db = db

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
        # print(user)
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

    def update(self, user_id: str, email: Optional[str], name: Optional[str], password: Optional[bytes]):
        schema = UpdateUserSchema()

        validated_data = schema.dump({
            "email": email,
            "name": name,
            "password": password
        })

        (self.db.session.query(User).where(User.id == user_id).update(validated_data))

        self.db.session.commit()

    def delete(self):
        pass

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

