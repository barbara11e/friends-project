import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
BCRYPT_LOG_ROUNDS = 12

SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
