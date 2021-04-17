import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'vpszdjecia.online'
    MAIL_PORT = 25
    MAIL_USERNAME = 'gocio@vpszdjecia.online'
    MAIL_PASSWORD = 'gocio12345'
    SERVER_NAME = 'word-gather.herokuapp.com'