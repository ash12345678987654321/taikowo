import pandas as pd

df=pd.read_csv('metadata.csv',index_col=0)
df=df.T

f=open('metadata.txt','w',encoding='utf8')

for idx in df.index:
    for column in df.columns:
        f.write(df[column][idx]+'\0')
        
f.close()