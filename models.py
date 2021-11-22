from flask import Flask, render_template_string, redirect
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, logout_user, FlaskLoginClient
# from flaskblog import db, login_manager
from flask_blogging import db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# login = LoginManager(app)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# @LoginManager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # password column - 80 characters once hashed
    password = db.Column(db.String(80), nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

# def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.profile_image}')"

def following(self):
        return (User
                .select()
                .join(Relationship, on=Relationship.to_user)
                .where(Relationship.from_user == self)
                .order_by(User.username))

def followers(self):
        return (User
                .select()
                .join(Relationship, on=Relationship.from_user)
                .where(Relationship.to_user == self)
                .order_by(User.username))

def is_following(self, user):
        return (Relationship
                .select()
                .where(
                    (Relationship.from_user == self) &
                    (Relationship.to_user == user))
                .exists())

class Relationship(db.Model):
    from_user = db.ForeignKeyField(User, backref='relationships')
    to_user = db.ForeignKeyField(User, backref='related_to')

    class Meta:
        indexes = ((('from_user', 'to_user'), True),)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(145), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Message(db.Model):
    user = db.ForeignKeyField(User, backref='messages')
    content = db.TextField()
    pub_date = db.DateTimeField()

# def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"

def create_tables():
    with db:
        db.create_tables([User, Relationship, Post, Message])

if __name__ == '__main__':
    create_tables()
    app.run()