from flask import request
from flask_restx import Resource, Namespace
from .docs.response_models import UserResponseModels
from .docs.request_models import UserRequestModels
from ..common.docs.response_models import CommonResponseModels
from app.db import db
from app.auth.util import AuthFunctions
from app.middlewares.blocked_ip_middleware import blocked_ip_middleware
from app.middlewares.ddos_protect_middleware import ddos_protect_middleware
from .repository import UserRepository
from .service import UserService
from ..middlewares.auth_middleware import auth_middleware

user_namespace = Namespace('user', 'User Route')
requests = UserRequestModels(user_namespace)
responses = UserResponseModels(user_namespace)
common_responses = CommonResponseModels(user_namespace)
user_repository = UserRepository(db)
auth_functions = AuthFunctions()
user_service = UserService(user_repository, auth_functions)

@user_namespace.route('')
@user_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@user_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@user_namespace.response(code=401, model=common_responses.unauthorized, description='Unauthorized')
@user_namespace.response(code=404, model=common_responses.no_user_found, description='No user found')
class UserResource(Resource):

    @auth_middleware
    @ddos_protect_middleware
    @blocked_ip_middleware
    @user_namespace.header('Authorization', 'Authorization access token')
    @user_namespace.param('user_id')
    @user_namespace.response(code=200, model=responses.get_all_200, description='All users')
    @user_namespace.response(code=200, model=responses.get_one_200, description='One user')
    def get(self):
        return user_service.get_user(request=request)


    @user_namespace.expect(requests.crate_user)
    @user_namespace.response(model=responses.post_201, description="Created!", code=201)
    @user_namespace.response(model=responses.post_409, description="Conflict", code=409)
    def post(self):
        return user_service.create_user(request=request)


@user_namespace.route('/<recipient_user_id>')
class UniqueUserResource(Resource):
    def put(self, recipient_user_id):
        pass

    def delete(self, recipient_user_id):
        pass
