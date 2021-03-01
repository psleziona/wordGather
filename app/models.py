from app import db


word_mean = db.Table('word_translate',
    db.Column('eng_id', db.Integer, db.ForeignKey('english_words.id')),
    db.Column('pol_id', db.Integer, db.ForeignKey('polish_words.id'))
)

class EnglishWords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(20))
    pol_translate = db.relationship('PolishWords', secondary=word_mean, backref='polish_translation')
    


class PolishWords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(20))
    eng_translate = db.relationship('EnglishWords', secondary=word_mean, backref='english_translation')
