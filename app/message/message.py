from flask import request
from flask_restx import Resource, Namespace
from marshmallow.exceptions import ValidationError
from .schemas import CreateMessageSchema, UpdateMessageSchema
from .docs.response_models import MessageResponseModels
from .docs.request_models import MessageRequestModels
from app.common.docs.response_models import CommonResponseModels


message_namespace = Namespace('message', 'Message Route')
requests = MessageRequestModels(message_namespace)
responses = MessageResponseModels(message_namespace)
common_responses = CommonResponseModels(message_namespace)


@message_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@message_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@message_namespace.response(code=409, model=common_responses.unauthorized, description='Unauthorized')
@message_namespace.route('')
class MessageResource(Resource):
    def get(self):
        pass

    def post(self):
        data = request.get_json()
        schema = CreateMessageSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400
        pass


@message_namespace.route('/<id>')
class UniqueMessageResource(Resource):
    def put(self):
        data = request.get_json()
        schema = UpdateMessageSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400
        pass

    def delete(self):
        pass
