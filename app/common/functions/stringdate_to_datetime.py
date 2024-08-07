import datetime


def stringdate_to_datetime(stringdate: str) -> datetime:
    return datetime.datetime.strptime(stringdate, format('%Y-%m-%d %H:%M:%S.%f'))
