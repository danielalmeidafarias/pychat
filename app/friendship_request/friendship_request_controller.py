from flask import request
from flask_restx import Resource, Namespace
from app.db import db
from .docs.response_models import Friendship_requestResponseModels
from .docs.request_models import Friendship_requestRequestModels
from app.common.docs.response_models import CommonResponseModels
from .friendship_request_schemas import GetFriendshipRequestSchema, CreateFriendshipRequestSchema, UpdateFriendshipRequestSchema
from ..user.user_repository import UserRepository
from .friendship_request_repository import FriendshipRequestRepository
from ..auth.util import auth_functions
from .friendship_request_service import FriendshipRequestService
from ..friendship.friendship_repository import FriendshipRepository
from ..chat.chat_repository import ChatRepository
from ..chat_members.chat_members_repository import ChatMemberRepository
from ..middlewares.auth_middleware import auth_middleware
from ..middlewares.validate_route_middleware import ValidateRouteMiddleware

friendship_request_namespace = Namespace('friendship_request', 'Friendship_request Route')
requests = Friendship_requestRequestModels(friendship_request_namespace)
responses = Friendship_requestResponseModels(friendship_request_namespace)
common_responses = CommonResponseModels(friendship_request_namespace)
user_repository = UserRepository(db)
friendship_request_repository = FriendshipRequestRepository(db)
chat_repository = ChatRepository(db)
chat_members_repository = ChatMemberRepository(db)

friendship_request_service = FriendshipRequestService(
    friendship_request_repository=friendship_request_repository,
    user_repository=user_repository,
    auth_functions=auth_functions,
    friendship_repository=FriendshipRepository(db),
    chat_repository=chat_repository,
    chat_members_repository=chat_members_repository
)


@friendship_request_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@friendship_request_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@friendship_request_namespace.response(code=409, model=common_responses.unauthorized, description='Unauthorized')
@friendship_request_namespace.route('')
class FriendshipRequestResource(Resource):
    @auth_middleware
    @ValidateRouteMiddleware(GetFriendshipRequestSchema).middleware
    def get(self):
        return friendship_request_service.get(request=request)

    @ValidateRouteMiddleware(CreateFriendshipRequestSchema).middleware
    def post(self):
        return friendship_request_service.create(request)

@friendship_request_namespace.route('/<friendship_request_id>')
class UniqueFriendshipRequestResource(Resource):
    @auth_middleware
    @ValidateRouteMiddleware(UpdateFriendshipRequestSchema).middleware
    def put(self, friendship_request_id):
        return friendship_request_service.update(request, friendship_request_id)

    @auth_middleware
    def delete(self, friendship_request_id):
        return friendship_request_service.delete(friendship_request_id)
