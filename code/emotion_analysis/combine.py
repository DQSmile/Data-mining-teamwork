import os
import pandas as pd
import numpy as np

files = []
for i,j,k in os.walk(os.getcwd()):
    files = k[2:]
print(files)

dfs = []
for file in files:
    df = pd.read_csv(file,dtype = {'tweet_id': np.int64})
    print(df.head)
    print(df.dtypes)
    # df = df.dropna(axis=0,how='any')
    dfs.append(df)

result = pd.concat(dfs)
# result.astype({'tweet_id': 'string'}).dtypes
# result['tweet_id'] = result['tweet_id'].astype('int64')
print(result.dtypes)
result.to_csv("all_tweets.csv",index=False)
print(result)
