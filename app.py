from flask import Flask, render_template

app = Flask(__name__)


posts = [
    {
        'user': 'ezxjams',
        'content': 'wuss gud',
    },
    {
        'user': 'user2',
        'content': 'Happy Thanksgiving!',
    },
        {
        'user': 'RLintao',
        'content': 'Hello world!!',
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


if __name__ == '__main__':
    app.run(debug=True)