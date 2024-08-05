import uuid

from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from uuid import UUID as UUID4
from app.db import db


class UserModel(db.Model):
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    __table_args__ = {'extend_existing': True}

    __tablename__ = 'user'
    id: Mapped[str] = mapped_column(primary_key=True, default=str(uuid.uuid4()))
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes] = mapped_column()

    def __repr__(self) -> str:
        return f"{{id:{self.id}, name:{self.name}}}"
