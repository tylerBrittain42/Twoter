from app import app
from flask import render_template, flash, redirect, url_for

# DO THIS LAST
@app.route('/')
def index():
    return "<h1> Index </h1>"

@app.route('/login', methods=['GET'])
def login_get():
    render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    return 'login post recieved'

@app.route('/logout')
def logout():
    return 'logout req recieved'

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

