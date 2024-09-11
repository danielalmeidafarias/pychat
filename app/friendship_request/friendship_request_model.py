from app.db import db
from datetime import datetime

class FriendshipRequest(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    sender_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __repr__(self) -> str:
        return f"{{id:{self.id}, \
        sender_id: {self.sender_id}, \
        receiver_id: {self.receiver_id}, \
        status: {self.status}, \
        created_at: {self.created_at}"
