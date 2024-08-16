import datetime
from sqlalchemy.orm import Mapped
from app.db import db

class Message(db.Model):
    def __init__(self):
       pass

    id: Mapped[str] = db.Column(db.String(36), primary_key=True)
    content: Mapped[str] = db.Column(db.String, nullable=False)

    created_at: Mapped[str] = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_at: Mapped[str] = db.Column(db.DateTime, nullable=True, default=None)
    deleted_at: Mapped[str] = db.Column(db.DateTime, nullable=True, default=None)

    chat_id: Mapped[str] = db.Column(db.String(36), db.ForeignKey('chat.id'), nullable=False)
    user_id: Mapped[str] = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"{{id:{self.id}}}"
