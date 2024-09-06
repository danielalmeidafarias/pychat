from app.db import db
from datetime import datetime


class Chat(db.Model):
    def __init__(self, chat_id: str, chat_name: str | None):
        self.id = chat_id
        self.name = chat_name

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())

    messages = db.relationship('Message', backref='chat')

    # chat_members = db.relationship('User', secondary=chat_members, overlaps="chats")

    def __repr__(self) -> str:
        return f"{{id:{self.id}, messages:{self.messages}}}"
