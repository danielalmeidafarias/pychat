import uuid
from flask import request
from flask_restx import Resource, Namespace
from sqlalchemy.exc import IntegrityError, NoResultFound, OperationalError
import bcrypt
from .schemas import CreateUserSchema
from marshmallow.exceptions import ValidationError
from .docs.response_models import UserResponseModels
from .docs.request_models import UserRequestModels
from ..common.docs.response_models import CommonResponseModels
from app.db import db
from app.auth.functions.functions import AuthFunctions
from app.middlewares.blocked_ip_middleware import blocked_ip_middleware
from app.middlewares.ddos_protect_middleware import ddos_protect_middleware
from .user_repository import UserRepository


user_namespace = Namespace('user', 'User Route')
requests = UserRequestModels(user_namespace)
responses = UserResponseModels(user_namespace)
common_responses = CommonResponseModels(user_namespace)
user_repository = UserRepository(db)
auth_functions = AuthFunctions()

@user_namespace.route('')
@user_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@user_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@user_namespace.response(code=401, model=common_responses.unauthorized, description='Unauthorized')
@user_namespace.response(code=404, model=common_responses.no_user_found, description='No user found')
class UserResource(Resource):
    # @auth_middleware.middleware
    @ddos_protect_middleware
    @blocked_ip_middleware
    @user_namespace.header('Authorization', 'Authorization access token')
    @user_namespace.param('user_id')
    @user_namespace.response(code=200, model=responses.get_all_200, description='All users')
    @user_namespace.response(code=200, model=responses.get_one_200, description='One user')
    def get(self):
        """

        Registered users
        """
        user_id = request.args.get('user_id')

        if user_id:
            try:
                user = user_repository.get(user_id)
                return {
                    "user": {
                        "id": user['id'],
                        "name": user['name']
                    },
                }, 200
            except NoResultFound:
                return {"message": "No user with this credentials was found"}, 400

            except Exception as err:
                print(err)
                return {"message": str(err)}, 500
        else:
            try:
                users = user_repository.get_all()
                return {
                    "users": users
                }, 200
            except Exception as err:
                print(err)
                return {"message": "Something went wrong, try again later"}, 500

    @user_namespace.expect(requests.crate_user)
    @user_namespace.response(model=responses.post_201, description="Created!", code=201)
    @user_namespace.response(model=responses.post_409, description="Conflict", code=409)
    def post(self):
        """

          Register new users
          """
        data = request.get_json()
        schema = CreateUserSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {"message": "Data Validation Error!", "errors": err.messages}, 400

        try:
            new_user = user_repository.create(
                id=str(uuid.uuid4()),
                email=validated_data['email'],
                password=bcrypt.hashpw(str.encode(validated_data["password"]), bcrypt.gensalt()),
                name=validated_data['name']
            )

        except IntegrityError as err:
            return {"message": "There is already a user with this credentials!"}, 409

        return {
            "message": "User created with success",
            "id": new_user.id.__str__(),
            "email": new_user.email,
            "name": new_user.name
        }, 201

@user_namespace.route('/<recipient_user_id>')
class UniqueUserResource(Resource):
    def put(self, recipient_user_id):
        pass

    def delete(self, recipient_user_id):
        pass