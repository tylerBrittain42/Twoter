from flask import Flask, db
from datetime import datetime
# from flaskblog import db, login_manager
from flask_login import UserMixin

app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

class User(db.Model, UserMixin):
    # identity column
    id = db.Column(db.Integer, primary_key=True)
    # username column - unique so no same usernames
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # password column - 80 characters once hashed
    password = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


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

def create_tables():
    with db:
        db.create_tables([User, Relationship, Post])

if __name__ == '__main__':
    create_tables()
    app.run()