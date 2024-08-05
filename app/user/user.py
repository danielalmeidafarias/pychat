from flask import request
from flask_restx import Resource, Namespace
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
import bcrypt
from .model import UserModel
from .schemas import CreateUserSchema
from marshmallow.exceptions import ValidationError
from password_strength import PasswordPolicy
from .docs.response_models import UserResponseModels
from .docs.request_models import UserRequestModels
from app.db import db
from app.middlewares.auth_middleware import middleware
user_namespace = Namespace('user', 'User Route')
requests = UserRequestModels(user_namespace)
responses = UserResponseModels(user_namespace)

@user_namespace.route('')
# @user_namespace.header('Authorization', 'Authorization access token')
class UserResource(Resource):
    @middleware.auth_middleware
    @user_namespace.header('Authorization')
    def get(self):
        """

        :return: All registered users
                 For testing only purpose
        """
        data = db.session.execute(db.select(UserModel)).scalars().all()
        return {"users": data.__str__()}, 200

    @user_namespace.expect(requests.crate_user)
    @user_namespace.response(model=responses.post_201, description="Created!", code=201)
    @user_namespace.response(model=responses.post_400, description="Created!", code=400)
    @user_namespace.response(model=responses.post_409, description="Created!", code=409)
    def post(self):
        """

        :return: Register new users
        """
        data = request.get_json()
        schema = CreateUserSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {"message": "Data Validation Error!", "errors": err.messages}, 400

        new_user = UserModel(
            email=validated_data["email"],
            password=bcrypt.hashpw(str.encode(validated_data["password"]), bcrypt.gensalt()),
            name=validated_data["name"]
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as err:
            return {"message": "There is already a user with this credentials!"}, 409

        return {
            "message": "User created with success",
            "id": new_user.id.__str__(),
            "email": new_user.email,
            "name": new_user.name
        }, 201

