from flask_restx import Resource, Namespace
from dotenv import load_dotenv
from flask import request, make_response, render_template
from .docs.response_models import AuthResponseModels
from .docs.request_models import AuthRequestModels
from ..common.docs.response_models import CommonResponseModels
from ..middlewares.redirect_auth_middleware import redirect_auth_middleware
from app.db import db, r
from .auth_service import AuthService
from ..user.user_repository import UserRepository


load_dotenv()
auth_namespace = Namespace(name='auth', description='Authorization route')
requests = AuthRequestModels(auth_namespace)
responses = AuthResponseModels(auth_namespace)
common_responses = CommonResponseModels(auth_namespace)
user_repository = UserRepository(db)
auth_service = AuthService(user_repository, r=r)


@auth_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@auth_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@auth_namespace.response(code=401, model=common_responses.unauthorized, description='Unauthorized')
@auth_namespace.response(code=404, model=common_responses.no_user_found, description='No User Found')
@auth_namespace.route('/signin')
class SignInResource(Resource):
    def post(self):
        return auth_service.sign_in(request=request)


    @redirect_auth_middleware
    def get(self):
        response = make_response(render_template('auth.html'))
        response.set_cookie('authorization', '')
        return response


@auth_namespace.route('/logout')
class SignOutResource(Resource):
    def post(self):
        return auth_service.sign_out()
