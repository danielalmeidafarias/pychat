from flask import request
from flask_restx import Resource, Namespace
from app.db import db
from marshmallow.exceptions import ValidationError
from .model import friendship_table
from .schemas import GetFriendshipSchema, CreateFriendshipSchema, UpdateFriendshipSchema, DeleteFriendshipSchema
from .docs.response_models import FriendshipResponseModels
from .docs.request_models import FriendshipRequestModels
from app.common.docs.response_models import CommonResponseModels


friendship_namespace = Namespace('friendship', 'Friendship Route')
requests = FriendshipRequestModels(friendship_namespace)
responses = FriendshipResponseModels(friendship_namespace)
common_responses = CommonResponseModels(friendship_namespace)


@friendship_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@friendship_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@friendship_namespace.response(code=409, model=common_responses.unauthorized, description='Unauthorized')
@friendship_namespace.route('')
class FriendshipResource(Resource):
    def get(self):
        pass

    def post(self):
        data = request.get_json()
        schema = CreateFriendshipSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400
        pass


@friendship_namespace.route('/<id>')
class UniqueFriendshipResource(Resource):
    def put(self):
        data = request.get_json()
        schema = UpdateFriendshipSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400
        pass

    def delete(self):
        pass
