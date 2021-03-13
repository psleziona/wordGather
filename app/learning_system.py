import random
from app.models import *

def test_answer_generator(eng_word_obj):
    right_answer = random.choice([x.word for x in eng_word_obj.pol_translate])
    words_for_false = [x.word for x in PolishWords.query.all() if x not in eng_word_obj.pol_translate]
    false_answers = random.sample(words_for_false, 3)
    return {'right': right_answer, 'false': false_answers}