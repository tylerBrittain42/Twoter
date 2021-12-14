import os

class Config(object):
    SECRET_KEY = 'postgresql://ohyfcvzr:AkehyaoHTqP7U0sK0L_fe9SOwurIAfSK@kashin.db.elephantsql.com/ohyfcvzr'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS='Content-Type'
