from flask import request, redirect
from functools import wraps
from ..auth.util import AuthFunctions

class AuthMiddleware:
    def __init__(self):
        self.auth_functions = AuthFunctions()
        pass

    def middleware(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            authorization_cookie = request.cookies.get('authorization')
            try:
                self.auth_functions.verify_access_token(authorization_cookie)

                return redirect('/chat')

            except Exception as err:
                print(err)
                return func(self)

        return wrapper

redirect_auth_middleware = AuthMiddleware().middleware
