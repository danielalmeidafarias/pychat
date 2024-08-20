from abc import ABC, abstractmethod
from flask import Request, jsonify
from .schemas import CreateFriendshipRequestSchema, UpdateFriendshipRequestSchema
from sqlalchemy.exc import NoResultFound, IntegrityError
from marshmallow.exceptions import ValidationError
from ..user.service import UserRepositoryInterface
from ..auth.util import AuthFunctions
from ..friendship.repository import FriendshipRepository

class FriendshipRequestRepositoryInterface(ABC):
    @abstractmethod
    def create(self, sender_id: str, receiver_id: str):
        pass

    @abstractmethod
    def get_one(self, sender_id: str, receiver_id: str):
        pass

    @abstractmethod
    def get_one_by_id(self, id):
        pass

    @abstractmethod
    def get_sent(self, sender_id, status: str or None):
        pass

    @abstractmethod
    def get_received(self, receiver_id, status: str or None):
        pass

    @abstractmethod
    def get_all(self, user_id, status: str or None):
        pass

    @abstractmethod
    def update(self, friendship_request_id: str, status):
        pass

    @abstractmethod
    def delete(self, friendship_request_id: str):
        pass


class FriendshipRequestService:
    def __init__(self, friendship_request_repository: FriendshipRequestRepositoryInterface,
                 user_repository: UserRepositoryInterface,
                 auth_functions: AuthFunctions,
                 friendship_repository: FriendshipRepository
                 ):
        self.friendship_request_repository = friendship_request_repository
        self.user_repository = user_repository
        self.auth_functions = auth_functions
        self.friendship_repository = friendship_repository

    def create(self, request: Request):
        receiver_id = request.get_json()['receiver_id']

        sender_id = self.auth_functions.decode_jwt((request.headers.get('Authorization')))['user_id']

        schema = CreateFriendshipRequestSchema()

        validated_data = schema.dump({
            "receiver_id": receiver_id,
            "sender_id": sender_id,
        })

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400

        try:
            sender_user = self.user_repository.get_one(sender_id)
        except NoResultFound:
            return {
                "message": "Unauthorized!"
            }, 401

        try:
            self.user_repository.get_one(receiver_id)
        except NoResultFound:
            return {
                "message": "No User Found"
            }, 404

        for friend in sender_user['friends']:
            if friend.id == receiver_id:
                return {
                    "message": 'You are already friends',
                }, 400

        friendship_already_requested = self.friendship_request_repository.get_one(sender_id=sender_id,
                                                                             receiver_id=receiver_id)
        if friendship_already_requested is not None:
            return {
                "message": 'You had already sent a friendship request for this user'
            }, 400

        try:
            friendship_request = self.friendship_request_repository.create(sender_id=sender_id,
                                                                      receiver_id=receiver_id)

            return {
                "message": "Friendship request sent",
                'friendship_request': {
                    "id": friendship_request.id,
                    "sender_id": friendship_request.sender_id,
                    "receiver_id": friendship_request.receiver_id,
                    "status": friendship_request.status
                }
            }, 200
        except IntegrityError as err:
            print(err)
            return {
                "message": 'You are already friends'
            }, 500

    def get(self, request: Request):
        status = request.args.get('status')
        sent = request.args.get('sent')
        user_id = self.auth_functions.decode_jwt((request.headers.get('Authorization')))['user_id']

        if sent == 'true':
            friendship_requests = self.friendship_request_repository.get_sent(user_id, status)
            return friendship_requests
        elif sent == 'false':
            friendship_requests = self.friendship_request_repository.get_received(user_id, status)
            return friendship_requests
        else:
            friendship_requests = self.friendship_request_repository.get_all(user_id, status)
            return friendship_requests

        pass

    def update(self, request: Request, friendship_request_id):
        data = request.get_json()
        schema = UpdateFriendshipRequestSchema()
        validated_data = schema.dump(data)

        user_id = self.auth_functions.decode_jwt(request.headers.get('Authorization'))['user_id']

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400

        try:
            friendship_request = self.friendship_request_repository.get_one_by_id(friendship_request_id)
        except NoResultFound:
            return {
                "message": "No friendship request with this id was found"
            }, 404

        if friendship_request['receiver_id'] != user_id:
            return {
                "message": "The user_id don't correspond to this friendship request's receiver_id"
            }, 400

        if validated_data['status'] == 'accepted':
            self.friendship_request_repository.update(friendship_request_id, status='accepted')

            self.friendship_repository.create(user_id=user_id, friend_id=friendship_request['sender_id'])

            return {
                "message": 'friendship request successfully accepted'
            }, 200
        elif validated_data['status'] == 'refused':
            self.friendship_request_repository.update(friendship_request_id, status='refused')

            return {
                "message": 'friendship request successfully refused'
            }

    def delete(self):
        pass

