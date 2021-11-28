from flask import Flask, render_template

app = Flask(__name__)


posts = [
    {
        'user': 'ezxjams',
        'content': 'wuss gud',
        'status': 'followed'
    },
    {
        'user': 'user2',
        'content': 'Happy Thanksgiving!',
        'status': 'unfollowed'
    },
        {
        'user': 'RLintao',
        'content': 'Hello world!!',
        'status': 'unfollowed'
    },
    {
        'user': 'Tyler',
        'content': 'Hows it goin chief',
        'status': 'unfollowed'
    },
    {
        'user': 'ivanjeser',
        'content': 'The FitnessGram™ Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test',
        'status': 'unfollowed'
    }
]

@app.route('/')
def index():
    return "<h1> Index </h1>"

@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)