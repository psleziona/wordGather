import random, json
from app import app, db
from flask import request, render_template, jsonify, redirect, url_for, Response, session, make_response
from flask_login import login_user, current_user, login_required, logout_user
from flask.sessions import SecureCookieSessionInterface
from app.models import EnglishWords, PolishWords, Users, WordsHandler
from app.learning_system import return_object_generator, update_db, gen_stats_object
from app.utils import gen_res, db_add_word

session_cookie = SecureCookieSessionInterface()


@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    user = Users.query.filter_by(username=name).first()
    res = make_response()
    if user is not None:
        login_user(user)
    s = session_cookie.get_signing_serializer(app)
    cookie = s.dumps(dict(session))
    res.headers.add("Set-Cookie", f"session={cookie}; Secure; HttpOnly; SameSite=None; Path=/;")
    return res

@app.route('/logout')
def logout():
    logout_user()
    res = make_response()
    return res


@app.route('/register')
def register():
    return 'Work in progress'


@app.route('/word', methods = ['POST', 'GET', 'DELETE', 'PUT'])
@login_required
def word():
    if request.method == 'GET':
        word = random.choice([x.word for x in current_user.words]) # losowy obiekt EnglishWord, x - WordsHandler obiekt
        pol_meaning = [x.word for x in word.pol_translate] # lista znaczen
        word = word.word
        return {'word': word, 'meaning': pol_meaning}

    elif request.method == 'POST':
        word = request.form.get('word')
        res, code = db_add_word(word, current_user)
        return res, code

    elif request.method == 'DELETE': #calosc? danego uzytkownika -> WordsHandler tylko. Do ogarniecia
        name = request.form.get('word') # lub id? wtedy id dolaczam do response
        word = EnglishWords.query.filter_by(word=name).first()
        db.session.delete(word)
        db.session.commit()
        return 'deleted'


@app.route('/words', methods=['GET', 'POST'])
@login_required
def all_words():
    if request.method == 'GET':
        data = [return_object_generator(x.word) for x in current_user.words]
        return jsonify(data)
    elif request.method == 'POST':
        data = json.loads(request.data)
        for answer in data:
            word = list(answer)[0]
            is_right = answer[word]
            update_db(current_user, word, is_right)
        return gen_res('Success'), 200
    

@app.route('/words/<int:count>')
@login_required
def words(count):
    words = EnglishWords.query.all()
    random.shuffle(words)
    words = words[:count]
    data = [return_object_generator(x) for x in words]
    return jsonify(data)
    
@app.route('/words/progress/<float:progress>')
@login_required
def words_progress(progress):
    current_user_words = [x.word for x in current_user.words if x.progress and x.progress <= progress]
    data = [return_object_generator(x) for x in current_user_words]
    return jsonify(data)

@app.route('/words/stats')
@login_required
def words_stats():
    words = current_user.words
    data = [gen_stats_object(word.word, current_user) for word in words]
    return jsonify(data)
