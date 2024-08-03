import json
from flask_restx import Resource, Namespace
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound
from flask import request
from .schemas import SignInSchema
from marshmallow import ValidationError
from ..user.model import UserModel
import bcrypt
from dotenv import load_dotenv
import os
import jwt
import datetime
from .docs.response_models import AuthResponseModels
from .docs.request_models import AuthRequestModels
from app.db import db, r
from ..middlewares.blocked_ip_middleware import middleware

load_dotenv()

auth_namespace = Namespace(name='auth', description='Authorization route')

requests = AuthRequestModels(auth_namespace)
responses = AuthResponseModels(auth_namespace)


@auth_namespace.route('')
class AuthResource(Resource):
    @middleware.blocked_ip_middleware
    @auth_namespace.expect(requests.signin)
    @auth_namespace.response(model=responses.post_200, description="Success", code=200)
    @auth_namespace.response(model=responses.post_400, description="Some field is wrong", code=400)
    @auth_namespace.response(model=responses.post_401, description="Wrong login credentials", code=401)
    @auth_namespace.response(model=responses.post_404, description="No user account found", code=404)
    def post(self):
        data = request.get_json()
        ip_address = request.origin
        schema = SignInSchema()
        validated_data = schema.dump(data)

        try:
            schema.load(validated_data)
        except ValidationError as err:
            return {"message": "Data Validation Error!", "errors": err.messages}, 400

        try:
            user = db.session.execute(db.select(UserModel).filter_by(email=validated_data["email"])).scalar_one()

            login_trying_count = r.get(f"login_count:{user.id}")

            if login_trying_count is not None and int(login_trying_count) >= 20:
                r.set(f"blocked_ip:{ip_address}", 1)
                r.expireat(f"blocked_ip:{ip_address}", datetime.datetime.now() + datetime.timedelta(days=1))

                return {
                    "message": f"Ip address {ip_address} is temporary blocked"
                }, 401
            elif login_trying_count is not None and int(login_trying_count) >= 5:
                r.set(f"login_count:{user.id}", int(login_trying_count) + 1)
                r.expireat(f"login_count:{user.id}", datetime.datetime.now() + datetime.timedelta(minutes=15))

                return {
                    "message": "Too many login attempts, try again later"
                }, 401
        except NoResultFound:
            return {
                "message": "No user with this credentials was found, please check the email"
            }, 404

        is_password_correct = bcrypt.checkpw(
            password=str.encode(validated_data["password"]),
            hashed_password=user.password
        )

        if is_password_correct:
            if login_trying_count is not None:
                r.delete(f"login_count:{user.id}")

            payload = {
                "user_id": str(user.id),
                "expires_at": str(datetime.datetime.now() + datetime.timedelta(hours=1))
            }

            access_token = jwt.encode(
                payload=payload,
                key=os.getenv('JWT_SECRET')
            )

            return {
                "access_token": access_token
            }, 200
        else:
            if login_trying_count is None:
                r.set(f"login_count:{user.id}", 1)
            else:
                r.set(f"login_count:{user.id}", int(login_trying_count) + 1)
                r.expireat(f"login_count:{user.id}", datetime.datetime.now() + datetime.timedelta(minutes=15))

            return {
                "message": "Unauthorized"
            }, 401
