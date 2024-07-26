from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from uuid import UUID as UUID4


def user_model(db: SQLAlchemy):
    class UserModel(db.Model):
        def __init__(self, user_id, email, name, password):
            self.id = user_id
            self.email = email
            self.name = name
            self.password = password

        __tablename__ = 'user'
        id: Mapped[UUID4] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column()
        email: Mapped[str] = mapped_column(unique=True)
        password: Mapped[bytes] = mapped_column()

        def __repr__(self) -> str:
            return f"User(id={self.id}, name={self.name}, email={self.email})"

    return UserModel
