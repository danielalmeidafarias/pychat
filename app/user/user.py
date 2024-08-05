import json

from flask import request
from flask_restx import Resource, Namespace
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import Row
from uuid import uuid4
import bcrypt
from .model import UserModel
from .schemas import CreateUserSchema
from marshmallow.exceptions import ValidationError
from .docs.response_models import UserResponseModels
from .docs.request_models import UserRequestModels
from app.db import db
from app.middlewares.auth_middleware import middleware
user_namespace = Namespace('user', 'User Route')
requests = UserRequestModels(user_namespace)
responses = UserResponseModels(user_namespace)

@user_namespace.route('')
@user_namespace.response(code=500, model=responses.internal_error, description='Something went wrong')
class UserResource(Resource):
    @middleware.auth_middleware
    @user_namespace.header('Authorization', 'Authorization access token')
    @user_namespace.param('user_id')
    @user_namespace.response(code=400, model=responses.get_400, description='No user found')
    @user_namespace.response(code=200, model=responses.get_all_200, description='All users')
    @user_namespace.response(code=200, model=responses.get_one_200, description='One user')
    def get(self):
        """

        :return: registered users
        :param: user_Id
        """
        user_id = request.args.get('user_id')

        if user_id:
            try:
                user = db.session.execute(db.select(UserModel).where(UserModel.id == user_id)).scalar_one()
                return {
                    "user": {
                        "id": user.id,
                        "name": user.name
                    }
                },  200
            except NoResultFound:
                return {"message": "No user with this credentials was found"}, 400

            except Exception as err:
                print(err)
                return {"message": "I'm sorry, something went wrong. Try again later"}, 500
        else:
            try:
                data = db.session.execute(db.select(UserModel)).scalars().all()
                users = [{"id": user.id, "name": user.name} for user in data]
                return {"users": users}, 200
            except Exception as err:
                print(err)
                return {"message": "I'm sorry, something went wrong. Try again later"}, 500

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
