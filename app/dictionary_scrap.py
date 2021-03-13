from app import db
from app.models import PolishWords, EnglishWords
import requests
from bs4 import BeautifulSoup


def getTranslate(word):
    url = 'https://pl.pons.com/t%C5%82umaczenie/angielski-polski/'

    res = requests.get(url + word)
    soup = BeautifulSoup(res.text, 'html.parser')

    translations = getScrapWords(soup)
    if translations:
        putIntoDb(word, translations)
        return True
    return False


def getScrapWords(bsObj):
    words = bsObj.find_all('div', {'class': 'target'})
    alert = bsObj.find('div', {'class': 'fuzzysearch'})
    if alert:
        return False
    translations = set()
    for word in words:
        word = word.find('a')
        if word:
            translations.add(word.string)
    return translations


def putIntoDb(translate_word, list_of_translations):
    db_trans = EnglishWords(word=translate_word)
    db.session.add(db_trans)
    for pol_word in list_of_translations:
        wt = PolishWords.query.filter_by(word=pol_word).first()
        if wt:
            wt.eng_translate=db_trans
        else:
            wt = PolishWords(word=pol_word)
            db.session.add(wt)
            db_trans.pol_translate.append(wt)
    db.session.commit()


