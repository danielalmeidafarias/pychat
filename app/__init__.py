from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from .db import db
from .user.user import user_namespace
from .auth.auth import auth_namespace


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///youmusic.db"

    db.init_app(app)

    api.add_namespace(user_namespace)
    api.add_namespace(auth_namespace)

    with app.app_context():
        db.create_all()

    app.run(debug=True)

    return app
