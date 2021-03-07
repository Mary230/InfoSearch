import pymorphy2
from bs4 import BeautifulSoup
import re
TOKKENS_FILE_NAME = 'tokkens.txt'
LEMMAS_FILE_NAME = 'lemmas.txt'
HTML_FILE_PATH = 'htmls/file_'
HTML_FILE_COUNT = 100
tok_f = open(TOKKENS_FILE_NAME, 'w')
lem_f = open(LEMMAS_FILE_NAME, 'w')

def toking(file):
    text = file.get_text()
    text = text.lower()
    result = str(text).replace("\n", " ")
    result = re.sub("[!?@#$%^&'*()_+=-©–«»<>,.\":/;-]", ' ', result)
    result = re.sub("\d+", '', result)
    result = str(result).replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("  ", " ")
    result = result.split(" ")
    result = set(result)
    return result

def lemming(tokens):
    morph = pymorphy2.MorphAnalyzer()
    for word in tokens:
        tok_f.write('<' + word + '>\n')
        lem_f.write('<' + word + '>')
        w_lems = []
        for p in morph.parse(word):
            w_lems.append(p.normal_form)
        w_lems = list(set(w_lems))
        for lem in w_lems:
            lem_f.write('<' + lem + '>')
        lem_f.write('\n')

num = 1
tokens = []
while num<=HTML_FILE_COUNT:
    f = open(HTML_FILE_PATH + str(num) +'.txt')
    html_doc = f.read()
    num += 1
    soup = BeautifulSoup(html_doc)
    tokens = tokens + list(toking(soup))
    f.close()
tokens = set(tokens)
lemming(tokens)




