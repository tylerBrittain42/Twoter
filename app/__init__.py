from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate, migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login_get'

def getApp():
    return app



from app import routes, models

