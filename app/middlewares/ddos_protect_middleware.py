from app.db import r
from flask import request
from functools import wraps
from ..common.functions.stringdate_to_datetime import stringdate_to_datetime
from ..common.functions.datetime_to_string import datetime_to_string
from datetime import datetime, timedelta


class DDOSProtectMiddleware:
    def __init__(self):
        pass

    def middleware(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ip_address = request.remote_addr
            user_requests_record = r.hgetall(f"ip_address:{ip_address}")

            if len(user_requests_record) == 0:
                r.hset(f"ip_address:{ip_address}", mapping={
                    'requests': 1,
                    'first_request': datetime_to_string(datetime.now()),
                    'last_request': datetime_to_string(datetime.now()),
                })
                r.expireat(f"ip_address:{ip_address}", datetime.now() + timedelta(minutes=1))

                return func(self)

            else:
                first_request = user_requests_record['first_request']
                requests = user_requests_record['requests']

                time_since_first_request = (datetime.now() - stringdate_to_datetime(first_request))
                seconds_since_first_request = round(time_since_first_request.seconds + time_since_first_request.microseconds * (10 ** -6), 2)

                r.hset(f"ip_address:{ip_address}", mapping={
                    'requests': int(requests) + 1,
                    'first_request': first_request,
                    'last_request': datetime_to_string(datetime.now()),
                })
                r.expireat(f"ip_address:{ip_address}", datetime.now() + timedelta(minutes=1))

                requests_per_second = (int(requests) + 1) / seconds_since_first_request

                if requests_per_second > 1 and int(requests) + 1 >= 30:
                    r.set(f"blocked_ip:{ip_address}", 1)
                    r.expireat(f"blocked_ip:{ip_address}", datetime.now() + timedelta(days=1))
                    return {
                        "message": "Too many requests"
                    }
                elif requests_per_second > 1 and int(requests) + 1 >= 10:
                    return {
                        "message": "Too many requests"
                    }, 429
                else:
                    return func(self)

        return wrapper


ddos_protect_middleware = DDOSProtectMiddleware().middleware
