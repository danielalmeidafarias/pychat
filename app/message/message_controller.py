from flask import request
from flask_restx import Resource, Namespace
from marshmallow.exceptions import ValidationError
from .message_schemas import CreateMessageSchema, UpdateMessageSchema, GetMessageSchema
from .docs.response_models import MessageResponseModels
from .docs.request_models import MessageRequestModels
from app.common.docs.response_models import CommonResponseModels
from ..middlewares.auth_middleware import auth_middleware
from ..middlewares.blocked_ip_middleware import blocked_ip_middleware
from ..middlewares.ddos_protect_middleware import ddos_protect_middleware
from ..middlewares.validate_data_middleware import ValidateDataMiddleware


message_namespace = Namespace('message', 'Message Route')
requests = MessageRequestModels(message_namespace)
responses = MessageResponseModels(message_namespace)
common_responses = CommonResponseModels(message_namespace)


@message_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@message_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@message_namespace.response(code=409, model=common_responses.unauthorized, description='Unauthorized')
@message_namespace.route('')
class MessageResource(Resource):
    @ddos_protect_middleware
    @blocked_ip_middleware
    @auth_middleware
    @ValidateDataMiddleware(GetMessageSchema).middleware
    def get(self):
        pass

    @ddos_protect_middleware
    @blocked_ip_middleware
    @auth_middleware
    @ValidateDataMiddleware(CreateMessageSchema).middleware
    def post(self):

        pass


@message_namespace.route('/<id>')
class UniqueMessageResource(Resource):
    @ddos_protect_middleware
    @blocked_ip_middleware
    @auth_middleware
    @ValidateDataMiddleware(UpdateMessageSchema).middleware
    def put(self):
        pass

    @ddos_protect_middleware
    @blocked_ip_middleware
    @auth_middleware
    def delete(self):
        pass
