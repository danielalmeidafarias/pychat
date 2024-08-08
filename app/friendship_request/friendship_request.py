from flask import request
from flask_restx import Resource, Namespace
from app.db import db
from marshmallow.exceptions import ValidationError
from .model import Friendship_requestModel
from .schemas import GetFriendshipRequestSchema, CreateFriendshipRequestSchema, UpdateFriendshipRequestSchema, DeleteFriendshipRequestSchema
from .docs.response_models import Friendship_requestResponseModels
from .docs.request_models import Friendship_requestRequestModels
from app.common.docs.response_models import CommonResponseModels
from ..middlewares.auth_middleware import auth_middleware, decode_jwt
from ..user.user_repository import UserRepository
from sqlalchemy.exc import NoResultFound, OperationalError

friendship_request_namespace = Namespace('friendship_request', 'Friendship_request Route')
requests = Friendship_requestRequestModels(friendship_request_namespace)
responses = Friendship_requestResponseModels(friendship_request_namespace)
common_responses = CommonResponseModels(friendship_request_namespace)
user_repository = UserRepository(db)


@auth_middleware
@friendship_request_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@friendship_request_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@friendship_request_namespace.response(code=409, model=common_responses.unauthorized, description='Unauthorized')
@friendship_request_namespace.route('')
class Friendship_requestResource(Resource):
    # Receber as solicitações
    def get(self):
        pass

    # Enviar uma solicitação
    # Caso ja forem amigos ou ja foi enviado uma solicitação, não deve ser possivel enviar
    def post(self):
        data = request.get_json()
        schema = CreateFriendshipRequestSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400

        requesting_user_id = decode_jwt(request.headers.get('Authorization'))['user_id']

        try:
            requesting_user = user_repository.get(requesting_user_id)
        except NoResultFound:
            return {
                "message": "Unauthorized!"
            }, 401

        try:
            recipient_user = user_repository.get(validated_data['recipient_id'])
        except NoResultFound:
            return {
                "message": "No User Found"
            }, 404

        try:
            user_friends_str: str = requesting_user['friends']
            user_friends = user_friends_str.split(',')

            already_friend_index = user_friends.index(recipient_user['id'])

            if already_friend_index is not None:
                return {
                    "message": 'You are already friends'
                }, 400
        except ValueError:
            pass

        try:
            user_friendship_requests_str = requesting_user['sent_friendship_request']
            user_friendship_requests = user_friendship_requests_str.split(',')
            friendship_request_already_sent_index = user_friendship_requests.index(recipient_user['id'])

            if friendship_request_already_sent_index is not None:
                return {
                    "message": 'You had already sent a friendship_request for this user'
                }, 400
        except ValueError:
            pass

        try:
            user_repository.update(requesting_user_id, {'sent_friendship_request': validated_data['recipient_id']})
            user_repository.update(validated_data['recipient_id'], {'friendship_request': requesting_user_id})

            db.session.commit()
        except OperationalError:
            db.session.rollback()
            return {
                "message": "Invalid data"
            }, 400

        return {
            "message": "Friendship request sent"
        }, 200


@friendship_request_namespace.route('/<id>')
class UniqueFriendship_requestResource(Resource):
    # Aceitar ou recusar uma solicitação
    # Nesse caso deve ser modificado dos dois usuarios envolvidos
    def put(self):
        data = request.get_json()
        schema = UpdateFriendship_requestSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {'message': 'Data Validation Error!', 'errors': err.messages}, 400
        pass

    # Remover solicitações
    # Deve recusar uma solicitação caso esta ainda esteja em aberto
        # Nesse caso deve ser modificado dos dois usuarios envolvidos
    def delete(self):
        pass
