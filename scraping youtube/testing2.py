from bs4 import BeautifulSoup as bs
import json
import re

html=open('baba.html','r',encoding='utf-8').read()

soup=bs(html,"lxml")
script=soup.find('script', text=re.compile('ytInitialData')).string #find the part of the js script we want
json_text=script[script.index('{'):script.rindex('}')+1] #hardcoding... 

data=json.loads(json_text)

#print(data)

with open('bruh.json','w') as out:
    json.dump(data,out)
    
d=data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]
print(d["title"]["runs"][0]["text"])
print(d["viewCount"]["videoViewCountRenderer"]["viewCount"]["simpleText"])
print(d["videoActions"]["menuRenderer"]["topLevelButtons"][0]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"])
print(d["videoActions"]["menuRenderer"]["topLevelButtons"][1]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"])

temp=data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][1]["videoSecondaryInfoRenderer"]["description"]["runs"]

desc=""

for i in temp:
    desc+=i["text"]
    
print(desc)

