import pandas as pd


df_all = pd.read_csv('../../ml-1m/ratings.dat',sep='::',names=['USER_ID','ITEM_ID','EVENT_VALUE', 'TIMESTAMP'])

df_all['EVENT_TYPE']='RATING'
items_all = pd.read_csv('../../ml-1m/movies.dat',sep='::', encoding='latin1',names=['ITEM_ID', '_TITLE', 'GENRE'],)
df_all.to_csv('interactions.csv',index=False)
items_all.to_csv('movies.csv', index=False)