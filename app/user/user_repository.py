from .model import UserModel
from flask_sqlalchemy import SQLAlchemy
from .schemas import UpdateUserSchema

class UserRepository():
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, id: str, email: str, password: bytes, name: str):
        new_user = UserModel(
            id=id,
            email=email,
            password=password,
            name=name
        )

        self.db.session.add(new_user)
        self.db.session.commit()

        return new_user

    def get(self, user_id: str):
        user = self.db.session.execute(self.db.select(UserModel).where(UserModel.id == user_id)).scalar_one()
        return {
                "id": user_id,
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "friends": user.friends,
                "friendship_request": user.friendship_request,
                "sent_friendship_request": user.sent_friendship_request
        }

    def get_all(self):
        data = self.db.session.execute(self.db.select(UserModel)).scalars().all()
        users = [{"id": user.id, "name": user.name} for user in data]
        return users

    def update(self, user_id: str, update_data: dict):
        schema = UpdateUserSchema()
        validated_data = schema.dump(update_data)

        (self.db.session.query(UserModel).where(UserModel.id == user_id).update(validated_data))

    def delete(self):
        pass
