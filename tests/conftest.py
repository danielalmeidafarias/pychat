import pytest
from flask import Flask
from flask_restx import Api
from app.db import db
from app.user.user import user_namespace
from app.auth.auth import auth_namespace


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
