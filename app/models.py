from enum import unique
from app import db
from app.routes import index
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(100))

    twotes = db.relationship('Twote',backref='user', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'


class Twote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(145), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.content}'