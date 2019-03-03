import os
import random, string
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'db.db')+'?check_same_thread=False'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')