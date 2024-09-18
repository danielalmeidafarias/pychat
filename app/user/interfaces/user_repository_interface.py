from abc import ABC, abstractmethod
from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from ..user_model import User


class UserResponse(User):
    def __init__(self, user_id: str, name: str, email: str, friends, sent_requests, received_requests, chats):
        super().__init__(user_id, name, email)
        self.friends = friends
        self.sent_requests = sent_requests
        self.received_requests = received_requests
        self.chats = chats


class UserRepositoryInterface(ABC):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    @abstractmethod
    def create(self, user_id: str, email: str, password: bytes, name: str) -> UserResponse:
        pass

    @abstractmethod
    def get_one(self, user_id: str) -> UserResponse:
        pass

    @abstractmethod
    def get_one_by_email(self, email) -> UserResponse:
        pass

    @abstractmethod
    def get_all(self) -> List[UserResponse]:
        pass

    @abstractmethod
    def update(self, user_id: str, data):
        pass

    @abstractmethod
    def delete(self, user_id: str):
        pass

    @abstractmethod
    def search(self, user_id: str, name: str) -> List[UserResponse]:
        pass