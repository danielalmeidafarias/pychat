from flask import request, redirect
from functools import wraps
from dotenv import load_dotenv
from ..auth.util import AuthFunctions

load_dotenv()


class AuthMiddleware:
    def __init__(self):
        self.auth_functions = AuthFunctions()
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
                self.auth_functions.verify_access_token(authorization_cookie)

                return func(self)

            except Exception as err:
                print(err)
                return redirect('/auth/signin')

        return wrapper

auth_middleware = AuthMiddleware().middleware
