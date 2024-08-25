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
from app.user.repository import UserRepository
from app.friendship.repository import FriendshipRepository
from app.friendship_request.repository import FriendshipRequestRepository
from app.chat.repository import ChatRepository
from app.chat_members.repository import ChatMemberRepository
from app.message.repository import MessageRepository
from flask_socketio import test_client
from flask_socketio.test_client import SocketIOTestClient
from app.chat.websocket import Websocket

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
def user3(client):
    response = client.post('/user', json={
        "email": "daniel3@email.com",
        "name": "Daniel3",
        "password": "Daniel@123"
    })

    return response.json


@pytest.fixture
def user4(client):
    response = client.post('/user', json={
        "email": "daniel4@email.com",
        "name": "Daniel4",
        "password": "Daniel@123"
    })

    return response.json


@pytest.fixture
def access_token(user):
    payload = {
        "user_id": str(user['id']),
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
def friendship_repository():
    friendship_repository = FriendshipRepository(db)

    return friendship_repository

@pytest.fixture
def friendship_request_repository():
    friendship_request_repository = FriendshipRequestRepository(db)

    return friendship_request_repository

@pytest.fixture
def chat_repository():
    chat_repository = ChatRepository(db)

    return chat_repository

@pytest.fixture
def chat_members_repository():
    chat_members_repository = ChatMemberRepository(db)

    return chat_members_repository

@pytest.fixture
def message_repository():
    message_repository = MessageRepository(db)

    return message_repository


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


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def socketio(app):
    socketio = Websocket(app)
    return socketio


@pytest.fixture
def socketio_client(app, socketio):
    websocket_client = SocketIOTestClient(app, socketio)
    return websocket_client


@pytest.fixture
def friendship_request(client, user, user2, access_token, friendship_request_repository):
    sender_id = user['id']
    recipient_id = user2['id']

    client.post("/friendship_request", headers={
        'Authorization': access_token
    }, json={
        'recipient_id': recipient_id
    })

    friendship_request = friendship_request_repository.get_one(recipient_id=recipient_id, sender_id=sender_id)

    return friendship_request
