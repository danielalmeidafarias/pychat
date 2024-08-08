import uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.db import db


class Friendship_requestModel(db.Model):
    def __init__(self):
       pass

    __table_args__ = {'extend_existing': True}

    __tablename__ = 'user'

    id: Mapped[str] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"{{id:{self.id}}}"

