import urllib.request
num = 1
urls_f = open('urls.txt', 'r')
for line in urls_f:
    url = line
    html = ""
    sock = urllib.request.urlopen(url)
    html = sock.read()
    html = html.decode()
    num += 1
    f = open('htmls/'+ 'file_' + str(num) +'.txt', 'w')
    f.write(html)
    f.close()
    sock.close()