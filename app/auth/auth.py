from flask_restx import Resource, Namespace
from dotenv import load_dotenv
from flask import request
from .docs.response_models import AuthResponseModels
from .docs.request_models import AuthRequestModels
from ..common.docs.response_models import CommonResponseModels
from ..middlewares.blocked_ip_middleware import blocked_ip_middleware
from ..middlewares.ddos_protect_middleware import ddos_protect_middleware
from app.db import db, r
from .service import AuthService

load_dotenv()
auth_namespace = Namespace(name='auth', description='Authorization route')
requests = AuthRequestModels(auth_namespace)
responses = AuthResponseModels(auth_namespace)
common_responses = CommonResponseModels(auth_namespace)
auth_service = AuthService(db=db, r=r)


@auth_namespace.route('')
@auth_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@auth_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@auth_namespace.response(code=401, model=common_responses.unauthorized, description='Unauthorized')
@auth_namespace.response(code=404, model=common_responses.no_user_found, description='No User Found')
class AuthResource(Resource):
    @ddos_protect_middleware
    @blocked_ip_middleware
    @auth_namespace.expect(requests.signin)
    @auth_namespace.response(model=responses.post_200, description="Success", code=200)
    def post(self):
        return auth_service.signIn(request=request)

