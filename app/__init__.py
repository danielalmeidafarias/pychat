from flask import Flask
from flask_restx import Api
from .db import db
from .user.user import user_namespace
from .auth.auth import auth_namespace
from .friendship_request.friendship_request import friendship_request_namespace
from .chat.model import Chat
from .message.model import Message

def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pychat.db"

    db.init_app(app)

    api.add_namespace(user_namespace)
    api.add_namespace(auth_namespace)
    api.add_namespace(friendship_request_namespace)

    with app.app_context():
        db.create_all()

    app.run(debug=True)

    return app
