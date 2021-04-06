import pandas as pd

df=pd.read_csv('metadata.csv',index_col=0)
df=df.T

res=open("results.txt","r").read().split("\n")

curr=0

correct=0
total=0
for idx in df.index:
    if (df["clickbait"][idx]==res[curr]): correct+=1
    total+=1
    
    curr+=1

print(correct,total)
