from flask import Flask, render_template, request, redirect, make_response, send_file
from flask_restx import Api
from .db import db
from .user.user_controller import UserNamespace
from .auth.auth_controller import auth_namespace
from .chat.chat_controller import chat_namespace
from .friendship_request.friendship_request_controller import friendship_request_namespace
from .friendship.friendship_controller import friendship_namespace
from media.media import media_namespace
from .chat.model import Chat
from .message.message_model import Message
from .chat.websocket import ChatWebsocket
from .db import db

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'SUPER SECRET KEY'
    app.config['CORS_HEADERS'] = 'Content-Type'

    socketio = ChatWebsocket(app, cors_allowed_origins="*", db=db)

    @app.errorhandler(404)
    def page_not_found(e):
        if request.method == "GET":
            return redirect('/auth/signin')
        else:
            return render_template('not_found.html'), 404


    api = Api(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pychat.db"

    db.init_app(app)

    user_namespace = UserNamespace('user', 'asdawdaw')

    api.add_namespace(user_namespace)
    api.add_namespace(auth_namespace)
    api.add_namespace(friendship_request_namespace)
    api.add_namespace(chat_namespace)
    api.add_namespace(friendship_namespace)
    api.add_namespace(media_namespace)

    with app.app_context():
        db.create_all()

    socketio.run(app, debug=True)

    return app, socketio
