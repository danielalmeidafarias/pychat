from flask import request
from flask_restx import Resource,Namespace
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import bcrypt
from .responses import get_responses
from .model import user_model


def user(db: SQLAlchemy):
    UserModel = user_model(db)

    user_namespace = Namespace('user', 'User Route')

    create_user_model = get_responses(user_namespace)

    @user_namespace.route('')
    class UserResource(Resource):
        @staticmethod
        def get():
            data = db.session.execute(db.select(UserModel)).scalars().all()

            return data.__str__()

        @user_namespace.expect(create_user_model)
        def post(self):
            data = request.get_json()

            new_user = UserModel(
                user_id=uuid4(),
                email=data["email"],
                password=bcrypt.hashpw(str.encode(data["password"]), bcrypt.gensalt()),
                name=data["name"]
            )

            db.session.add(new_user)

            db.session.commit()

            return {
                "id": new_user.id.__str__(),
                "email": new_user.email,
                "password": new_user.password.__str__(),
                "name": new_user.name
            }

    return user_namespace
