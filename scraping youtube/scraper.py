import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup as bs
import json
import re
import pandas as pd

def scrape(url):
    print(url)
    response = urllib.request.urlopen(url)
    webContent = response.read()

    html=webContent.decode('utf-8')

    soup=bs(html,"lxml")
    script=soup.find('script', text=re.compile('ytInitialData')).string #find the part of the js script we want
    json_text=script[script.index('{'):script.rindex('}')+1] #hardcoding... 

    data=json.loads(json_text)

    #print(data)

    #with open('bruh.json','w') as out:
    #    json.dump(data,out)
    
    curr=0
    while(not "videoPrimaryInfoRenderer" in data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][curr]): curr+=1
    d=data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][curr]["videoPrimaryInfoRenderer"]
    
    res={}
    res["title"]=d["title"]["runs"][0]["text"]
    res["views"]=d["viewCount"]["videoViewCountRenderer"]["viewCount"]["simpleText"]
    res["likes"]=d["videoActions"]["menuRenderer"]["topLevelButtons"][0]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"]
    res["dislikes"]=d["videoActions"]["menuRenderer"]["topLevelButtons"][1]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"]

    temp=data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][curr+1]["videoSecondaryInfoRenderer"]["description"]["runs"]

    desc=""

    for i in temp:
        desc+=i["text"]
        
    res["desc"]=desc
    
    return pd.Series(res)

videos=[]

temp=open("veritasium.txt","r").read().split("\n")

for id in temp:
    videos.append(scrape("http://www.youtube.com/watch?v="+id))

df=pd.concat(videos,axis=1)
df.to_csv("metadata_veritasium.csv")

