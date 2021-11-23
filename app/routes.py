from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required, login_user
from flask_login import current_user, login_user, logout_user
from app.models import User


# DO THIS LAST
@app.route('/')
def index():
    if current_user.is_authenticated:
        return 'yes'
    return 'no'

@app.route('/login', methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.form.get('username')).first()
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
    render_template('sign-up.html')

@app.route('/sign-up', methods=['POST'])
def signup_post():
    return 'sign-up post recieved'

@app.route('/user/<user>')
def user(user):
    return f'User: {user} GET received'

@app.route('/follow', methods=['POST'])
def follow():
    return 'follow post recieved'
    
@app.route('/unfollow', methods=['POST'])
def unfollow():
    return 'UNfollow post recieved'

# feed for followers
@app.route('/feed')
def feed():
    render_template('feed.html')

@app.route('/feed/all')
def all_feed():
    return 'ALL feed req received'

@app.route('/twote/', methods=['POST'])
def twote_post():
    return 'TWOTE POST recieved'

