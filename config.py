import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sewrjwao5rhiawllsdfkjlksenf,smdnvf,xzmcvn,zxcmvnsdfg'
    SQLALCHEMY_DATABASE_URI = 'postgresql://ohyfcvzr:AkehyaoHTqP7U0sK0L_fe9SOwurIAfSK@kashin.db.elephantsql.com/ohyfcvzr'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
