from flask import request, render_template, jsonify, redirect, url_for
from app import app, db
from app.dictionary_scrap import getTranslate
from app.models import EnglishWords, PolishWords, Users, WordsHandler
from flask_login import login_user, current_user, login_required
import random

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form.get('name')
        user = Users.query.filter_by(username=name).first()
        if user is not None:
            login_user(user)
            return redirect(url_for('index'))



@app.route('/word', methods = ['POST', 'GET', 'DELETE'])
@login_required
def word():
    current_user = Users.query.get(1)
    if request.method == 'GET':
        word = random.choice([x.word for x in current_user.words]) # losowy obiekt EnglishWord, x - WordsHandler obiekt
        pol_meaning = [x.word for x in word.pol_translate] # lista znaczen
        word = word.word
        return {'word': word, 'meaning': pol_meaning}

    elif request.method == 'POST':
        word = request.form.get('word')
        db_word = EnglishWords.query.filter_by(word=word).first()
        if db_word:
            if db_word in [x.word for x in current_user.words]:
                return 'alert: Masz to'
            else:
                db.session.add(WordsHandler(word=db_word, user=current_user))
                db.session.commit()
                return 'Added'
        else:
            if getTranslate(word):
                db.session.add(WordsHandler(word=EnglishWords.query.filter_by(word=word).first(), user=current_user))
                db.session.commit()
                return 'Added'
            else:
                return 'Somfing wrong'
    else:
        name = request.form.get('word')
        word = EnglishWords.query.filter_by(word=name).first()
        db.session.delete(word)
        db.session.commit()
        return 'deleted'

@app.route('/word/progress_filter/<float:progress>')
@login_required
def progress_filter(progress):
    current_user = Users.query.get(1)
    word = random.choice([x.word for x in current_user.words if x.progress and x.progress <= progress]) # cannot choose from empty / default progress 0 and x.progress > 0?
    return {'word': word.word, 'translates': [x.word for x in word.pol_translate]}

@app.route('/words/<int:count>')
def words(count):
    words = EnglishWords.query.all()
    random.shuffle(words)
    words = words[:count]
    data = [{'word': x.word, 'translates': [w.word for w in x.pol_translate]} for x in words]
    return jsonify(data)
    

