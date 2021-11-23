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
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # password column - 80 characters once hashed
    password = db.Column(db.String(80), nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def __init__(self, username, email, password, profile_image, posts):
        self.username = username
        self.email = email
        self.password = password
        self.profile_image = profile_image
        self.posts = posts

    # def __repr__(self):
    #         return f"User('{self.username}', '{self.email}', '{self.profile_image}', '{self.posts}')"

    
    def getUsers():
        users = User.query.all()
        return [{"id": i.id, "username": i.username, "email": i.email, "password": i.password} for i in users]


    def getUser(user_id):
        users = User.query.all()
        user = list(filter(lambda x: x.id == user_id, users))[0]
        return {"id": user.id, "username": user.username, "email": user.email, "password": user.password}


    def addUser(username, email, password):
        try:
            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False


    def removeUser(user_id):
        try:
            user = User.query.get(user_id)
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
        return False

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

    def getPosts():
            posts = Post.query.all()
            return [{"id": i.id, "content": i.content, "user": getUser(i.user_id)} for i in posts]

    def getUserPosts(user_id):
        posts = Post.query.all()
        return [{"id": item.id, "userid": item.uid, "content": item.content} for item in
                filter(lambda i: i.uid == user_id, posts)]



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(145), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    like_count = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', foreing_keys=user_id)

    def addPost(title, content, user_id):
        try:
            user = list(filter(lambda i: i.id == user_id, User.query.all()))[0]
            post = Post(title=title, content=content, user=user)
            db.session.add(post)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delPost(pid):
        try:
            post = Post.query.get(pid)
            db.session.delete(post)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False



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