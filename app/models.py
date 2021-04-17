import jwt, time
from string import ascii_letters
from random import choices
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return Users.query.get(id)


word_mean = db.Table('word_translate',
                     db.Column('eng_id', db.Integer, db.ForeignKey('english_words.id')),
                     db.Column('pol_id', db.Integer, db.ForeignKey('polish_words.id')))


class EnglishWords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(20))
    pol_translate = db.relationship(
        'PolishWords', secondary=word_mean, backref='english_translate', cascade='all, delete')


class PolishWords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(20))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(200))
    email = db.Column(db.String(40))
    api_key = db.Column(db.String(20))
    auth = db.Column(db.Boolean, default=False)

    @property
    def is_authenticated(self):
        return self.auth

    def confirm_user(self):
        self.auth = True

    @staticmethod
    def gen_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def gen_api_key():
        key = ''.join(choices(ascii_letters, k=20))
        if Users.query.filter_by(api_key=key).first() == None:
            return key
        return self.gen_api_key()

    def gen_auth_token(self):
        payload = {
            'username': self.username,
            'expired': time.time() + 3600
        }
        token = jwt.encode(payload, 'jajeczko', 'HS256')
        return token


class WordsHandler(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('english_words.id'), primary_key=True)

    show_counter = db.Column(db.Integer, default=0)
    right_answers = db.Column(db.Integer, default=0)
    progress = db.Column(db.Float, default=0)

    user = db.relationship('Users', backref='words', cascade='all, delete')
    word = db.relationship('EnglishWords')


    def increment_counter(self):
        self.show_counter += 1

    def progress_eval(self):
        self.progress = self.right_answers / self.show_counter