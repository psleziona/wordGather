import json
from flask import Response
from flask_login import current_user
from app import db
from app.models import EnglishWords, Users, WordsHandler
from app.dictionary_scrap import getTranslate

def gen_res(msg=None):
    res = Response()
    res.headers.add('Access-Control-Allow-Origin', '*')
    if msg:
        res.data = json.dumps({'msg': msg})
    return res

def db_add_word(word, user):
    db_word = EnglishWords.query.filter_by(word=word).first()
    if db_word:
        if db_word in [x.word for x in current_user.words]:
            return gen_res('Word in db'), 200
        else:
            db.session.add(WordsHandler(word=db_word, user=current_user))
            db.session.commit()
            return gen_res(), 201
    else:
        if getTranslate(word):
            db.session.add(WordsHandler(word=EnglishWords.query.filter_by(word=word).first(), user=current_user))
            db.session.commit()
            return gen_res(), 201
        else:
            return gen_res('Error'), 500