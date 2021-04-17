import json
from flask import make_response, url_for
from flask_mail import Message
from app import db, mail
from app.models import EnglishWords, Users, WordsHandler
from app.dictionary_scrap import getTranslate


def db_add_word(word, user):
    db_word = EnglishWords.query.filter_by(word=word).first()
    res = make_response()
    if db_word:
        if db_word in [x.word for x in user.words]:
            return res, 200
        else:
            db.session.add(WordsHandler(word=db_word, user=user))
            db.session.commit()
            return res, 201
    else:
        if getTranslate(word):
            db.session.add(WordsHandler(word=EnglishWords.query.filter_by(word=word).first(), user=user))
            db.session.commit()
            return res, 201
        else:
            return res, 500


def send_auth_msg(token, user_mail):
    url = url_for('auth', token=token)
    url = 'https://' + app.config['SERVER_NAME'] + url
    msg = Message(
        subject='User confirm message',
        body=f'Here is your activate url if href doesn\'t work copy and past in browser url field {url}',
        html=f'<p>To confirm click</p><a href={url}>Confirm link</a>',
        recipients=[user_mail],
        sender='admin@example.com'
    )
    mail.send(msg)