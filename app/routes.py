from flask import request, render_template, jsonify
from app import app
from app.dictionary_scrap import *
from app.models import EnglishWords, PolishWords
import random

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_word', methods=['POST'])
def handle_word():
    english_word = request.form.get('word')
    getTranslate(english_word)
    return 'Added'


@app.route('/get_random_word', methods=['POST'])
def get_random_word():
    words = EnglishWords.query.all()
    word = random.choice(words)
    translates = word.pol_translate
    word = word.word
    translates = [x.word for x in translates]
    return jsonify(word=word, translates=translates)

@app.route('/menagement', methods=['POST','GET'])
def user_panel():
    if request.method == 'GET':
        eng_words = [x.word for x in EnglishWords.query.all()]
        pol_words = [x.word for x in PolishWords.query.all()]
        data = {
            'english_words': eng_words,
            'polish_words': pol_words
        }
        return render_template('admin_panel.html', data=data)
    