import numpy as np
import pandas as pd
import face_recognition

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches

df=pd.read_csv('metadata_alpha.csv',index_col=0)

df=df.T

def get_img(id):
    return mpimg.imread('thumbs/'+id+'.jpg')

curr=0
for id in df["id"]:
    print(id,curr)
    curr+=1
    
    img=get_img(id)
    
    locs=face_recognition.face_locations(img)
    
    for x in range(min(3,len(locs))):
        t,r,b,l=locs[x]
        
        plt.imsave('faces/'+id+'_'+str(x)+'.jpg',img[t:b,l:r])
