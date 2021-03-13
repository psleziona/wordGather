from app import db, login
from flask_login import UserMixin

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
        'PolishWords', secondary=word_mean, backref='english_translate')


class PolishWords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(20))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))


class WordsHandler(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('english_words.id'), primary_key=True)

    show_counter = db.Column(db.Integer, default=0)
    right_answers = db.Column(db.Integer, default=0)
    progress = db.Column(db.Float)  # right guess / counter

    user = db.relationship('Users', backref='words', cascade='all, delete')
    word = db.relationship('EnglishWords', cascade='all, delete')


    def increment_counter(self):
        self.show_counter += 1

    def progress_eval(self):
        self.progress = self.right_answers / self.show_counter



