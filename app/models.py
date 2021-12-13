
from sqlalchemy.orm import backref, relation, relationship
from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

liked = db.Table('liked',
    db.Column('twotes_id', db.Integer, db.ForeignKey('twote.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

retwot = db.Table('retwote',
    db.Column('twotes_id', db.Integer, db.ForeignKey('twote.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(120), index=True, default='None')
    password = db.Column(db.String(100))
    profile_image = db.Column(db.String(200), nullable=False, default='default.jpg')
    authenticated = db.Column(db.Boolean, default=False)

    twotes = db.relationship('Twote', backref='user', lazy='dynamic')

    # assorted follower stuff
    followed = db.relationship(
        'User', secondary=followers, 
        primaryjoin=(followers.c.follower_id == id), 
        secondaryjoin=(followers.c.followed_id == id),
        backref = db.backref('followers',lazy='dynamic'), lazy='dynamic')
    role = db.Column(db.String(100), default='user')
    authenticated = db.Column(db.Boolean, default=False)


    liked_twotes = relationship('Twote', secondary=liked, backref=db.backref('liked_by', lazy='dynamic'))
    retwotes = relationship('Twote', secondary=retwot, backref=db.backref('retwote_by', lazy='dynamic'))

    
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

    def set_password(self, new_password):
        self.password = generate_password_hash(new_password)
        
    def check_password(self, new_password):
        return check_password_hash(self.password, new_password)
    
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

    def retwoted(self):
        retwoted = Twote.query.join(
            retwot, (retwot.c.twotes_id== Twote.id)
        )
        own = Twote.query.filter_by(u_id=self.id)
        return retwoted.union(own).order_by(Twote.timestamp.desc()).all()




        return twotes

class Twote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(145), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    retwote_count = db.Column(db.Integer, nullable=False, default=0)


    def is_liked(self, user):
        return self.liked_by.filter(
            (liked.c.user_id == user.id)).count() > 0
        

    def like(self,user):
        if not self.is_liked(user):
            self.liked_by.append(user)
            self.like_count += 1

    def unlike(self,user):
        if self.is_liked(user):
            self.liked_by.remove(user)
            self.like_count -= 1

    def is_retwote(self, user):
        return self.retwote_by.filter(
            (retwot.c.user_id == user.id)).count() > 0

    def retwote(self, user):
        if not self.is_retwote(user):
            self.retwote_by.append(user)
            self.retwote_count += 1

    def undo_retwote(self, user):
        if self.is_retwote(user):
            self.retwote_by.remove(user)
            self.retwote_count -= 1   



    # liked_twotes = relationship('User', secondary=liked, backref=db.backref('user'))

    # likes = db.relationship(
    #     'User', secondary=liked,
    #     primaryjoin =(liked.c.twotes_id == id),
    #     secondaryjoin=liked,
    #     backref = db.backref('users', lazy='dynamic'), lazy='dynamic')

    # retwotes = db.relationship(
    #     'User', secondary=retwote,
    #     primaryjoin =(retwote.c.twotes_id == id),
    #     secondaryjoin=liked,
    #     backref = db.backref('users', lazy='dynamic'), lazy='dynamic')

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