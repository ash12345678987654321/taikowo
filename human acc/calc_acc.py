import pandas as pd
import os

df=pd.read_csv('metadata.csv',index_col=0)
df=df.T

for file in os.listdir("results/"):
    res=open("results/"+file).read().split("\n")
    
    tp=0
    fn=0
    fp=0
    
    for idx in df.index:
        if (df["clickbait"][idx]=='1' and res[int(idx)]=='1'): tp+=1
        if (df["clickbait"][idx]=='1' and res[int(idx)]=='0'): fn+=1
        if (df["clickbait"][idx]=='0' and res[int(idx)]=='1'): fp+=1
        
    print(file)
    print(tp,fn,fp)
    print("f1: ",2*tp/(2*tp+fn+fp))
