import os
from pymongo import MongoClient

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(Config):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    db = MongoClient('mongodb://localhost:27017').DesafioPonto


class Development(Config):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    db = MongoClient('mongodb://localhost:27017').DevDesafioPonto


class Testing(Config):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'testing.sqlite')
    db = MongoClient('mongodb://localhost:27017').TestDesafioPonto


config = dict(
    development=Development(),
    testing=Testing(),
    production=Production()
)
