from datetime import datetime


def datetime_to_string(date: datetime) -> str:
    return date.strftime(format='%Y-%m-%d %H:%M:%S.%f')
    