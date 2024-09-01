from flask import request, make_response, redirect
from functools import wraps
import datetime
from dotenv import load_dotenv
from ..auth.util import AuthFunctions

load_dotenv()


class AuthMiddleware:
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
            authorization_cookie = request.cookies.get('authorization')

            try:
                decoded_jwt = self.auth_functions.decode_jwt(jwt_token=authorization_cookie)
                expires_at = datetime.datetime.strptime(decoded_jwt['expires_at'], '%Y-%m-%d %H:%M:%S.%f')

                if expires_at < datetime.datetime.now():
                    raise Exception('Expired access_token')

                return func(self)

            except Exception as err:
                print(err)
                return redirect('/auth/signin')

        return wrapper

auth_middleware = AuthMiddleware().middleware
