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
from ..middlewares.validate_route_middleware import ValidateRouteMiddleware


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
    @ValidateRouteMiddleware(GetChatSchema).middleware
    @auth_middleware
    def get(self):
        return chat_service.get_chats()

    @ValidateRouteMiddleware(CreateChatSchema).middleware
    def post(self):
        data = request.get_json()
        schema = CreateChatSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400
        pass


@chat_namespace.route('/<id>')
class UniqueChatResource(Resource):
    @ValidateRouteMiddleware(UpdateChatSchema).middleware
    def put(self):
        data = request.get_json()
        schema = UpdateChatSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400
        pass

    def delete(self):
        pass

