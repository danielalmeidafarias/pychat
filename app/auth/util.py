import jwt
import os
import datetime
import bcrypt
from flask import Response, make_response, request
from ..db import r


class AuthFunctions:
    @staticmethod
    def decode_jwt(jwt_token: str):
        decoded_jwt = jwt.decode(str.encode(jwt_token), os.getenv('JWT_SECRET'), "HS256")

        return decoded_jwt

    @staticmethod
    def get_access_token(user_id):
        payload = {
            "user_id": str(user_id),
            "expires_at": str(datetime.datetime.now() + datetime.timedelta(minutes=30))
        }

        access_token = jwt.encode(
            payload=payload,
            key=os.getenv('JWT_SECRET')
        )

        return access_token

    def verify_access_token(self, authorization_cookie):
        if authorization_cookie is None:
            raise Exception('None access_token')

        decoded_jwt = self.decode_jwt(jwt_token=authorization_cookie)
        expires_at = datetime.datetime.strptime(decoded_jwt['expires_at'], '%Y-%m-%d %H:%M:%S.%f')

        if expires_at < datetime.datetime.now():
            raise Exception('Expired access_token')

    @staticmethod
    def is_password_correct(password, hashed_password):
        is_password_correct = bcrypt.checkpw(
            password=str.encode(password),
            hashed_password=hashed_password
        )

        return is_password_correct

    def set_auth_cookies(self, response: Response, authorization_cookie: str):
        user_id = self.decode_jwt(authorization_cookie)['user_id']
        access_token = self.get_access_token(user_id=user_id)

        response.set_cookie('authorization', access_token, samesite='Lax', httponly=True,
                            expires=(datetime.datetime.now().utcnow() + datetime.timedelta(hours=1)))
        return response

    def sign_in(self, user, password):
        is_password_correct = self.is_password_correct(password, user['password'])

        if is_password_correct:
            r.delete(f"login_count:{user['id']}")

            access_token = self.get_access_token(user['id'])
            response = make_response("Login successful")
            response.set_cookie('authorization', access_token, samesite='Lax', httponly=True)

            return response
        else:
            login_trying_count = r.get(f"login_count:{user['id']}")

            if login_trying_count is None:
                r.set(f"login_count:{user['id']}", 1)
                r.expireat(f"login_count:{user['id']}", datetime.datetime.now() + datetime.timedelta(minutes=15))
            else:
                r.set(f"login_count:{user['id']}", int(login_trying_count) + 1)
                r.expireat(f"login_count:{user['id']}", datetime.datetime.now() + datetime.timedelta(minutes=15))

                if int(login_trying_count) >= 20:
                    ip_address = request.origin

                    r.set(f"blocked_ip:{ip_address}", 1)
                    r.expireat(f"blocked_ip:{ip_address}", datetime.datetime.now() + datetime.timedelta(days=1))

                if int(login_trying_count) >= 5:
                    r.set(f"login_count:{user['id']}", int(login_trying_count) + 1)
                    r.expireat(f"login_count:{user['id']}",
                                    datetime.datetime.now() + datetime.timedelta(minutes=15))

                    return make_response({
                        "message": "Too many login attempts, try again later"
                    }, 401)

            return make_response({
                "message": "Unauthorized"
            }, 401)

auth_functions = AuthFunctions()
