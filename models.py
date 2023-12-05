from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(32))
    email = db.Column(db.String(120), index=True, unique=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(120))
    location = db.Column(db.String(120))
    date = db.Column(db.String(120))
    time = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id2 = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer)

class EventFriend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))

