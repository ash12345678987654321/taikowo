import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup as bs
import json
import re
import random
import time
import os.path

import numpy as np
import pandas as pd

df=pd.read_csv('metadata.csv',index_col=0)
df=df.T

for id in df["id"]:
    if (os.path.exists("thumbs/"+id+".jpg")): continue
    
    print(id)
    url="https://i.ytimg.com/vi/"+id+"/hqdefault.jpg"
    urllib.request.urlretrieve(url,"thumbs/"+id+".jpg")
    
    time.sleep(5)

