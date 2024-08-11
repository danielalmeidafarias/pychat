from sqlalchemy.orm import Mapped, mapped_column
from app.db import db


class FriendshipRequestModel(db.Model):
    def __init__(self, id, sender_id, recipient_id):
        self.id = id
        self.sender_id = sender_id
        self.recipient_id = recipient_id

    __table_args__ = {'extend_existing': True}

    id: Mapped[str] = mapped_column(primary_key=True)
    sender_id: Mapped[str] = mapped_column(nullable=False)
    recipient_id: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default='open')

    def __repr__(self) -> str:
        return f"{{id:{self.id}, sender_id: {self.sender_id}, recipient_id: {self.recipient_id}, status: {self.status}"
