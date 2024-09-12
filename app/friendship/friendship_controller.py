from flask import request, make_response, render_template
from flask_restx import Resource, Namespace
from marshmallow.exceptions import ValidationError
from .friendship_schemas import GetFriendshipSchema
from .docs.response_models import FriendshipResponseModels
from .docs.request_models import FriendshipRequestModels
from app.common.docs.response_models import CommonResponseModels
from ..middlewares.auth_middleware import auth_middleware
from ..middlewares.validate_data_middleware import ValidateDataMiddleware
from ..auth.util import auth_functions
from ..user.user_controller import user_repository

friendship_namespace = Namespace('friendship', 'Friendship Route')
requests = FriendshipRequestModels(friendship_namespace)
responses = FriendshipResponseModels(friendship_namespace)
common_responses = CommonResponseModels(friendship_namespace)


@friendship_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@friendship_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@friendship_namespace.response(code=409, model=common_responses.unauthorized, description='Unauthorized')
@friendship_namespace.route('')
class FriendshipResource(Resource):
    @auth_middleware
    @ValidateDataMiddleware(GetFriendshipSchema).middleware
    def get(self):
        user_id = auth_functions.decode_jwt(request.cookies.get('authorization'))['user_id']
        user = user_repository.get_one(user_id)

        search = request.args.get('search')

        if search is not None:
            results = user_repository.search(user_id, search)
            response = make_response(render_template('friends.html', results=results, user=user))
        else:
            response = make_response(render_template('friends.html'))

        return response

@friendship_namespace.route('/<id>')
class UniqueFriendshipResource(Resource):
    def delete(self):
        pass
