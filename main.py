import urllib.request
num = 1
urls_f = open('urls.txt', 'r')
index = open('index.txt', 'w')
for line in urls_f:
    url = line
    html = ""
    sock = urllib.request.urlopen(url)
    html = sock.read()
    html = html.decode()
    f = open('htmls/'+ 'file_' + str(num) +'.txt', 'w')
    index.write('file_' + str(num) + '  ' + line + ' \n')
    num += 1
    f.write(html)
    f.close()
    sock.close()