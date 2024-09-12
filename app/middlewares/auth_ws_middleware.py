from flask import request
from functools import wraps
import datetime
from dotenv import load_dotenv
from ..auth.util import AuthFunctions
from flask_socketio import disconnect

load_dotenv()


class AuthWsMiddleware:
    def __init__(self):
        self.auth_functions = AuthFunctions()
        pass

    def middleware(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            authorization_cookie = request.cookies.get('authorization')
            socketio_id = request.sid

            try:
                self.auth_functions.verify_access_token(authorization_cookie)
                return func(*args, **kwargs)

            except Exception as err:
                print(err)
                return disconnect(socketio_id)

        return wrapper


auth_ws_middleware = AuthWsMiddleware().middleware
