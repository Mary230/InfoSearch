import re
TOKKENS_FILE_NAME = 'lemmas.txt'
HTML_FILE_PATH = 'htmls/file_'
HTML_FILE_COUNT = 100
INDEX_FILE = 'inverted_index.txt'
B_FILE = 'bool.txt'
tok_f = open(TOKKENS_FILE_NAME)
index_file = open(INDEX_FILE, 'w')
b_file = open(B_FILE, 'w')

def lems_to_normalform(lemmas):
    new_tokkens = []
    tokens = lemmas.read().replace("<", " ").replace(">", " ").replace("\n", ";;").split(";;")
    for i in tokens:
        i = i.split(" ")
        for ii in i:
            if len(ii) < 2:
                i.remove(ii)
        new_tokkens.append(i)
    return new_tokkens

num = 1
is_in_file = 0
find = []
find_in_all = 0

tokens = lems_to_normalform(tok_f)
for lems in tokens :
    if len(lems)>0 :
        index_file.write(lems[0] + '[')
        b_file.write(lems[0] + '[')
        while num <= HTML_FILE_COUNT :
            find = 0
            f = open(HTML_FILE_PATH + str(num) + '.txt')
            html_doc = f.read()
            for word in lems:
                find = find + len(re.findall(word, html_doc))
            if find > 0:
                index_file.write(str(num) + ':' + str(find) + ';')
                #формат слово [номер файла:кол-во вхождений;номер файла1:кол-во вхождений1;...]
            if find > 0:
                b_file.write('1,')
            else:
                b_file.write('0,')
            num += 1
            f.close()
        b_file.write(']\n')
        index_file.write(']\n')
        num = 1






