from flask import request
from functools import wraps
import jwt
import datetime
import os
from dotenv import load_dotenv
load_dotenv()


class Auth:
    def __init__(self):
        pass


    @staticmethod
    def decode_jwt(authorization_header: str):
        decoded_jwt = jwt.decode(authorization_header, os.getenv('JWT_SECRET'), "HS256")
        return decoded_jwt


    def middleware(self, func):
        """

        :param func: Function to be executed after/if authorization passes
        :return: is user not allowed?: Unauthorized 401, '%%
                 is user allowed?: Next function/route service
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            authorization_header = request.headers.get('Authorization')

            try:
                decoded_jwt = self.decode_jwt(authorization_header)
                expires_at = datetime.datetime.strptime(decoded_jwt['expires_at'], '%Y-%m-%d %H:%M:%S.%f')

                if expires_at < datetime.datetime.now():
                    raise Exception('Expired access_token')

                return func(self)
            except Exception as err:
                return {
                    "message": "Unauthorized"
                }, 401

        return wrapper


auth_middleware = Auth().middleware
decode_jwt = Auth().decode_jwt
