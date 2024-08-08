import uuid

from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from uuid import UUID as UUID4
from app.db import db


class UserModel(db.Model):
    def __init__(self, id, email, name, password):
        self.id = id
        self.email = email
        self.name = name
        self.password = password

    __table_args__ = {'extend_existing': True}

    __tablename__ = 'user'
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes] = mapped_column()

    friends: Mapped[str] = mapped_column(default='')
    friendship_request: Mapped[str] = mapped_column(default='')
    sent_friendship_request: Mapped[str] = mapped_column(default='')

    def __repr__(self) -> str:
        return f"{{id:{self.id}, \
        name:{self.name}, \
        email: {self.email}, \
        password: {self.password}, \
        friends:{self.friends}, \
        friendship_request: {self.friendship_request} \
        sent_friendship_request: {self.friendship_request} \
        }}"
