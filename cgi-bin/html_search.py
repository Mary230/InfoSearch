#!/usr/bin/env python3
import cgi

form = cgi.FieldStorage()

import pymorphy2

B_FILE = '/Users/bmacha/PycharmProjects/InfoSearch/bool.txt'
URLS_FILE = '/Users/bmacha/PycharmProjects/InfoSearch/urls.txt'


def f_and(arr):
    the_and = 1
    for i in arr:
        the_and = the_and & int(i)
    return the_and


def f_or(arr):
    the_or = 1
    for i in arr:
        the_or = the_or | int(i)
    return the_or


def f_no(arr):
    new_arr = []
    for i in arr:
        if int(i) == 0:
            new_arr.append(1)
        else:
            new_arr.append(0)
    return new_arr


def no_uni(word):
    uni = ["и", "или", "and", "or"]
    for u in uni:
        if word == u:
            return 0
    return 1


def check_on_no(arr):
    new_arr = []
    no = 0
    for i in arr:
        if i == "не":
            no = 1
        else:
            if no == 0:
                new_arr.append(i)
            else:
                no = 0
                new_arr.append("!" + str(i))
    return new_arr


def search_one_word(word):
    finds_arr = []
    b_f = open(B_FILE)
    for l in b_f:
        b_word = l.split("[")[0].strip()
        if word == b_word:
            finds_arr = l.split("[")[1].split(",")
            finds_arr.pop()
    b_f.close()
    return finds_arr


def get_urls(arr_finds):
    urls = []
    result_urls = []
    with open(URLS_FILE, "r") as f:
        urls = f.readlines()
    num = 0
    is_find = 0
    for i in arr_finds:
        if int(i) == 1:
            # print(urls[num])
            result_urls.append(urls[num])
            is_find += 1
        num += 1
    # if is_find == 0:
    # print("Ничего не нашлось")
    return result_urls


def check_uni(arr):
    ind = 1
    new_arr = []
    for i in arr:
        if int(ind % 2 == 0) & no_uni(i):
            new_arr.append("или")
        new_arr.append(i)
        ind += 1
    return new_arr


def searching(search_text):
    morph = pymorphy2.MorphAnalyzer()
    search_text = search_text.strip()

    if len(search_text) < 2:
        # raise IOError("Запрос неверный. Пожалуйста, введите больше двух букв")
        return []
    search_text = search_text.split(" ")
    search_text = [x.lower() for x in search_text]
    search_text = check_uni(check_on_no(search_text))
    if len(search_text) == 1:
        if search_text[0][0] == '!':
            search_text[0] = search_text[0][1:]
            find_arr = search_one_word(search_text[0])
            new_find_arr = []
            for i in find_arr:
                if int(i) == 0:
                    new_find_arr.append(1)
                else:
                    new_find_arr.append(0)
            return get_urls(new_find_arr)
        else:
            return get_urls(search_one_word(search_text[0]))
    if len(search_text) < 1:
        # raise IOError("Запрос неверный. Пожалуйста, введите хотя бы одно слово для поиска")
        return []
    # print("Поисковая строка:", end=' ')
    # [print(x, end=' ') for x in search_text]
    # print()
    unis = []
    for i in search_text:
        if no_uni(i) == 0:
            unis.append(i)
    #         в отдельный лист вынесла все союзы

    index_arr = []
    no = 0
    for i in search_text:
        if no_uni(i):
            b_file = open(B_FILE)
            for line in b_file:
                b_str = line.split("[")[0].strip()
                if i[0] == "!":
                    no = 1
                    i = i[1:]
                if i == b_str:
                    index = line.split("[")[1].split(",")
                    index.pop()
                    if no == 1:
                        index_arr.append(f_no(index))
                        no = 0
                    else:
                        index_arr.append(index)

            b_file.close()

    if len(index_arr) < len(search_text) // 2:
        # raise IOError("Таких слов нет")
        return []

    finish_ind = []
    w_count = range(len(index_arr))
    # кол-во норм слов
    i_b = 0
    chos = []
    for i in index_arr[0]:
        choooo = []
        for count in w_count:
            choooo.append(index_arr[count][i_b])
        i_b += 1
        chos.append(choooo)

    if len(index_arr) > 1:
        for i in chos:
            first = int(i[0])
            c = 1
            for u in unis:
                if u == "и":
                    first = first & int(i[c])
                if u == "или":
                    first = first | int(i[c])
                c += 1
            finish_ind.append(first)

    return get_urls(finish_ind)


text1 = form.getfirst("TEXT_1", "не задано")
urls = searching(text1)

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Поиск</title>
        </head>
        <body>""")
if len(urls) > 0:
    print("<h1>Найдены следующие ссылки:</h1>")
    print("<p><a href = {}> Назад </a>".format("http://localhost:8000/"))
    for url in urls:
        print("<p><a href={}>".format(url) + "{} </a><p>".format(url))
else:
    print("<h1>Ничего не нашлось:(</h1>")
    print("<p><a href = {}> Попробовать снова </a>".format("http://localhost:8000/"))

print("""</body>
        </html>""")
