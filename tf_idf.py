import math
import re
import string

from bs4 import BeautifulSoup

HTML_FILE_PATH = 'htmls/file_'
TF_FILE = 'tf.txt'
IDF_FILE = 'idf.txt'
# TF_IDF_FILE = 'tf_idf.txt'
HTML_FILE_COUNT = 100
INVERTED_INDEX_FILE = 'inverted_index.txt'
INVERTED_INDEX_W_COUNT = 17326
TF_FACTOR = 100000


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


def int_r(num_to_round):
    num_to_round = int(num_to_round + (0.5 if num_to_round > 0 else -0.5))
    return num_to_round


html_words = [0] * 100

num = 1
while num <= HTML_FILE_COUNT:
    f = open(HTML_FILE_PATH + str(num) + '.txt')
    html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html5lib')
    html_words[num - 1] = len(toking(soup))
    num += 1
    f.close()
print(html_words)
tf = 0
tf_file = open(TF_FILE, 'w')
idf_file = open(IDF_FILE, 'w')
# tf_idf_file = open(TF_IDF_FILE, 'w')
tf_file_string = ''
idf_file_string = ''
# tf_idf_file_string = ''
with open(INVERTED_INDEX_FILE, 'r') as inverted_index_file:
    line_num = 0
    while line_num < INVERTED_INDEX_W_COUNT:
        tfs = []
        file_count = 0
        line = inverted_index_file.readline()
        word = line.split("[")[0].strip()
        file_num_and_word_count = line.split("[")[1].split(";")
        file_num_and_word_count.pop()
        tf_file_string = word + '['
        idf_file_string = word + '['
        # tf_idf_file_string = word + '['
        for i in file_num_and_word_count:
            file_count += 1
            f_num = int(i.split(":")[0]) - 1
            w_count = int(i.split(":")[1])
            f_w_count = int(html_words[f_num])
            if f_w_count > 0:
                tf = math.ceil((w_count / f_w_count) * TF_FACTOR)
            else:
                tf = 0
            # tfs.append(tf)
            # tf_file_string = tf_file_string + str(f_num + 1) + ':' + str(tf) + ';'
        tf_file_string = tf_file_string + ']\n'
        if file_count == 0:
            file_count = 0.01
        idf = math.log10(HTML_FILE_COUNT / file_count)
        # for i in tfs:
        #     tf_idf_file_string = tf_idf_file_string + str(f_num) + ':' + str(int(tf)*idf) + ';'
        idf_file_string = idf_file_string + str(file_count) + ']\n'
        # tf_idf_file_string = tf_idf_file_string + ']\n'
        tf_file.write(tf_file_string)
        idf_file.write(idf_file_string)
        # tf_idf_file.write(tf_idf_file_string)
        line_num += 1
