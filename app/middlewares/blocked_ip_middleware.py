from app.db import r
from flask import request
from functools import wraps


class BlockedIpMiddleware:
    def __init__(self):
        pass

    def blocked_ip_middleware(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ip_address = request.origin
            is_blocked = r.get(f"blocked_ip:{ip_address}")

            if is_blocked is None:
                return func(self)
            else:
                return {
                    "message": f"Ip address {ip_address} is temporary blocked"
                }, 401

        return wrapper


middleware = BlockedIpMiddleware()
