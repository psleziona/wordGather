import random
from app.models import *
from app import db


def return_object_generator(eng_word_obj):
    right_answers = [x.word for x in eng_word_obj.pol_translate]
    false_answers = [x.word for x in PolishWords.query.all() if x not in eng_word_obj.pol_translate]
    false_answers = random.sample(false_answers, 3)
    return {'english_word': eng_word_obj.word, 'right_answers': right_answers, 'false_answers': false_answers}

def update_db(user, word, right):
    word_obj = EnglishWords.query.filter_by(word=word).first()
    wh_obj = WordsHandler.query.filter_by(word_id=word_obj.id, user_id=user.id).first()
    wh_obj.show_counter += 1
    if right:
        wh_obj.right_answers += 1
    wh_obj.progress_eval()
    db.session.commit()


def gen_stats_object(eng_word_obj, user):
    wh_obj = WordsHandler.query.filter_by(word_id=eng_word_obj.id, user_id=user.id).first()
    return {'word': eng_word_obj.word, 'progress': wh_obj.progress, 'counter': wh_obj.show_counter}
