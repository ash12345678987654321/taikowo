import urllib.request, urllib.error, urllib.parse

url = 'https://www.youtube.com/watch?v=kmte4HGJCdo'

response = urllib.request.urlopen(url)
webContent = response.read()

f = open('baba.html','wb')
f.write(webContent)
f.close