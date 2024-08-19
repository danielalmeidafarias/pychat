from sqlalchemy.exc import NoResultFound
from app.user.model import User
from app.auth.schemas import SignInSchema
from flask import Request
from marshmallow import ValidationError
import datetime
from redis import Redis
from .util import AuthFunctions
from ..user.service import UserRepositoryInterface


class AuthService:
    def __init__(self, user_repository: UserRepositoryInterface, r: Redis):
        self.user_repository = user_repository
        self.r = r

    def sign_in(self, request: Request, ):
        data = request.get_json()
        schema = SignInSchema()
        validated_data = schema.dump(data)

        auth_functions = AuthFunctions()

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {"message": "Data Validation Error!", "errors": err.messages}, 400

        try:
            user = self.user_repository.get_one_by_email(validated_data['email'])
            print(user)
        except NoResultFound:
            return {
                "message": "No user with this credentials was found, please check the email"
            }, 404

        is_password_correct = auth_functions.is_password_correct(validated_data['password'], user['password'])

        if is_password_correct:
            self.r.delete(f"login_count:{user['id']}")

            access_token = auth_functions.get_access_token(user['id'])

            return {
                "access_token": access_token
            }, 200
        else:
            login_trying_count = self.r.get(f"login_count:{user['id']}")

            if login_trying_count is None:
                self.r.set(f"login_count:{user['id']}", 1)
                self.r.expireat(f"login_count:{user['id']}", datetime.datetime.now() + datetime.timedelta(minutes=15))
            else:
                self.r.set(f"login_count:{user['id']}", int(login_trying_count) + 1)
                self.r.expireat(f"login_count:{user['id']}", datetime.datetime.now() + datetime.timedelta(minutes=15))

                if int(login_trying_count) >= 20:
                    ip_address = request.origin

                    self.r.set(f"blocked_ip:{ip_address}", 1)
                    self.r.expireat(f"blocked_ip:{ip_address}", datetime.datetime.now() + datetime.timedelta(days=1))

                if int(login_trying_count) >= 5:
                    self.r.set(f"login_count:{user['id']}", int(login_trying_count) + 1)
                    self.r.expireat(f"login_count:{user['id']}", datetime.datetime.now() + datetime.timedelta(minutes=15))

                    return {
                        "message": "Too many login attempts, try again later"
                    }, 401

            return {
                "message": "Unauthorized"
            }, 401