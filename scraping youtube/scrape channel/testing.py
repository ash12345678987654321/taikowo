import urllib.request
from bs4 import BeautifulSoup as bs
import json
import re

url='https://www.youtube.com/channel/UCqGtqSn0NiOCottKpYwBc4w/videos' #Futakuchi Mana

response = urllib.request.urlopen(url)
webContent = response.read()

html=webContent.decode('utf-8')

#open("dump.html","w",encoding="utf-8").write(html)

soup=bs(html,"lxml")
script=soup.find('script', text=re.compile('ytInitialData')).string #find the part of the js script we want
json_text=script[script.index('{'):script.rindex('}')+1] #hardcoding... 

data=json.loads(json_text)

#with open('bruh.json','w') as out:
#    json.dump(data,out)

temp=data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["gridRenderer"]["items"]

f=open("mana.txt","w")

for x in temp:
    if "gridVideoRenderer" in x:
        f.write(x["gridVideoRenderer"]["videoId"]+"\n")