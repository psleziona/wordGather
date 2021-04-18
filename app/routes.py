import random
import json
import jwt
import datetime
from app import app, db
from flask import request, jsonify, url_for, make_response, redirect, session
from flask_login import login_user, current_user, login_required, logout_user
from flask.sessions import SecureCookieSessionInterface
from flask_cors import cross_origin
from app.models import EnglishWords, PolishWords, Users, WordsHandler
from app.learning_system import return_object_generator, update_db, gen_stats_object
from app.utils import db_add_word, send_auth_msg

session_cookie = SecureCookieSessionInterface()


@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    user = Users.query.filter_by(username=name).first()
    res = make_response()
    if user is not None and user.check_password(password):
        login_user(user)
        s = session_cookie.get_signing_serializer(app)
        cookie = s.dumps(dict(session))
        res.headers.add(
            "Set-Cookie", f"session={cookie}; Secure; HttpOnly; SameSite=None; Path=/;")
        return res, 200
    return res, 404


@app.route('/logout')
def logout():
    logout_user()
    res = make_response()
    return res


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('e-mail')
    password = request.form.get('password')
    if Users.query.filter_by(username=username).first() != None \
            or Users.query.filter_by(email=email).first() != None:
        return 'already in', 409
    password_hash = Users.gen_password(password)
    api_key = Users.gen_api_key()
    user = Users(username=username, password_hash=password_hash,
                 email=email, api_key=api_key)
    auth_token = user.gen_auth_token()
    if send_auth_msg(auth_token, email):
        db.session.add(user)
        db.session.commit()
        return 'git', 200
    return 'niegit', 500


@app.route('/auth/<token>')
def auth(token):
    try:
        data = jwt.decode(token, 'jajeczko', 'HS256')
        user = data['username']
        timestamp = data['expired']
        current_time = datetime.datetime.now()
        if datetime.datetime.fromtimestamp(timestamp) > current_time:
            user = Users.query.filter_by(username=user).first()
            user.confirm_user()
            db.session.commit()
            return redirect('https://psleziona.github.io/login')
        else:
            # link wygasl, wygerenruj nowy
            return 'niegit', 404
    except:
        return redirect('https://psleziona.github.io/404')


@app.route('/word', methods=['DELETE'])
@login_required
def word():
    word = request.form.get('word')
    word = EnglishWords.query.filter_by(word=word).first()
    wh_obj = WordsHandler.query.filter_by(
        word_id=word.id, user_id=current_user.id).first()
    db.session.delete(wh_obj)
    db.session.commit()
    return 'deleted'


@app.route('/<string:api_key>/word', methods=['POST'])
@cross_origin(origins='*')
def add_word(api_key):
    word = request.form.get('word')
    user = Users.query.filter_by(api_key=api_key).first()
    res, code = db_add_word(word, user)
    return res, code


@app.route('/words', methods=['GET', 'POST'])
@login_required
def all_words():
    if request.method == 'GET':
        data = [{'word': x.word.word, 'meanings': [y.word for y in x.word.pol_translate]} for x in current_user.words]
        return jsonify(data)
    elif request.method == 'POST':
        res = make_response()
        data = json.loads(request.data)
        for answer in data:
            word = list(answer)[0]
            is_right = answer[word]
            update_db(current_user, word, is_right)
        return res


@app.route('/test-words/<int:count>')
@login_required
def words(count):
    words = [x.word for x in current_user.words]
    random.shuffle(words)
    words = words[:count]
    data = [return_object_generator(x) for x in words]
    return jsonify(data)


@app.route('/words/progress/<float:progress>')
@login_required
def words_progress(progress):
    current_user_words = [
        x.word for x in current_user.words if x.progress and x.progress <= progress]
    data = [return_object_generator(x) for x in current_user_words]
    return jsonify(data)


@app.route('/user')
@login_required
def user_page():
    words = current_user.words
    stats = [gen_stats_object(word.word, current_user) for word in words]
    api = current_user.api_key
    username = current_user.username
    data = {'stats': stats, 'username': username, 'api-key': api}
    return data
