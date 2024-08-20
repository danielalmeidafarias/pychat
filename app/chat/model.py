from app.db import db
from datetime import datetime
from ..chat_members.model import chat_members


class Chat(db.Model):
    def __init__(self, chat_id: str):
        self.id = chat_id

    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())

    messages = db.relationship('Message', backref='chat')
    chat_members = db.relationship('Chat', primaryjoin=id==chat_members.c.user_id, secondaryjoin=id==chat_members.c.chat_id,
                            backref=db.backref('chat_of'), secondary=chat_members)

    def __repr__(self) -> str:
        return f"{{id:{self.id}}}"
