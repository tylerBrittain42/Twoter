
from app import db, login
from datetime import datetime
from flask_login import UserMixin

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)
    
    twotes = db.relationship('Twote',backref='user', lazy='dynamic')

    # assorted follower stuff
    followed = db.relationship(
        'User', secondary=followers, 
        primaryjoin=(followers.c.follower_id == id), 
        secondaryjoin=(followers.c.followed_id == id),
        backref = db.backref('followers',lazy='dynamic'), lazy='dynamic')
    role = db.Column(db.String(100), default='user')
    authenticated = db.Column(db.Boolean, default=False)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # assorted password stuff
    def check_password(self, password):
        return self.password == password
    

    def __repr__(self):
        return f'{self.name}'


class Twote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(145), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.content}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))