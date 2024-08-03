from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import redis


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

r = redis.Redis(decode_responses=True)
