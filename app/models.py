
from app import db, login
from datetime import datetime
from flask_login import UserMixin
import hashlib
from werkzeug.security import generate_password_hash,check_password_hash

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(100))
    profile_image = db.Column(db.String(200), nullable=False, default='default.jpg')
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
    
    def __repr__(self):
        return '<User {}>'.format(self.name)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def set_password(self, password):
        self.password_hash == generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def followed_ids(self):
        id_list = [self.id]
        for user in self.followed.all():
            id_list.append(user.id)
        return id_list

    def followed_twotes(self):
        followed = Twote.query.join(
            followers, (followers.c.followed_id == Twote.u_id)).filter(
                followers.c.follower_id == self.id)
        own = Twote.query.filter_by(u_id=self.id)
        return followed.union(own).order_by(Twote.timestamp.desc())



class Twote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(145), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    like_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Twote {}>'.format(self.content)

# class Message(db.Model):
#     user = db.ForeignKeyField(User, backref='messages')
#     content = db.TextField()
#     pub_date = db.DateTimeField()

    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.content}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))