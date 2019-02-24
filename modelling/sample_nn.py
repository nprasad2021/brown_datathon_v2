import pandas as pd
import util

DATAFRAME_NAME = './new.csv'

df = util.create_sparse_matrix(DATAFRAME_NAME, replace=False).iloc[:2000,:]

n_users, n_movies = len(df.user_id.unique()), len(df.hotel_id.unique())
print(n_movies)
user_index_map = {ids:i for (ids, i) in zip(list(set(df['user_id'])),list(range(n_users)))}
df['user_id'] = df['user_id'].apply(lambda x: user_index_map[x])

hotel_index_map = {ids:i for (ids, i) in zip(list(set(df['hotel_id'])),list(range(n_movies)))}
df['hotel_id'] = df['hotel_id'].apply(lambda x: hotel_index_map[x])

df.to_csv("data.csv")