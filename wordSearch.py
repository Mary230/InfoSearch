import pymorphy2
from bs4 import BeautifulSoup
import re
import string

TOKKENS_FILE_NAME = 'tokkens.txt'
LEMMAS_FILE_NAME = 'lemmas.txt'
HTML_FILE_PATH = 'htmls/file_'
HTML_FILE_COUNT = 100
tok_f = open(TOKKENS_FILE_NAME, 'w')
lem_f = open(LEMMAS_FILE_NAME, 'w')


def contains_whitespace(s):
    return True in [c in s for c in string.whitespace]


def toking(file):
    text = file.get_text()
    text = text.lower()
    result = str(text)
    result = re.sub(r'\b\w{1,3}\b', '', result)
    result = re.sub(r'\b\w{20,100}\b', '', result)
    result = re.sub(r'[^А-Яа-я]+', ' ', result)
    result = result.split()
    result = list(set(result))
    for i in result:
        ind = result.index(i)
        new_i = re.sub(r'[^А-Яа-я]+', ' ', i)
        new_i = new_i.strip()
        if contains_whitespace(new_i):
            new_i = new_i.split()
            del result[ind]
            result = result + list(new_i)
        else:
            result[ind] = new_i
    result = list(set(result))
    for i in result:
        if len(i) < 4:
            result.remove(i)
    for i in result:
        if len(i) > 20:
            result.remove(i)
    return result


def lemming(tokens):
    morph = pymorphy2.MorphAnalyzer()
    for word in tokens:
        str(word).replace(' ', '')
        tok_f.write('<' + word.strip() + '>\n')
        lem_f.write('<' + word.strip() + '>')
        w_lems = []
        for p in morph.parse(word):
            w_lems.append(p.normal_form)
        w_lems = list(set(w_lems))
        for lem in w_lems:
            lem_f.write('<' + lem + '>')
        lem_f.write('\n')


num = 1
tokens = []
while num <= HTML_FILE_COUNT:
    f = open(HTML_FILE_PATH + str(num) + '.txt')
    html_doc = f.read()
    num += 1
    soup = BeautifulSoup(html_doc, 'html5lib')
    tokens = tokens + list(toking(soup))
    f.close()
tokens = set(tokens)
lemming(tokens)
