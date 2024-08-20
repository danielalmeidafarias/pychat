from flask import request
from flask_restx import Resource, Namespace
from app.db import db
from marshmallow.exceptions import ValidationError
from .model import Chat_membersModel
from .schemas import GetChat_membersSchema, CreateChat_membersSchema, UpdateChat_membersSchema, DeleteChat_membersSchema
from .docs.response_models import Chat_membersResponseModels
from .docs.request_models import Chat_membersRequestModels
from app.common.docs.response_models import CommonResponseModels


chat_members_namespace = Namespace('chat_members', 'Chat_members Route')
requests = Chat_membersRequestModels(chat_members_namespace)
responses = Chat_membersResponseModels(chat_members_namespace)
common_responses = CommonResponseModels(chat_members_namespace)


@chat_members_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@chat_members_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@chat_members_namespace.response(code=409, model=common_responses.unauthorized, description='Unauthorized')
@chat_members_namespace.route('')
class Chat_membersResource(Resource):
    def get(self):
        pass

    def post(self):
        data = request.get_json()
        schema = CreateChat_membersSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400
        pass


@chat_members_namespace.route('/<id>')
class UniqueChat_membersResource(Resource):
    def put(self):
        data = request.get_json()
        schema = UpdateChat_membersSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400
        pass

    def delete(self):
        pass
