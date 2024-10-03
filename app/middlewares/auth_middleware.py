from flask import request, redirect, make_response
from functools import wraps
from dotenv import load_dotenv
from ..auth.util import AuthFunctions
from jwt import ExpiredSignatureError

load_dotenv()


class AuthMiddleware:
    def __init__(self):
        self.auth_functions = AuthFunctions()

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
                response = func(*args, **kwargs)
                return self.auth_functions.set_auth_cookies(response, authorization_cookie)
            except Exception as err:
                print(err)
                if request.method == 'GET':
                    if err == "Expired access_token":
                        response = make_response(redirect('/auth/signin?expired_session=true'))
                        response.set_cookie('authorization', '')
                        return response
                    else:
                        response = make_response(redirect('/auth/signin?unauthorized=true'))
                        response.set_cookie('authorization', '')
                        return response
                else:

                    return {
                        "message": "Unauthorized"
                    }, 401
        return wrapper

auth_middleware = AuthMiddleware().middleware
