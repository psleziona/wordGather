from flask import request, render_template, jsonify, redirect, url_for, Response
from app import app, db
from app.dictionary_scrap import getTranslate
from app.models import EnglishWords, PolishWords, Users, WordsHandler
from flask_login import login_user, current_user, login_required
import random, json
from app.learning_system import test_answer_generator

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



@app.route('/word', methods = ['POST', 'GET', 'DELETE', 'PUT'])
# @login_required
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

        response_obj = Response()
        response_obj.headers.add('Access-Control-Allow-Origin', '*')
        res_data = {'msg': ''}
        # albo funkcja msg -> resObj with msg?

        if db_word:
            if db_word in [x.word for x in current_user.words]:
                res_data['msg'] = 'alert: masz to'
                response_obj.data = json.dumps(res_data)
                return response_obj
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
    elif request.method == 'DELETE':
        name = request.form.get('word')
        word = EnglishWords.query.filter_by(word=name).first()
        db.session.delete(word)
        db.session.commit()
        return 'deleted'
    elif request.method == 'PUT':
        '''
         {'word': 'x', 'right': bool}
    '''
    
        data = json.loads(request.data)
        word = EnglishWords.query.filter_by(word=data['word']).first()
        wh_obj = WordsHandler.query.filter_by(word_id=word.id, user_id=current_user.id).first()
        wh_obj.show_counter += 1
        if data['right']:
            wh_obj.right_answers += 1
        wh_obj.progress_eval()
        return 'done'

@app.route('/word/progress_filter/<float:progress>')
# @login_required
def progress_filter(progress):
    current_user = Users.query.get(1)
    word = random.choice([x.word for x in current_user.words if x.progress and x.progress <= progress]) # cannot choose from empty / default progress 0 and x.progress > 0?
    return {'word': word.word, 'translates': [x.word for x in word.pol_translate]}

#funkcja do zwracania odpowiednich danych w zaleznosci od endpointu?
# jeden endpoint do odbierania wynikow

@app.route('/words')
def all_words():
    current_user = Users.query.get(1)
    data = [{'word': x.word.word, 'translates': [w.word for w in x.word.pol_translate]} for x in current_user.words]
    return jsonify(data)

@app.route('/words/<int:count>')
def words(count):
    words = EnglishWords.query.all()
    random.shuffle(words)
    words = words[:count]
    data = [{'word': x.word, 'translates': [w.word for w in x.pol_translate]} for x in words]
    return jsonify(data)
    











@app.route('/test', methods=['GET', 'POST'])
def testa():
    current_user = Users.query.get(1)
    if request.method == 'GET':
        w = random.choice(EnglishWords.query.all())
        return {'word': w.word, 'answers': test_answer_generator(w)}
    else:
        '''
        [
            {
                'word': word,
                'right': bool
            },
            ...
        ]
        '''
        lista_ass = []
        data = json.loads(request.data)
        for eng_word in data:
            word = EnglishWords.query.filter_by(word=eng_word['word']).first()
            right = eng_word['bool']
            print(right)
            as_obj = WordsHandler(word_id=word.id, user_id=current_user.id)
            #increase counter, check if right, if so then right_counter increase, count progress
            lista_ass.append(as_obj)
        print(lista_ass)
        db.session.commit()
        return 'testy'