from abc import ABC, abstractmethod
from flask import Request, Response


class UserServiceInterface(ABC):
    @abstractmethod
    def get_user(self, request: Request) -> Response:
        pass

    @abstractmethod
    def create_user(self, request: Request) -> Response:
        pass

    @abstractmethod
    def user_profile(self, request: Request) -> Response:
        pass
