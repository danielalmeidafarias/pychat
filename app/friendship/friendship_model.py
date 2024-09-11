from app.db import db

friendship_table = db.Table('friendship',
                      db.Column('user_id', db.String, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('friend_id', db.String, db.ForeignKey('user.id'), primary_key=True)
                      )
