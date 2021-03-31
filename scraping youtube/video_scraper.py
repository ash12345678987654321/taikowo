import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup as bs
import json
import re
import random

import numpy as np
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
    if ("viewCount" in d):
        res["views"]=d["viewCount"]["videoViewCountRenderer"]["viewCount"]["simpleText"]
    else:
        res["views"]=np.nan
    
    if ("accessibility" in d["videoActions"]["menuRenderer"]["topLevelButtons"][0]["toggleButtonRenderer"]["defaultText"]): #likes/dislikes hidden
        res["likes"]=d["videoActions"]["menuRenderer"]["topLevelButtons"][0]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"]
        res["dislikes"]=d["videoActions"]["menuRenderer"]["topLevelButtons"][1]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"]
    else:
        res["likes"]=np.nan
        res["dislikes"]=np.nan
        
    temp=data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][curr+1]["videoSecondaryInfoRenderer"]
    
    if "description" in temp: #age restrcited videos dont have :/
        desc=""
        for i in temp["description"]["runs"]:
            desc+=i["text"]
            
        res["desc"]=desc
    else:
        res["desc"]=np.nan
    
    return pd.Series(res)

videos=[]

inp=open("ids.txt","r").read().split("\n")
inp=inp[:-1] #kill last video

random.shuffle(inp)

curr=1
for id in inp[:2000]: #first 2000 bcas lazy
    print("current:",str(curr))
    curr+=1

    temp=id.split("\t")
    dat=scrape("http://www.youtube.com/watch?v="+temp[0])
    dat["id"]=temp[0]
    dat["clickbait"]=temp[1]
    
    videos.append(dat)

df=pd.concat(videos,axis=1)
df.to_csv("metadata.csv")

