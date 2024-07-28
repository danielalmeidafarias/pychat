from flask import request
from flask_restx import Resource, Namespace
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
import bcrypt
from .docs.request_models import request_models
from .model import get_user_model
from .schemas import CreateUserSchema
from marshmallow.exceptions import ValidationError
from password_strength import PasswordPolicy


def user(db: SQLAlchemy):
    user_model = get_user_model(db)

    user_namespace = Namespace('user', 'User Route')

    create_user_model = request_models(user_namespace)

    @user_namespace.route('')
    class UserResource(Resource):
        @staticmethod
        def get():
            data = db.session.execute(db.select(user_model)).scalars().all()

            return data.__str__()

        @user_namespace.expect(create_user_model)
        def post(self):
            data = request.get_json()
            schema = CreateUserSchema()
            validated_data = schema.dump(data)

            try:
                schema.load(validated_data)
            except ValidationError as err:
                return {"message": "Data Validation Error!", "errors": err.messages}

            new_user = user_model(
                user_id=uuid4(),
                email=validated_data["email"],
                password=bcrypt.hashpw(str.encode(validated_data["password"]), bcrypt.gensalt()),
                name=validated_data["name"]
            )

            try:
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError as err:
                return {"message": "There is already a registered user with this credentials!"}

            return {
                "id": new_user.id.__str__(),
                "email": new_user.email,
                "password": new_user.password.__str__(),
                "name": new_user.name
            }

    return user_namespace
