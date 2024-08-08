import pytest
from flask import Flask
from flask_restx import Api
from app.db import db
from app.user.user import user_namespace
from app.auth.auth import auth_namespace
from app.friendship_request.friendship_request import friendship_request_namespace
import datetime
import jwt
import os
from app.user.user_repository import UserRepository


@pytest.fixture
def user(client):
    response = client.post('/user', json={
        "email": "daniel@email.com",
        "name": "Daniel",
        "password": "Daniel@123"
    })

    return response.json


@pytest.fixture
def user2(client):
    response = client.post('/user', json={
        "email": "daniel2@email.com",
        "name": "Daniel2",
        "password": "Daniel@123"
    })

    return response.json


@pytest.fixture
def access_token(user):
    payload = {
        "user_id": str(user['id']), ''
        "expires_at": str(datetime.datetime.now() + datetime.timedelta(hours=1))
    }

    access_token = jwt.encode(
        payload=payload,
        key=os.getenv('JWT_SECRET')
    )

    return access_token


@pytest.fixture
def user_repository():
    user_repository = UserRepository(db)

    return user_repository

@pytest.fixture
def app():
    app = Flask('test_app')
    api = Api(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_pychat.db"
    app.config['TESTING'] = True

    db.init_app(app)

    api.add_namespace(user_namespace)
    api.add_namespace(auth_namespace)
    api.add_namespace(friendship_request_namespace)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

