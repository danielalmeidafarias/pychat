from flask import request
from flask_restx import Resource, Namespace
from marshmallow.exceptions import ValidationError
from .chat_schemas import CreateChatSchema, UpdateChatSchema, GetChatSchema
from .docs.response_models import ChatResponseModels
from .docs.request_models import ChatRequestModels
from app.common.docs.response_models import CommonResponseModels
from .chat_service import ChatService
from app.db import db
from ..middlewares.auth_middleware import auth_middleware
from ..middlewares.validate_data_middleware import ValidateDataMiddleware


chat_namespace = Namespace('chat', 'Chat Route')
requests = ChatRequestModels(chat_namespace)
responses = ChatResponseModels(chat_namespace)
common_responses = CommonResponseModels(chat_namespace)
chat_service = ChatService(db)


@chat_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@chat_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@chat_namespace.response(code=409, model=common_responses.unauthorized, description='Unauthorized')
@chat_namespace.route('')
class ChatResource(Resource):
    @ValidateDataMiddleware(GetChatSchema).middleware
    @auth_middleware
    def get(self):
        return chat_service.get_chats()

    @ValidateDataMiddleware(CreateChatSchema).middleware
    def post(self):
        pass

@chat_namespace.route('/<id>')
class UniqueChatResource(Resource):
    @ValidateDataMiddleware(UpdateChatSchema).middleware
    def put(self):

        pass

    def delete(self):
        pass

