import random
from app.models import *
from app import db

def test_answer_generator(eng_word_obj):
    right_answer = random.choice([x.word for x in eng_word_obj.pol_translate])
    words_for_false = [x.word for x in PolishWords.query.all() if x not in eng_word_obj.pol_translate]
    false_answers = random.sample(words_for_false, 3)
    return {'right': right_answer, 'false': false_answers}


def return_object_generator(eng_word_obj):
    right_answers = [x.word for x in eng_word_obj.pol_translate]
    false_answers = [x.word for x in PolishWords.query.all() if x not in eng_word_obj.pol_translate]
    false_answers = random.sample(false_answers, 3)
    return {'english_word': eng_word_obj.word, 'right_answers': right_answers, 'false_answers': false_answers}

def update_db(user, word, right):
    word_obj = EnglishWords.query.filter_by(word=word).first()
    wo_obj = WordsHandler.query.filter_by(word_id=word_obj.id, user_id=user.id).first()
    wo_obj.show_counter += 1
    if right:
        wo_obj.right_answers += 1
    wo_obj.progress_eval()
    db.session.commit()