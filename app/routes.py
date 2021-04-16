import random, json, jwt, datetime
from app import app, db
from flask import request, jsonify, url_for, make_response, redirect
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


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('e-mail')
    password = request.form.get('password')
    if Users.query.filter_by(username=username).first() != None \
        or Users.query.filter_by(email=email).first() !=None:
        return 'already in', 409
    password_hash = Users.gen_password(password)
    api_key = Users.gen_api_key()
    user = Users(username=username, password_hash=password_hash, email=email, api_key=api_key)
    db.session.add(user)
    db.session.commit()
    send_auth_msg(auth_token, email)
    return 'git', 200

@app.route('/auth/<token>')
def auth(token):
    try:
        data = jwt.decode(token, 'jajeczko', 'HS256')
        user = data['username']
        timestamp = data['expired']
        current_time = datetime.datetime.now()
        if datetime.datetime.fromtimestamp(timestamp) < current_time:
            user = Users.query.filter_by(username=user).first()
            user.confirm_user()
            db.session.commit()
            return redirect('https://psleziona.github.io/login')
        else:
            #link wygasl, wygerenruj nowy
            return 'niegit', 404
    except:
        return redirect('https://psleziona.github.io/404')


@app.route('/word', methods = ['GET', 'DELETE'])
@login_required
def word():
    if request.method == 'GET':
        word = random.choice([x.word for x in current_user.words]) # losowy obiekt EnglishWord, x - WordsHandler obiekt
        pol_meaning = [x.word for x in word.pol_translate] # lista znaczen
        word = word.word
        return {'word': word, 'meaning': pol_meaning}
    elif request.method == 'DELETE': 
        name = request.form.get('word') 
        word = WordsHandler.query.filter_by(word_id=word, user_id=current_user.id).first()
        db.session.delete(word)
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
        data = [return_object_generator(x.word) for x in current_user.words]
        return jsonify(data)
    elif request.method == 'POST':
        res = make_response()
        data = json.loads(request.data)
        for answer in data:
            word = list(answer)[0]
            is_right = answer[word]
            update_db(current_user, word, is_right)
        return res
    

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

@app.route('/user')
@login_required
def user_page():
    words = current_user.words
    stats = [gen_stats_object(word.word, current_user) for word in words]
    api = current_user.api_key
    username = current_user.username
    data = {'stats': stats, 'username': username, 'api-key': api}
    return data