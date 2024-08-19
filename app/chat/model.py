from app.db import db
from datetime import datetime


chat_members = db.Table('chat_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'), primary_key=True)
)

class Chat(db.Model):
    def __init__(self):
       pass

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    messages = db.relationship('Message', backref='chat')
    chat_members = db.relationship('Chat', primaryjoin=id==chat_members.c.user_id, secondaryjoin=id==chat_members.c.chat_id,
                            backref=db.backref('chat_of'), secondary=chat_members)

    def __repr__(self) -> str:
        return f"{{id:{self.id}}}"
