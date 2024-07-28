from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from .user.user import user
from .auth.auth import auth


def create_app():
    class Base(DeclarativeBase):
        pass

    db = SQLAlchemy(model_class=Base)

    app = Flask(__name__)
    api = Api(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///youmusic.db"

    db.init_app(app)

    user_namespace = user(db)
    auth_namespace = auth(db)

    api.add_namespace(user_namespace)
    api.add_namespace(auth_namespace)

    with app.app_context():
        db.create_all()

    app.run(debug=True)

    return app
