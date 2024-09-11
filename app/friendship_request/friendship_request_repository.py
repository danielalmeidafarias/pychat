import itertools
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from .friendship_request_model import FriendshipRequest
from uuid import uuid4 as uuid
from .friendship_request_service import FriendshipRequestRepositoryInterface


class FriendshipRequestRepository(FriendshipRequestRepositoryInterface):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, sender_id: str, receiver_id: str):
        friendship_request = FriendshipRequest(
            id=str(uuid()),
            sender_id=sender_id,
            receiver_id=receiver_id
        )

        self.db.session.add(friendship_request)
        self.db.session.commit()

        return friendship_request

    def get_one(self, sender_id: str, receiver_id: str):
        friendship_request = (self.db.session.query(FriendshipRequest)
                              .where(and_(FriendshipRequest.sender_id == sender_id,
                                          FriendshipRequest.receiver_id == receiver_id)).one_or_none())

        return friendship_request

    def get_one_by_id(self, id):
        data = self.db.session.execute(
            self.db.select(FriendshipRequest).where(FriendshipRequest.id == id)).scalar_one()

        return {
            "id": data.id,
            "sender_id": data.sender_id,
            "receiver_id": data.receiver_id,
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
                "sender": request.sender,
                "receiver": request.receiver
            }
            for request in data
        ]

        return friendship_requests

    def get_received(self, receiver_id, status: str or None):
        if status is None:
            data = self.db.session.execute(
                self.db.select(FriendshipRequest).
                where(FriendshipRequest.receiver_id == receiver_id)).scalars()
        else:
            data = self.db.session.execute(
                self.db.select(FriendshipRequest).
                where(FriendshipRequest.receiver_id == receiver_id,
                      FriendshipRequest.status == status)).scalars()

        friendship_requests = [
            {
                "id": request.id,
                "sender": request.sender,
                "receiver": request.receiver
            }
            for request in data
        ]

        return friendship_requests

    def get_all(self, user_id, status: str or None):
        sent = self.get_sent(sender_id=user_id, status=status)
        received = self.get_received(receiver_id=user_id, status=status)


        total = []
        for request in itertools.chain(sent, received):
            total.append(request)

        return total

    def update(self, friendship_request_id: str, status: str):
        (self.db.session.query(FriendshipRequest).where(FriendshipRequest.id == friendship_request_id)
         .update({
            "status": status,
         })
         )
        self.db.session.commit()

    def delete(self, friendship_request_id: str):
        self.db.session.query(FriendshipRequest).where(FriendshipRequest.id == friendship_request_id).delete()
        self.db.session.commit()
