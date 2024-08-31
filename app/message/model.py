import datetime
from app.db import db

class Message(db.Model):
    def __init__(self, message_id: str, chat_id: str, user_id: str, content: str):
        self.id = message_id
        self.chat_id = chat_id
        self.user_id = user_id
        self.content = content

    id = db.Column(db.String(36), primary_key=True)
    content = db.Column(db.String, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, nullable=True, default=None)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    chat_id = db.Column(db.String(36), db.ForeignKey('chat.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"{{id:{self.id}}}"
