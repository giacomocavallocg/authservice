import os
import datetime
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'..','db/cookingauthdb.db')
    JWT_SECRET_KEY = "super-secret"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1) 

class ProductionConfig(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQL_DATABASE_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1) 

class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = "super-secret"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1) 

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestConfig,
    prod=ProductionConfig
)
