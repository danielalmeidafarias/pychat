import jwt
import os
import datetime
import bcrypt
from flask import Response, make_response

class AuthFunctions:
    @staticmethod
    def decode_jwt(jwt_token: str):
        decoded_jwt = jwt.decode(str.encode(jwt_token), os.getenv('JWT_SECRET'), "HS256")

        return decoded_jwt

    @staticmethod
    def get_access_token(user_id):
        payload = {
            "user_id": str(user_id),
            "expires_at": str(datetime.datetime.now() + datetime.timedelta(hours=1))
        }

        access_token = jwt.encode(
            payload=payload,
            key=os.getenv('JWT_SECRET')
        )

        return access_token

    @staticmethod
    def is_password_correct(password, hashed_password):
        is_password_correct = bcrypt.checkpw(
            password=str.encode(password),
            hashed_password=hashed_password
        )

        return is_password_correct

    def set_auth_cookies(self, user_id: str, response: Response):
        response.set_cookie('Authorization', self.get_access_token(user_id), httponly=True, secure=True,
                            expires=(datetime.datetime.now() + datetime.timedelta(hours=1)))

        return response
