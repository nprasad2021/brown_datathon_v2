import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from keras.optimizers import Adam
from sklearn.metrics import mean_absolute_error
import util
import keras
import os
import pickle
print(keras.__version__)

DATAFRAME_NAME = './new.csv'

df = util.create_sparse_matrix(DATAFRAME_NAME, replace=False)

n_users, n_movies = len(df.user_id.unique()), len(df.hotel_id.unique())
user_index_map = {ids:i for (ids, i) in zip(list(set(df['user_id'])),list(range(n_users)))}
df['user_id'] = df['user_id'].apply(lambda x: user_index_map[x])

hotel_index_map = {ids:i for (ids, i) in zip(list(set(df['hotel_id'])),list(range(n_movies)))}
df['hotel_id'] = df['hotel_id'].apply(lambda x: hotel_index_map[x])
print(df.head())
train, test = train_test_split(df, test_size=0.2)

with open('user_id_map.pkl',wb) as handle:
	pickle.dump(user_index_map, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('hotel_id_map.pkl',wb) as handle:
	pickle.dump(hotel_index_map, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(n_users, n_movies)	

n_latent_factors_user = 5
n_latent_factors_movie = 8

movie_input = keras.layers.Input(shape=[1],name='Item')
movie_embedding = keras.layers.Embedding(n_movies + 1, n_latent_factors_movie, name='Movie-Embedding')(movie_input)
movie_vec = keras.layers.Flatten(name='FlattenMovies')(movie_embedding)
movie_vec = keras.layers.Dropout(0.2)(movie_vec)


user_input = keras.layers.Input(shape=[1],name='User')
user_vec = keras.layers.Flatten(name='FlattenUsers')(keras.layers.Embedding(n_users + 1, n_latent_factors_user,name='User-Embedding')(user_input))
user_vec = keras.layers.Dropout(0.2)(user_vec)


concat = keras.layers.merge([movie_vec, user_vec], mode='concat',name='Concat')
concat_dropout = keras.layers.Dropout(0.2)(concat)
dense = keras.layers.Dense(200,name='FullyConnected')(concat)
dropout_1 = keras.layers.Dropout(0.2,name='Dropout')(dense)
dense_2 = keras.layers.Dense(100,name='FullyConnected-1')(concat)
dropout_2 = keras.layers.Dropout(0.2,name='Dropout')(dense_2)
dense_3 = keras.layers.Dense(50,name='FullyConnected-2')(dense_2)
dropout_3 = keras.layers.Dropout(0.2,name='Dropout')(dense_3)
dense_4 = keras.layers.Dense(20,name='FullyConnected-3', activation='relu')(dense_3)


result = keras.layers.Dense(1, activation='relu',name='Activation')(dense_4)
adam = Adam(lr=0.005)
model = keras.models.Model([user_input, movie_input], result)
model.compile(optimizer=adam,loss= 'mean_absolute_error')

history = model.fit([train.user_id, train.hotel_id], train.user_action, epochs=1, verbose=1)

y_hat_2 = np.round(model.predict([test.user_id, test.hotel_id]),0)
y_true = test.user_action
print(mean_absolute_error(y_true, y_hat_2))
print("MAE", mean_absolute_error(y_true, model.predict([test.user_id, test.hotel_id])))

model.save("nn.h5")
