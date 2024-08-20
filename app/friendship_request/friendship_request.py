from flask import request
from flask_restx import Resource, Namespace
from app.db import db
from .docs.response_models import Friendship_requestResponseModels
from .docs.request_models import Friendship_requestRequestModels
from app.common.docs.response_models import CommonResponseModels
from ..middlewares.auth_middleware import auth_middleware
from ..user.repository import UserRepository
from .repository import FriendshipRequestRepository
from ..auth.util import AuthFunctions
from .service import FriendshipRequestService
from ..friendship.repository import FriendshipRepository

friendship_request_namespace = Namespace('friendship_request', 'Friendship_request Route')
requests = Friendship_requestRequestModels(friendship_request_namespace)
responses = Friendship_requestResponseModels(friendship_request_namespace)
common_responses = CommonResponseModels(friendship_request_namespace)
user_repository = UserRepository(db)
friendship_request_repository = FriendshipRequestRepository(db)
auth_functions = AuthFunctions()
friendship_request_service = FriendshipRequestService(
    friendship_request_repository=friendship_request_repository,
    user_repository=user_repository,
    auth_functions=auth_functions,
    friendship_repository=FriendshipRepository(db)
)


@auth_middleware
@friendship_request_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@friendship_request_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@friendship_request_namespace.response(code=409, model=common_responses.unauthorized, description='Unauthorized')
@friendship_request_namespace.route('')
class FriendshipRequestResource(Resource):
    def get(self):
        return friendship_request_service.get(request)

    def post(self):
        return friendship_request_service.create(request)

@friendship_request_namespace.route('/<friendship_request_id>')
class UniqueFriendshipRequestResource(Resource):
    def put(self, friendship_request_id):
        return friendship_request_service.update(request, friendship_request_id)

    def delete(self):
        pass
