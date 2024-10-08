from flask import request
from flask_restx import Resource, Namespace
from marshmallow.exceptions import ValidationError
from .chat_members_schemas import CreateChatMembersSchema, UpdateChatMembersSchema, GetChatMembersSchema
from .docs.response_models import Chat_membersResponseModels
from .docs.request_models import Chat_membersRequestModels
from app.common.docs.response_models import CommonResponseModels
from ..chat.chat_schemas import GetChatSchema
from ..middlewares.auth_middleware import auth_middleware
from ..middlewares.blocked_ip_middleware import blocked_ip_middleware
from ..middlewares.ddos_protect_middleware import ddos_protect_middleware
from ..middlewares.validate_data_middleware import ValidateDataMiddleware


chat_members_namespace = Namespace('chat_members', 'Chat_members Route')
requests = Chat_membersRequestModels(chat_members_namespace)
responses = Chat_membersResponseModels(chat_members_namespace)
common_responses = CommonResponseModels(chat_members_namespace)


@chat_members_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@chat_members_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@chat_members_namespace.response(code=409, model=common_responses.unauthorized, description='Unauthorized')
@chat_members_namespace.route('')
class Chat_membersResource(Resource):
    @ddos_protect_middleware
    @blocked_ip_middleware
    @auth_middleware
    @ValidateDataMiddleware(GetChatSchema).middleware
    def get(self):
        pass


    @ddos_protect_middleware
    @blocked_ip_middleware
    @auth_middleware
    @ValidateDataMiddleware(UpdateChatMembersSchema).middleware
    def post(self):
        pass


@chat_members_namespace.route('/<chat_id>/<user_id>')
class UniqueChat_membersResource(Resource):
    @ddos_protect_middleware
    @blocked_ip_middleware
    @auth_middleware
    @ValidateDataMiddleware(UpdateChatMembersSchema).middleware
    def put(self):
        pass


    @ddos_protect_middleware
    @blocked_ip_middleware
    @auth_middleware
    def delete(self):
        pass
