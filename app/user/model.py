from app.db import db

friendship = db.Table('friendship',
                      db.Column('user_id', db.String, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('friend_id', db.String, db.ForeignKey('user.id'), primary_key=True)
                      )

chat_members = db.Table('chat_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'), primary_key=True)
)

class User(db.Model):
    def __init__(self, user_id: str, name: str, email: str, password: bytes):
        self.id = user_id
        self.name = name
        self.email = email
        self.password = password

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(128), nullable=False)

    friends = db.relationship('User', secondary=friendship,
                              primaryjoin=id==friendship.c.user_id,
                              secondaryjoin=id==friendship.c.friend_id,
                              backref=db.backref('friend_of', lazy='dynamic'))

    sent_requests = db.relationship('FriendshipRequest', backref='sender', lazy=True, foreign_keys='FriendshipRequest.sender_id')
    received_requests = db.relationship('FriendshipRequest', backref='receiver', lazy=True, foreign_keys='FriendshipRequest.receiver_id')

    chats = db.relationship('Chat', primaryjoin=id==chat_members.c.user_id, secondaryjoin=id==chat_members.c.chat_id,
                            backref=db.backref('chat_of'),secondary=chat_members)

    messages = db.relationship('Message', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f"{{id:{self.id}, \
        name:{self.name}, \
        email: {self.email}, \
        password: {self.password}, \
        friends:{self.friends}}}"
