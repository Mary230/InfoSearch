# InfoSearch
Repo for hometask 
Для исполнения кода необходимо скачать библиотеку urllib

 git clone git://github.com/urllib3/urllib3.git
 python setup.py install
 
 Файл urls.txt - список ссылок
 В папке htmls лежат готовые файлы
 
Список слов - файл words.txt

Список токенов - файл tokkens.txt

Список лемм - файл lemmas.txt

При запуске файла search.py нужно ввести строку для поиска в формате: слово и/или (не) слово и/или (не) слово ...

Параметры tf, idf находятся в файлах с соответствующим названием и расширением txt.

Для запуска:
python3 -m http.server --cgi
Открываем http://localhost:8000/
Вводим слово (слова)
