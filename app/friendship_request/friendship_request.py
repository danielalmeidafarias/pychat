import uuid

from flask import request
from flask_restx import Resource, Namespace
from app.db import db
from marshmallow.exceptions import ValidationError
from .schemas import GetFriendshipRequestSchema, CreateFriendshipRequestSchema, UpdateFriendshipRequestSchema, DeleteFriendshipRequestSchema
from .docs.response_models import Friendship_requestResponseModels
from .docs.request_models import Friendship_requestRequestModels
from app.common.docs.response_models import CommonResponseModels
from ..middlewares.auth_middleware import auth_middleware
from ..user.repository import UserRepository
from sqlalchemy.exc import NoResultFound, OperationalError
from .repository import FriendshipRequestRepository
from ..auth.util import AuthFunctions

friendship_request_namespace = Namespace('friendship_request', 'Friendship_request Route')
requests = Friendship_requestRequestModels(friendship_request_namespace)
responses = Friendship_requestResponseModels(friendship_request_namespace)
common_responses = CommonResponseModels(friendship_request_namespace)
user_repository = UserRepository(db)
friendship_request_repository = FriendshipRequestRepository(db)
auth_functions = AuthFunctions()


@auth_middleware
@friendship_request_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@friendship_request_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@friendship_request_namespace.response(code=409, model=common_responses.unauthorized, description='Unauthorized')
@friendship_request_namespace.route('')
class Friendship_requestResource(Resource):
    def get(self):
        status = request.args.get('status')
        sent = request.args.get('sent')
        user_id = auth_functions.decode_jwt((request.headers.get('Authorization')))['user_id']

        if sent == 'true':
            friendship_requests = friendship_request_repository.get_sent(user_id, status)
            return friendship_requests
        elif sent == 'false':
            friendship_requests = friendship_request_repository.get_received(user_id, status)
            return friendship_requests
        else:
            friendship_requests = friendship_request_repository.get_all(user_id, status)
            return friendship_requests

    def post(self):
        recipient_id = request.get_json()['recipient_id']

        sender_id = auth_functions.decode_jwt((request.headers.get('Authorization')))['user_id']

        schema = CreateFriendshipRequestSchema()
        validated_data = schema.dump({
            "recipient_id": recipient_id,
            "sender_id": sender_id,
            "id": uuid.uuid4()
        })
        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400

        try:
            sender_user = user_repository.get(sender_id)
        except NoResultFound:
            return {
                "message": "Unauthorized!"
            }, 401

        try:
            recipient_user = user_repository.get(recipient_id)
        except NoResultFound:
            return {
                "message": "No User Found"
            }, 404

        try:
            sender_friends_str: str = sender_user['friends']
            sender_friends = sender_friends_str.split(',')

            already_friend_index = sender_friends.index(recipient_user['id'])

            if already_friend_index is not None:
                return {
                    "message": 'You are already friends'
                }, 400
        except ValueError:
            pass

        friendship_already_requested = friendship_request_repository.get_one(sender_id=sender_id, recipient_id=recipient_id)

        if friendship_already_requested is not None:
            return {
                "message": 'You had already sent a friendship request for this user'
            }, 400

        friendship_request = friendship_request_repository.create(sender_id=validated_data['sender_id'],
                                                                  recipient_id=validated_data['recipient_id'],
                                                                  id=validated_data['id'])

        return {
            "message": "Friendship request sent",
            'friendship_request': {
                "id": friendship_request.id,
                "sender_id": friendship_request.sender_id,
                "recipient_id": friendship_request.recipient_id,
                "status": friendship_request.status
            }
        }, 200


@friendship_request_namespace.route('/<id>')
class UniqueFriendship_requestResource(Resource):
    def put(self, id):
        data = request.get_json()
        schema = UpdateFriendshipRequestSchema()
        validated_data = schema.dump(data)

        user_id = auth_functions.decode_jwt(request.headers.get('Authorization'))['user_id']

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400

        try:
            friendship_request = friendship_request_repository.get_one_by_id(id)
        except NoResultFound:
            return {
                "message": "No friendship request with this id was found"
            }, 404

        if friendship_request['recipient_id'] != user_id:
            return {
                "message": "The user_id don't correspond to this friendship request's recipient_id"
            }, 400

        if validated_data['status'] == 'accepted':
            friendship_request_repository.update(friendship_request['id'], status='accepted')

            user_repository.add_friend(friendship_request['recipient_id'], friendship_request['sender_id'])
            return {
                "message": 'friendship request successfully accepted'
            }, 200
        elif validated_data['status'] == 'refused':
            friendship_request_repository.update(friendship_request['id'], status='refused')

            return {
                "message": 'friendship request successfully refused'
            }

    def delete(self):
        pass
