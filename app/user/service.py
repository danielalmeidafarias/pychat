from flask import Request, make_response
from sqlalchemy.exc import NoResultFound
from app.db import db
from .schemas import CreateUserSchema
from marshmallow import ValidationError
import uuid
import bcrypt
from sqlalchemy.exc import IntegrityError
from abc import ABC, abstractmethod
from typing import Optional
from ..auth.util import AuthFunctions


class UserRepositoryInterface(ABC):
    @abstractmethod
    def create(self, user_id:str, email:str, password:bytes, name:str):
        pass

    @abstractmethod
    def get_one(self, user_id):
        pass

    def get_one_by_email(self, email):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, user_id: str, email: Optional[str], name: Optional[str], password: Optional[bytes]):
        pass


class UserService:
    def __init__(self, user_repository: UserRepositoryInterface, auth_functions: AuthFunctions):
        self.user_repository = user_repository
        self.auth_functions = auth_functions

    def get_user(self, request: Request):
        user_id = request.args.get('user_id')

        if user_id is not None:
            try:
                user = self.user_repository.get_one(user_id)

                response = make_response({
                    "user": {
                        "id": user['id'],
                        "name": user['name'],
                        "friends": [{"user_id": user.id, "user_name": user.name} for user in user['friends']]
                    },
                })
                response.status_code = 200
                return self.auth_functions.set_auth_cookies(request.headers.get('Authorization'), response)

            except NoResultFound:
                return {"message": "No user with this credentials was found"}, 400

            except Exception as err:
                print(err)
                return {"message": str(err)}, 500
        else:
            try:
                users = self.user_repository.get_all()
                response = make_response({
                    "users": users,
                })
                response.status_code = 200
                return self.auth_functions.set_auth_cookies(request.headers.get('Authorization'), response)
            except Exception as err:
                print(err)
                return {"message": "Something went wrong, try again later"}, 500

    def create_user(self, request: Request):
        data = request.get_json()
        schema = CreateUserSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {"message": "Data Validation Error!", "errors": err.messages}, 400

        try:
            new_user = self.user_repository.create(
                user_id=str(uuid.uuid4()),
                email=validated_data['email'],
                password=bcrypt.hashpw(str.encode(validated_data["password"]), bcrypt.gensalt()),
                name=validated_data['name']
            )


        except IntegrityError as err:
            print(err)
            return {"message": "There is already a user with this credentials!"}, 409

        access_token = self.auth_functions.get_access_token(new_user.id)

        response = make_response({
            "message": "User created with success",
            "id": new_user.id.__str__(),
            "email": new_user.email,
            "name": new_user.name
        })

        response.set_cookie('authorization', access_token, httponly=True)

        return response



