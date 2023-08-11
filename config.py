import os
from decouple import config
from datetime import timedelta


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = config('SECRET_KEY', default='')
    UPLOAD_FOLDER = config('UPLOAD_FOLDER', default='')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    default_user_credo = {
        'username': config('DEFAULT_USERNAME', default='admin'),
        'password': config('DEFAULT_PASS', default='adminadmin')
    }

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_ACCESS_LIFESPAN = timedelta(days=1)
    JWT_REFRESH_LIFESPAN = timedelta(days=2)


class ProductionConfig(Config):

    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default=''),
        config('DB_USERNAME', default=''),
        config('DB_PASS', default=''),
        config('DB_HOST', default=''),
        config('DB_PORT', default=''),
        config('DB_NAME', default='')
    )
