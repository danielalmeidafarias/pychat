import pytest
from flask import Flask
from flask_restx import Api
from app.db import db
from app.user.user import user_namespace
from app.auth.auth import auth_namespace
import datetime
import jwt
import os


@pytest.fixture
def created_user(client):
    response = client.post('/user', json={
        "email": "daniel@email.com",
        "name": "Daniel",
        "password": "Daniel@123"
    })

    return response.json

@pytest.fixture()
def access_token():
    payload = {
        "user_id": "a13ee687-8dcb-4c34-9881-5ab6b3bdd9f4",
        "expires_at": str(datetime.datetime.now() + datetime.timedelta(hours=1))
    }

    access_token = jwt.encode(
        payload=payload,
        key=os.getenv('JWT_SECRET')
    )


@pytest.fixture
def app():
    app = Flask('test_app')
    api = Api(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_pychat.db"
    app.config['TESTING'] = True

    db.init_app(app)

    api.add_namespace(user_namespace)
    api.add_namespace(auth_namespace)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

