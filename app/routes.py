from sqlalchemy.engine import url
from sqlalchemy.orm import session
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required, login_user
from flask_login import current_user, login_user, logout_user
from app.models import User, Twote
from sqlalchemy import desc, asc
from datetime import date, datetime
from flask_admin import Admin, BaseView, expose
from flask_admin.base import AdminIndexView
from flask_admin.contrib.sqla import ModelView

# DELETE ME
@app.route('/c')
def new_admin():


    db.session.query(User).delete()
    db.session.query(Twote).delete()
    db.session.commit()
    
    new_user = User(name='admin', password='pw', role='admin')
    new_user.set_password('pw')
    db.session.add(new_user)
    db.session.commit()


    user_list = [
        ['user1','pw'],
        ['user2','pw'],
        ['user3','pw'],
        ['user4','pw'],
        ['user5','pw'],
    ]
    
    for cur_u in user_list:
        new_user = User(name=cur_u[0], password=cur_u[1])
        new_user.set_password(cur_u[1])
        db.session.add(new_user)
        db.session.commit()

    bar = 0
    for i in range(0,10):    
        if bar > 3:
            bar = 1
        else:
            bar += 1
        new_twote = Twote(content=f'This is a test twote #{i}',u_id=bar)
        db.session.add(new_twote)
        db.session.commit()

    return 'dummy data created'




@app.route('/test')
def testing():

    foo = Twote.query.first()
    foo.like(current_user)
    db.session.commit()
    print(foo.is_liked(current_user))
    print(foo.liked_by.first())
    foo.unlike(current_user)
    print(foo.is_liked(current_user))
    db.session.commit()
    return '200'


# DO THIS LAST
@app.route('/')
def index():
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect('/admin')
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    return redirect(url_for('login_get'))

@app.route('/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(name=request.form.get('username')).first()
    if user is None or not user.check_password(request.form.get('password')):
        return redirect(url_for('login_get'))
    login_user(user)

    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_get'))

@app.route('/sign-up', methods=['GET'])
def signup_get():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('sign-up.html')

@app.route('/sign-up', methods=['POST'])
def signup_post():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    data = request.form

    #check if user already exists
    if User.query.filter_by(name=data.get('username')).first() is not None:
        flash('Username already taken')
        return redirect(url_for('signup_get'))

    # create new user
    # new_user = User(name=data.get('username'), email=data.get('email'))
    new_user = User(name=data.get('username'), password=data.get('password'))
    new_user.set_password(data.get('password'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login_get'))


@app.route('/user/<user>')
def user(user):
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))    
    
    if User.query.filter_by(name=user).first() is None:
        flash('USER DOES NOT EXIST')
        return redirect(url_for('feed'))

    content = Twote.query.filter(Twote.user.has(name=user)).order_by(desc(Twote.timestamp)).all()

    return render_template('profile.html',twotes=content)

@app.route('/follow/<user>', methods=['POST'])
def follow(user):
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))
    user_to_follow = User.query.filter_by(name=user).first()
    if user_to_follow is None:
        return 'User not found', 500
    elif user == current_user.name:
        return 'Cannot follow yourself', 500
    else: 
        current_user.follow(user_to_follow)
        db.session.commit()
        return 'follow post recieved'
    
@app.route('/unfollow/<user>', methods=['POST'])
def unfollow(user):
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))
    user_to_unfollow = User.query.filter_by(name=user).first()
    if user_to_unfollow is None:
        return 'User not found', 500
    elif user == current_user.name:
        return 'Cannot unfollow yourself', 500
    else: 
        current_user.unfollow(user_to_unfollow)
        db.session.commit()
        return 'unfollow post recieved'


'''IMPORTANT'''
# We need to replicate the following query 
# SELECT DISTINCT *
# FROM Twote
# INNER JOIN followers on followed_id=twote.u_id  
# WHERE follower_id=2

# feed for followers(including a user's own posts)
@app.route('/feed')
def feed():

    if not current_user.is_authenticated:
        return redirect(url_for('login_get')) 

    content = []
    
    followed_users = current_user.followed.all()
    print(followed_users)

    content = Twote.query.order_by(desc(Twote.timestamp)).filter(Twote.u_id.in_(current_user.followed_ids())).all()

    return render_template('feed.html',twotes=content, c_u=current_user)

@app.route('/feed/all')
def all_feed():

    if not current_user.is_authenticated:
        return redirect(url_for('login_get')) 

    content = Twote.query.order_by(desc(Twote.timestamp)).all()
    return render_template('feed.html', twotes=content, c_u=current_user)

# REMOVE ME
# soletely used to test twote post route
@app.route('/twote')
def twote_get():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('compose.html')

@app.route('/twote', methods=['DELETE'])
def twote_delete():
    if not current_user.is_authenticated:
        return redirect(url_for('login_get')) 
    data = request.form
    cur_twote = Twote.query.filter_by(id=data.get('twote_id')).first()
    if current_user.id != cur_twote.u_id:
        return 'error', 500
    db.session.delete(cur_twote)
    db.session.commit()
    return redirect(url_for('feed'))
    
@app.route('/twote', methods=['PUT'])
def twote_put():
    if not current_user.is_authenticated:
        return redirect(url_for('login_get')) 
    data = request.form
    cur_twote = Twote.query.filter_by(id=data.get('twote_id')).first()
    if current_user.id != cur_twote.u_id:
        return 'error', 500
    cur_twote.content = data.get('content')
    cur_twote.timestamp = datetime.now()
    db.session.commit()
    return redirect(url_for('feed'))



@app.route('/twote', methods=['POST'])
def twote_post():
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))

    content = request.form.get('content')
    
    # check if empty
    if content == '' or str.isspace(content):
        flash('Error empty tweet')
        return redirect(url_for('twote_get'))

    new_twote = Twote(content=content,u_id=current_user.id)
    db.session.add(new_twote)
    db.session.commit()

    return 'TWOTE POST recieved'


class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        # return self.render('admin_index.html')
        if current_user.is_authenticated and current_user.role == 'admin':
            return self.render('admin_index.html')
        else:
            return redirect(url_for('login_get'))

admin = Admin(app, name='asdasdsad', template_mode='bootstrap3', index_view=HomeView())

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(SecureModelView(User, db.session))
admin.add_view(SecureModelView(Twote, db.session))
# admin.add_view(SecureModelView(Teacher, db.session))
# admin.add_view(SecureModelView(User, db.session))
# admin.add_view(SecureModelView(Enrollment,db.session))