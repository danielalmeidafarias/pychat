from flask import Flask, render_template
from flask_restx import Api
from flask_cors import CORS
from .db import db
from .user.user import user_namespace, account_namespace
from .auth.auth import auth_namespace
from .chat.chat import chat_namespace
from .friendship_request.friendship_request import friendship_request_namespace
from .friendship.friendship import friendship_namespace
from .chat.model import Chat
from .message.model import Message
from flask_socketio import SocketIO
from .chat.websocket import ChatWebsocket
from .db import db
from flask_bootstrap import Bootstrap4


def create_app():
    app = Flask(__name__)

    # CORS(app, resources={"*": {"origins": "*"}})
    CORS(app)

    app.config['SECRET_KEY'] = 'SUPER SECRET KEY'
    app.config['CORS_HEADERS'] = 'Content-Type'

    socketio = ChatWebsocket(app, cors_allowed_origins="*", db=db)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('not_found.html'), 404

    api = Api(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pychat.db"

    db.init_app(app)

    api.add_namespace(user_namespace)
    api.add_namespace(auth_namespace)
    api.add_namespace(friendship_request_namespace)
    api.add_namespace(chat_namespace)
    api.add_namespace(friendship_namespace)
    api.add_namespace(account_namespace)

    with app.app_context():
        db.create_all()

    socketio.run(app, debug=True)

    return app, socketio
