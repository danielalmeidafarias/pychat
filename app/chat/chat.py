from flask import request, make_response, render_template
from flask_restx import Resource, Namespace
from marshmallow.exceptions import ValidationError
from .schemas import CreateChatSchema, UpdateChatSchema, DeleteChatSchema
from .docs.response_models import ChatResponseModels
from .docs.request_models import ChatRequestModels
from app.common.docs.response_models import CommonResponseModels
from .service import ChatService
from app.db import db
from ..middlewares import auth_middleware
from ..middlewares.auth_middleware import auth_middleware


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
    @auth_middleware
    def get(self):
        return chat_service.get_chats()

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

