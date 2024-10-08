from abc import ABC, abstractmethod
from flask import Request, make_response, render_template
from sqlalchemy.exc import NoResultFound, IntegrityError
from ..user.user_service import UserRepositoryInterface
from ..auth.util import AuthFunctions
from ..friendship.friendship_repository import FriendshipRepository
from ..chat.chat_repository import ChatRepository
from ..chat_members.chat_members_repository import ChatMemberRepository

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
                 friendship_repository: FriendshipRepository,
                 chat_repository: ChatRepository,
                 chat_members_repository: ChatMemberRepository,
                 ):
        self.friendship_request_repository = friendship_request_repository
        self.user_repository = user_repository
        self.auth_functions = auth_functions
        self.friendship_repository = friendship_repository
        self.chat_repository = chat_repository
        self.chat_members_repository = chat_members_repository

    def create(self, request: Request):
        receiver_id = request.get_json()['receiver_id']

        sender_id = self.auth_functions.decode_jwt((request.cookies.get('authorization')))['user_id']

        try:
            sender_user = self.user_repository.get_one(sender_id)
        except NoResultFound:
            response = make_response({
                "message": "Unauthorized!"
            })
            response.status_code = 401
            return response

        try:
            self.user_repository.get_one(receiver_id)
        except NoResultFound:
            return make_response({
                "message": "No User Found"
            }, 404)


        already_friends = self.friendship_repository.get(user_id=sender_id, friend_id=receiver_id)

        if already_friends is not None:
            return make_response({
                    "message": 'You are already friends',
                }, 400)

        friendship_already_requested = self.friendship_request_repository.get_one(sender_id=sender_id,
                                                                             receiver_id=receiver_id)
        if friendship_already_requested is not None:
            return make_response({
                "message": 'You had already sent a friendship request for this user'
            }, 400)

        try:
            friendship_request = self.friendship_request_repository.create(sender_id=sender_id,
                                                                      receiver_id=receiver_id)

            return make_response({
                "message": "Friendship request sent",
                'friendship_request': {
                    "id": friendship_request.id,
                    "sender_id": friendship_request.sender_id,
                    "receiver_id": friendship_request.receiver_id,
                    "status": friendship_request.status
                }
            }, 200)
        except IntegrityError as err:
            print(err)
            return make_response({
                "message": 'You are already friends'
            }, 500)

    def get(self, request: Request):
        user_id = self.auth_functions.decode_jwt(request.cookies.get('authorization'))['user_id']
        user = self.user_repository.get_one(user_id)

        received = self.friendship_request_repository.get_received(user_id, None)
        sent = self.friendship_request_repository.get_sent(user_id, None)

        response = make_response(render_template('friendship_request.html', user=user, received=received, sent=sent))
        return response

    def update(self, request: Request, friendship_request_id):
        data = request.get_json()

        user_id = self.auth_functions.decode_jwt(request.cookies.get('authorization'))['user_id']

        try:
            friendship_request = self.friendship_request_repository.get_one_by_id(friendship_request_id)
        except NoResultFound:
            return make_response({
                "message": "No friendship request with this id was found"
            }, 404)


        if friendship_request['receiver_id'] != user_id:
            return make_response({
                "message": "The user_id don't correspond to this friendship request's receiver_id"
            }, 400)

        if data['status'] == 'accepted':
            self.friendship_request_repository.update(friendship_request_id, status='accepted')

            self.friendship_repository.create(user_id=user_id, friend_id=friendship_request['sender_id'])

            new_chat = self.chat_repository.create(chat_name=None)

            try:
                self.chat_members_repository.create(chat_id=new_chat['id'], user_id=user_id)
                self.chat_members_repository.create(chat_id=new_chat['id'], user_id=friendship_request['sender_id'])

            except Exception as err:
                print(err)

            self.friendship_request_repository.delete(friendship_request_id)

            return make_response({
                "message": 'friendship request successfully accepted'
            }, 200)
        elif data['status'] == 'refused':
            self.friendship_request_repository.update(friendship_request_id, status='refused')

            return make_response({
                "message": 'friendship request successfully refused'
            })

    def delete(self, friendship_request_id: str):
        try:
            self.friendship_request_repository.delete(friendship_request_id)
            return make_response({
                "message": "Friendship request deleted!"
            })
        except Exception as err:
            print(err)
            return make_response(
                {"message": "error"}, 400
            )
