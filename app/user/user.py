from flask import request
from flask_restx import Resource,Namespace
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
import bcrypt
from .responses import get_responses
from .model import user_model
from .schemas import CreateUserSchema
from marshmallow.exceptions import ValidationError
from password_strength import PasswordPolicy

password_policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=3,
    special=1,
    nonletters=1
)


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
            schema = CreateUserSchema()
            validated_data = schema.dump(data)

            try:
                schema.load(validated_data)
            except ValidationError as err:
                return {"message": "Data Validation Error!", "errors": err.messages}

            tested_password = password_policy.test(data["password"])

            if len(tested_password) > 0:
                return {
                    "message": "The password must have at least eight character, "
                               "one uppercase letter, "
                               "one special character, "
                               "and three numbers"
                }

            new_user = UserModel(
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
