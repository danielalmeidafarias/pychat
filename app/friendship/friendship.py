from flask import request, make_response, render_template
from flask_restx import Resource, Namespace
from marshmallow.exceptions import ValidationError
from .schemas import CreateFriendshipSchema, UpdateFriendshipSchema
from .docs.response_models import FriendshipResponseModels
from .docs.request_models import FriendshipRequestModels
from app.common.docs.response_models import CommonResponseModels
from ..middlewares.auth_middleware import auth_middleware
from ..auth.util import auth_functions
from ..user.user import user_repository

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


    def post(self):
        data = request.get_json()
        user_repository.search(data['name'])
        pass
        # schema = CreateFriendshipSchema()
        # validated_data = schema.dump(data)
        #
        # try:
        #     schema.load(validated_data)
        # except ValidationError as err:
        #     return {'message': 'Data Validation Error!', 'errors': err.messages}, 400
        # pass


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
