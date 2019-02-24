import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import keras
import util

import os


DATAFRAME_NAME = 'colab_filter.csv'


if not os.path.exists(DATAFRAME_NAME):
    df = util.create_rec_data(DATAFRAME_NAME)
else:
    df = pd.read_csv(DATAFRAME_NAME)

train, test = train_test_split(df, test_size=0.2)

n_users, n_movies = len(df.user_id.unique()), len(df.hotel_id.unique())
n_latent_factors = 3

movie_input = keras.layers.Input(shape=[1],name='Item')
movie_embedding = keras.layers.Embedding(n_movies + 1, n_latent_factors, name='Movie-Embedding')(movie_input)
movie_vec = keras.layers.Flatten(name='FlattenMovies')(movie_embedding)

user_input = keras.layers.Input(shape=[1],name='User')
user_vec = keras.layers.Flatten(name='FlattenUsers')(keras.layers.Embedding(n_users + 1, n_latent_factors,name='User-Embedding')(user_input))

prod = keras.layers.merge([movie_vec, user_vec], mode='dot',name='DotProduct')
model = keras.models.Model([user_input, movie_input], prod)
model.compile('adam', 'mean_squared_error')

print(model.summary())
history = model.fit([train.user_id, train.hotel_id], train.user_action, epochs=2, verbose=1)

pd.Series(history.history['loss']).plot(logy=True)
plt.xlabel("Epoch")
plt.ylabel("Train Error")

plt.savefig("train_accuracy.pdf", dvi=1000)
plt.close()

y_hat = np.round(model.predict([test.user_id, test.hotel_id]),0)
y_true = test.user_action

print("MAE", mean_absolute_error(y_true, y_hat))

model.save("mf.h5")