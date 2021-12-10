import re
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

# Reset route to create admin as well as dummy users and data
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
    for i in range(0,20):    
        bar = i%len(user_list) + 2
        new_twote = Twote(content=f'This is a test twote #{i}',u_id=bar)
        db.session.add(new_twote)
        db.session.commit()

    return 'dummy data created'



# used to test liked table functionality
@app.route('/test')
def testing():

    foo = Twote.query.first()

    print('TESTING LIKES')
    foo.like(current_user)
    db.session.commit()
    print(foo.is_liked(current_user))
    print(foo.liked_by.first())
    
    print('TESTING RETWOTES')
    print(foo.is_retwote(current_user))
    if not foo.is_retwote(current_user):
        foo.retwote(current_user)
    print(foo.is_retwote(current_user))
    db.session.commit()
    print(foo.retwote_by.first())
    # foo.undo_retwote(current_user)
    print(foo.is_retwote(current_user))

    # foo.unlike(current_user)
    # print(foo.is_liked(current_user))
    # db.session.commit()
    return '200'


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

    # content = Twote.query.filter(Twote.user.has(name=user)).order_by(desc(Twote.timestamp)).all()
    content = current_user.retwoted()
    
    return render_template('profile.html',twotes=content, c_u=current_user)

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
    foo = request.args.get('twote_id')
    if not current_user.is_authenticated:
        return redirect(url_for('login_get')) 
    data = request.form
    print(f'this is foo:{foo}:')
    cur_twote = Twote.query.filter_by(id=foo).first()
    if current_user.id != cur_twote.u_id:
        return 'error', 500
    db.session.delete(cur_twote)
    db.session.commit()
    return redirect(url_for('all_feed'))
    
@app.route('/twote', methods=['PUT'])
def twote_put():
    if not current_user.is_authenticated:
        return redirect(url_for('login_get')) 
    data = request.get_json()
    # print('data')
    # print(data)
    # print('data')
    # return {'status':200}
    cur_twote = Twote.query.filter_by(id=data.get('twote_id')).first()
    if current_user.id != cur_twote.u_id:
        return {'Does not have access', 500}
    cur_twote.content = data.get('editcontent')
    cur_twote.timestamp = datetime.now()
    db.session.commit()
    return {'success':200}




@app.route('/twote', methods=['POST'])
def twote_post():
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))

    content = request.form.get('content')
    
    # check if empty
    if content == '' or str.isspace(content):
        flash('Error empty tweet')
        return redirect(url_for('feed'))

    new_twote = Twote(content=content,u_id=current_user.id)
    db.session.add(new_twote)
    db.session.commit()

    return redirect(url_for('feed'))


# @app.route('/retwote/<twotes_id>',methods=['GET','POST'])
# @login_required
# def retwote(twotes_id):
#         retwotes = retwote(twotes_id=twote.id,id=self.id,timestamp=currentTime,content=new_twote.twote.data)
#         db.session.add(retweet)
#         db.session.commit()

@app.route('/like/<twote_id>',methods=['GET'])
def liked_twote(twote_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))
    cur_twote = Twote.query.filter_by(id=twote_id).first()
    return {'liked':cur_twote.is_liked(current_user)}


@app.route('/like/<twote_id>',methods=['POST'])
def like_twote(twote_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))
    cur_twote = Twote.query.filter_by(id=twote_id).first()
    print(cur_twote)
    if not cur_twote.is_liked(current_user):
        cur_twote.like(current_user)
        db.session.commit()
        return 'tweet liked'
    else:
        return 'already liked'    

@app.route('/unlike/<twote_id>',methods=['POST'])
def unlike_twote(twote_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))
    cur_twote = Twote.query.filter_by(id=twote_id).first()
    print(cur_twote)
    if cur_twote.is_liked(current_user):
        cur_twote.unlike(current_user)
        db.session.commit()
        return 'tweet unliked'
    else:
        return 'tweet already not liked'   


# ######################
@app.route('/retwote/<twote_id>',methods=['GET'])
def retwoted_twote(twote_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))
    cur_twote = Twote.query.filter_by(id=twote_id).first()
    return {'retwoted':cur_twote.is_retwote(current_user)}


@app.route('/retwote/<twote_id>',methods=['POST'])
def retwote_twote(twote_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))
    cur_twote = Twote.query.filter_by(id=twote_id).first()
    if not cur_twote.is_retwote(current_user):
        cur_twote.retwote(current_user)
        db.session.commit()
        return 'tweet retwoted'
    else:
        return 'already retwoted'    

@app.route('/unretwote/<twote_id>',methods=['POST'])
def unretwote_twote(twote_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login_get'))
    cur_twote = Twote.query.filter_by(id=twote_id).first()
    print(cur_twote)
    if cur_twote.is_retwote(current_user):
        cur_twote.undo_retwote(current_user)
        db.session.commit()
        return 'tweet unRETWOTES'
    else:
        return 'tweet already not retwoted'  


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