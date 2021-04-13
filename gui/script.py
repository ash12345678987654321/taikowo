import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import string
import time
import re
import nltk

# Import WordNetLemmatizer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')

import pickle

import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup as bs
import json


def scrape(url):
    #print(url)
    id=url[-11:]
    #time.sleep(1) #so that google doesnt block us
    
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
    
    




#load adapted text vectorize layer from pickle
from_disk = pickle.load(open("tv_layer.pkl", "rb"))
vectorize_layer = TextVectorization.from_config(from_disk['config'])
# You have to call `adapt` with some dummy data (BUG in Keras)
vectorize_layer.adapt(tf.data.Dataset.from_tensor_slices(["testing"]))
vectorize_layer.set_weights(from_disk['weights'])


#nlp preprocessing on string
def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    #print(tag_dict.get(tag, wordnet.NOUN))
    return tag_dict.get(tag, wordnet.NOUN)

pattern = re.compile("【|】|\[|\]")

# Initalize TweetTokenizer
tt = TweetTokenizer()

# English stop words
english_stops = stopwords.words('english')

printable = set(string.printable)

# Instantiate the WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

def editString(title):
    title = pattern.sub("|",title)                             # replace square brackets with |
    title = "".join(filter(lambda x: x in printable, title))   # remove non printable characters
    #print(title)
    tokens = tt.tokenize(text=title)
    
    # Convert the tokens into lowercase: lower_tokens, indicate if capital
    tokens_edited = [t.lower() + " [&CAP] " if (t.upper() == t and t.isalpha() and len(t) > 1) else t.lower() for t in tokens ]
    #print(tokens_edited)
    # Remove all stop words: no_stops
    no_stops = [t for t in tokens_edited if t not in english_stops]
    #print(no_stops)
    # Lemmatize all tokens into a new list: lemmatized
    lemmatized = [wordnet_lemmatizer.lemmatize(t, get_wordnet_pos(t)) for t in no_stops]
    #print(lemmatized)
    return " ".join(lemmatized)

def vectorize_text(text):
    text = tf.expand_dims(text, -1)
    return vectorize_layer(text)
    
def process(text):
    return vectorize_text(editString(text))

#print(editString("when the imposter is SUS!!"))
#print(vectorize_text("lol"))


def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

from_disk = pickle.load(open("model.pkl", "rb"))
model = tf.keras.Model.from_config(from_disk['config'])
model.set_weights(from_disk['weights'])
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["acc", precision_m, recall_m, f1_m])

def evaluate(url):
    dat=scrape(url)
    id = url[-11:]
    thumbnailurl = "https://i.ytimg.com/vi/"+id+"/hqdefault.jpg"
    title = dat["title"]
    val=model.predict(process(title))[0][0]
    return val, title, thumbnailurl;
    


import tkinter as tk
import time
import io
import base64
from urllib.request import urlopen
from PIL import Image, ImageTk
import tkinter.font as font


window = tk.Tk()
window.geometry("500x500")
window.title("Clickbait Identifier")
entry = tk.Entry(width=50)
entry.pack()
button = tk.Button(
    text="Is it clickbait?",
    width=500,
    height=1,
)
button.pack()
title = tk.Label(text="",wraplength=500)

title['font'] = font.Font(size=12)
title.pack()
imagepane = tk.Label(window,text="")
imagepane.pack()
result = tk.Label(window,image="")
result['font'] =  font.Font(size=20)
result.pack()



def handle_click(event):
    url = entry.get()
    result["text"] = "Loading..."
    title["text"] = ""
    if (True):
        val, TITLE, IMAGEURL = evaluate(url)
        title["text"] = TITLE
        img = ImageTk.PhotoImage(Image.open(urlopen(IMAGEURL)))
        imagepane.configure(image=img)
        imagepane.image = img
        if (val > 0.5):
            result["text"] = "CLICKBAIT: score = {:.3f}".format(val)
        else:
            result["text"] = "NOT CLICKBAIT: score = {:.3f}".format(val)
    else:
        result["text"] = "Error occurred"
        title["text"] = ""
    

    
button.bind("<Button-1>", handle_click)
window.mainloop()



