import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = b'\xd0$\xff\xb9\xfa\x97 L\xfb\xbe\xb7Y\r\xd3\xab\xeb'
DEBUG = True
BCRYPT_LOG_ROUNDS = 12

SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

GOOGLE_MAPS_KEY='AIzaSyCP5XP_S4EOFdpI8ceg3cGvzN7POyFqsOA'