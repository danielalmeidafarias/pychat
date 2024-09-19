from flask import Request, make_response, render_template
from sqlalchemy.exc import NoResultFound
import uuid
import bcrypt
from sqlalchemy.exc import IntegrityError
from ..auth.util import AuthFunctions
from media.util import save_profile_pic
from .interfaces.user_repository_interface import UserRepositoryInterface


class UserService:
    def __init__(self, user_repository: UserRepositoryInterface, auth_functions: AuthFunctions):
        self.user_repository = user_repository
        self.auth_functions = auth_functions

    def get_user(self, request: Request):
        user_id = request.args.get('user_id')

        if user_id is not None:
            try:
                user = self.user_repository.get_one(user_id)

                response = make_response({
                    "user": {
                        "id": user['id'],
                        "name": user['name'],
                        "friends": [{"user_id": user.id, "user_name": user.name} for user in user['friends']]
                    },
                })
                response.status_code = 200
                # return self.auth_functions.set_auth_cookies(request.cookies.get('authorization'), response)
                return response

            except NoResultFound:
                return {"message": "No user with this credentials was found"}, 400

            except Exception as err:
                print(err)
                return {"message": str(err)}, 500
        else:
            try:
                users = self.user_repository.get_all()
                response = make_response({
                    "users": users,
                })
                response.status_code = 200
                return self.auth_functions.set_auth_cookies(request.cookies.get('authorization'), response)
            except Exception as err:
                print(err)
                return make_response({"message": "Something went wrong, try again later"}, 500)

    def create_user(self, request: Request):
        data = request.form.to_dict()
        profile_pic = request.files['picture']

        try:
            new_user = self.user_repository.create(
                user_id= str(uuid.uuid4()),
                email=data['email'],
                password=bcrypt.hashpw(str.encode(data["password"]), bcrypt.gensalt()),
                name=data['name']
            )

            save_profile_pic(profile_pic, new_user.id)

        except IntegrityError as err:
            print(err)
            return {"message": "There is already a user with this credentials!"}, 409

        access_token = self.auth_functions.get_access_token(new_user.id)

        response = make_response({
            "message": "User created with success",
            "id": new_user.id.__str__(),
            "email": new_user.email,
            "name": new_user.name
        })

        response.set_cookie('authorization', access_token, httponly=True)

        return response

    def user_profile(self, request: Request):
        authorization = request.cookies.get('authorization')
        user_id = self.auth_functions.decode_jwt(authorization)['user_id']

        user = self.user_repository.get_one(user_id)

        response = make_response(render_template('profile.html', user=user))

        return response

    def update_profile(self, request: Request):
        data = request.form.to_dict()
        user_id = self.auth_functions.decode_jwt(request.cookies.get('authorization'))['user_id']

        try:
            user = self.user_repository.get_one(user_id)
        except NoResultFound as err:
            print(err)
            response = make_response({"message": "No user with this credentials was found"}, 404)
            response.set_cookie('authorization', '', httponly=True)
            return response

        if not self.auth_functions.is_password_correct(data['password'], user['password']):
            return make_response({"message": "Wrong password"}, 401)
        else:
            data.pop('password')

        iterable_data = data.copy()
        for key, value in iterable_data.items():
            if key == 'new_password':
                if self.auth_functions.is_password_correct(data['new_password'], user['password']):
                    data.pop('new_password')
                else:
                    data['new_password'] = bcrypt.hashpw(str.encode(data['new_password']), bcrypt.gensalt())

            elif data[key] == user[key]:
                data.pop(key)

        try:
            if len(data) == 0 and not request.files:
                response = make_response({"message": "No changes was required"}, 400)
                return response
            else:
                if request.files:
                    profile_pic = request.files['picture']
                    save_profile_pic(profile_pic, user_id)

                if len(data) > 0:
                    self.user_repository.update(user_id, data)

        except IntegrityError as err:
            print(err)
            response = make_response({"message": "There is already a user with this credentials!"}, 409)
            return response

        except Exception as err:
            print(err)

        response = make_response({'Account updated with success': True}, 200)
        return response

    def delete_profile(self, request: Request):
        data = request.get_json()

        if 'password' not in data:
            return make_response({"message": "No password was provided"}, 401)
        else:
            user_id = self.auth_functions.decode_jwt(request.cookies.get('authorization'))['user_id']
            user = self.user_repository.get_one(user_id)

            if not self.auth_functions.is_password_correct(data['password'], user['password']):
                return make_response({"message": "Wrong password"}, 401)
            else:
                try:
                    self.user_repository.delete(user_id)

                    response = make_response({"message": "User deleted successfully"}, 200)
                    response.set_cookie('authorization', '', httponly=True)
                    return response
                except Exception as err:
                    print(err)
                    response = make_response({"message": str(err)}, 500)
                    return response
