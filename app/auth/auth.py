from flask_restx import Resource, Namespace
from sqlalchemy.exc import NoResultFound
from flask import request
from .schemas import SignInSchema
from marshmallow import ValidationError
from ..user.model import UserModel
from dotenv import load_dotenv
import datetime
from .docs.response_models import AuthResponseModels
from .docs.request_models import AuthRequestModels
from ..common.docs.response_models import CommonResponseModels
from app.db import db, r
from ..middlewares.blocked_ip_middleware import blocked_ip_middleware
from ..middlewares.ddos_protect_middleware import ddos_protect_middleware


load_dotenv()
auth_namespace = Namespace(name='auth', description='Authorization route')
requests = AuthRequestModels(auth_namespace)
responses = AuthResponseModels(auth_namespace)
common_responses = CommonResponseModels(auth_namespace)
from .functions.functions import AuthFunctions


auth_functions = AuthFunctions()

@auth_namespace.route('')
@auth_namespace.response(code=500, model=common_responses.internal_error, description='Something went wrong')
@auth_namespace.response(code=400, model=common_responses.data_validation_error, description='Data Validation Error')
@auth_namespace.response(code=401, model=common_responses.unauthorized, description='Unauthorized')
@auth_namespace.response(code=404, model=common_responses.no_user_found, description='No User Found')
class AuthResource(Resource):
    @ddos_protect_middleware
    @blocked_ip_middleware
    @auth_namespace.expect(requests.signin)
    @auth_namespace.response(model=responses.post_200, description="Success", code=200)
    def post(self):
        data = request.get_json()
        schema = SignInSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {"message": "Data Validation Error!", "errors": err.messages}, 400

        try:
            user = db.session.execute(db.select(UserModel).filter_by(email=validated_data["email"])).scalar_one()
        except NoResultFound:
            return {
                "message": "No user with this credentials was found, please check the email"
            }, 404

        is_password_correct = auth_functions.is_password_correct(validated_data['password'], user.password)

        if is_password_correct:
            r.delete(f"login_count:{user.id}")

            access_token = auth_functions.get_access_token(user.id)

            return {
                "access_token": access_token
            }, 200
        else:
            login_trying_count = r.get(f"login_count:{user.id}")

            if login_trying_count is None:
                r.set(f"login_count:{user.id}", 1)
                r.expireat(f"login_count:{user.id}", datetime.datetime.now() + datetime.timedelta(minutes=15))
            else:
                r.set(f"login_count:{user.id}", int(login_trying_count) + 1)
                r.expireat(f"login_count:{user.id}", datetime.datetime.now() + datetime.timedelta(minutes=15))

                if int(login_trying_count) >= 20:
                    ip_address = request.origin

                    r.set(f"blocked_ip:{ip_address}", 1)
                    r.expireat(f"blocked_ip:{ip_address}", datetime.datetime.now() + datetime.timedelta(days=1))

                if int(login_trying_count) >= 5:
                    r.set(f"login_count:{user.id}", int(login_trying_count) + 1)
                    r.expireat(f"login_count:{user.id}", datetime.datetime.now() + datetime.timedelta(minutes=15))

                    return {
                        "message": "Too many login attempts, try again later"
                    }, 401

            return {
                "message": "Unauthorized"
            }, 401
