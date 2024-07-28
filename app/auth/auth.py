import json
from flask_restx import Resource, Namespace
from flask_sqlalchemy import SQLAlchemy
from .docs.request_models import request_models
from flask import request
from .schemas import SignInSchema
from marshmallow import ValidationError
from ..user.model import get_user_model
import bcrypt
from dotenv import load_dotenv
import os
import jwt
import datetime

load_dotenv()


def auth(db: SQLAlchemy):
    auth_namespace = Namespace(name='auth', description='Authorization route')

    signin_model = request_models(auth_namespace)

    @auth_namespace.route('')
    class AuthResource(Resource):
        @auth_namespace.expect(signin_model)
        def post(self):
            data = request.get_json()
            schema = SignInSchema()
            validated_data = schema.dump(data)

            user_model = get_user_model(db)

            try:
                schema.load(validated_data)
            except ValidationError as err:
                return {"message": "Data Validation Error!", "errors": err.messages}

            user = db.session.execute(db.select(user_model).filter_by(email=validated_data["email"])).scalar_one()

            is_password_correct = bcrypt.checkpw(password=str.encode(validated_data["password"]), hashed_password=user.password)

            if is_password_correct:
                payload = {
                    "user_id": str(user.id),
                    "expires_at": str(datetime.datetime.now() + datetime.timedelta(days=1))
                }

                access_token = jwt.encode(
                    payload=payload,
                    key=os.getenv('JWT_SECRET')
                )

                return {
                    "access_token": access_token
                }, 200
            else:
                return {
                    "message": "Unauthorized"
                }, 401

    return auth_namespace
