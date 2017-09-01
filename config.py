# coding:utf-8

class DevConfig(object):
    debug = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "mysql://db_user:db_passwd@ip_address/db_name"

class ProdConfig(object):
    pass

class Config(object):
    pass