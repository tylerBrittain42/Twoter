import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sewrjwao5rhiawllsdfkjlksenf,smdnvf,xzmcvn,zxcmvnsdfg'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///twoter.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS='Content-Type'
