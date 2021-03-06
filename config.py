import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
                              'sqlite:///dataBase\\defDataBase.db'


class TestingConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
    #                           'sqlite:///dataBase\\defDataBase.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
                              'sqlite:///dataBase\\defDataBase.db'


class ProductionConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
                              rf'sqlite:///dataBase\\defDataBase.db'
