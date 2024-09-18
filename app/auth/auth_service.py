from sqlalchemy.exc import NoResultFound
from flask import Request, make_response
import datetime
from redis import Redis
from ..user.user_service import UserRepositoryInterface
from .util import AuthFunctions

class AuthService:
    def __init__(self, user_repository: UserRepositoryInterface, r: Redis):
        self.user_repository = user_repository
        self.auth_functions = AuthFunctions()
        self.r = r

    def sign_in(self, request: Request):
        try:
            data = request.get_json()

            try:
                user = self.user_repository.get_one_by_email(data['email'])
            except NoResultFound:
                return {
                    "message": "No user with this credentials was found, please check the email"
                }, 404

            is_password_correct = self.auth_functions.is_password_correct(data['password'], user['password'])

            if is_password_correct:
                self.r.delete(f"login_count:{user['id']}")

                access_token = self.auth_functions.get_access_token(user['id'])
                response = make_response("Login successful")
                response.set_cookie('authorization', access_token, samesite='Lax', httponly=True)

                return response
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

                        return make_response({
                            "message": "Too many login attempts, try again later"
                        }, 401)

                return make_response({
                    "message": "Unauthorized"
                }, 401)
        except Exception as err:
            print(err)
            return make_response({
                "message": "Something went wrong, please try again"
            }, 500)

    def sign_out(self):
        response = make_response()
        response.set_cookie('authorization', '', expires=(datetime.datetime.now().utcnow() + datetime.timedelta(seconds=2)), httponly=True)
        return response
