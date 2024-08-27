from flask import request, make_response
from functools import wraps
import datetime
from dotenv import load_dotenv
from ..auth.util import AuthFunctions
from flask_socketio import disconnect

load_dotenv()


class AuthWsMiddleware:
    def __init__(self):
        self.auth_functions = AuthFunctions
        pass

    def middleware(self, func):
        """

        :param func: Function to be executed after/if authorization passes
        :return: is user not allowed?: Unauthorized 401, '%%
                 is user allowed?: Next function/route service
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            authorization_header = request.headers.get('Auth')

            try:
                decoded_jwt = self.auth_functions.decode_jwt(jwt_token=authorization_header)
                expires_at = datetime.datetime.strptime(decoded_jwt['expires_at'], '%Y-%m-%d %H:%M:%S.%f')

                if expires_at < datetime.datetime.now():
                    raise Exception('Expired access_token')

                return func()

            except Exception as err:
                print(err)
                return {
                    "message": "Unauthorized"
                }, 401

        return wrapper


auth_ws_middleware = AuthWsMiddleware().middleware
