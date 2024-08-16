import itertools

from flask_sqlalchemy import SQLAlchemy
from .model import FriendshipRequest
from itertools import chain


class FriendshipRequestRepository():
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, id: str, sender_id: str, recipient_id: str):
        friendship_request = FriendshipRequest(
            id=id,
            sender_id=sender_id,
            recipient_id=recipient_id
        )

        self.db.session.add(friendship_request)
        self.db.session.commit()

        return friendship_request

    def get_one(self, sender_id: str, recipient_id: str):
        friendship_request = (self.db.session.query(FriendshipRequest)
                              .where(FriendshipRequest.sender_id == sender_id and
                                     FriendshipRequest.recipient_id == recipient_id).one_or_none())

        return friendship_request

    def get_one_by_id(self, id):
        data = self.db.session.execute(
            self.db.select(FriendshipRequest).
            where(FriendshipRequest.id == id)).scalar_one()

        return {
            "id": data.id,
            "sender_id": data.sender_id,
            "recipient_id": data.recipient_id,
            "status": data.status
        }

    def get_sent(self, sender_id, status: str or None):
        if status is None:
            data = self.db.session.execute(
                self.db.select(FriendshipRequest).
                where(FriendshipRequest.sender_id == sender_id)).scalars()
        else:
            data = self.db.session.execute(
                self.db.select(FriendshipRequest).
                where(FriendshipRequest.sender_id == sender_id,
                      FriendshipRequest.status == status)).scalars()

        friendship_requests = [
            {
                "id": request.id,
                "sender_id": request.sender_id,
                "recipient_id": request.recipient_id,
                "status": request.status
            }
            for request in data
        ]

        return friendship_requests

    def get_received(self, recipient_id, status: str or None):
        if status is None:
            data = self.db.session.execute(
                self.db.select(FriendshipRequest).
                where(FriendshipRequest.recipient_id == recipient_id)).scalars()
        else:
            data = self.db.session.execute(
                self.db.select(FriendshipRequest).
                where(FriendshipRequest.recipient_id == recipient_id,
                      FriendshipRequest.status == status)).scalars()

        friendship_requests = [
            {
                "id": request.id,
                "sender_id": request.sender_id,
                "recipient_id": request.recipient_id,
                "status": request.status
            }
            for request in data
        ]

        return friendship_requests

    def get_all(self, user_id, status: str or None):
        sent = self.get_sent(sender_id=user_id, status=status)
        received = self.get_received(recipient_id=user_id, status=status)


        total = []
        for request in itertools.chain(sent, received):
            total.append(request)

        return total

    def update(self, friendship_request_id: str, status):
        (self.db.session.query(FriendshipRequest).where(FriendshipRequest.id == friendship_request_id)
         .update({
            "status": status,
         })
         )
        self.db.session.commit()

    def delete(self, friendship_request_id: str):
        pass

