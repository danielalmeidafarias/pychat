from app.db import db
from datetime import datetime


class Chat(db.Model):
    def __init__(self):
       pass

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    messages = db.relationship('Message', backref='chat')

    def __repr__(self) -> str:
        return f"{{id:{self.id}}}"
