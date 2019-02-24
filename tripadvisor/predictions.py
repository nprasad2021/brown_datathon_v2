import keras
import util
import numpy as np

NUM_SAMPLES = 40
DATAFRAME_NAME = "new.csv"

df = util.create_sparse_matrix(DATAFRAME_NAME, replace=False)

n_users, n_movies = len(df.user_id.unique()), len(df.hotel_id.unique())
user_index_map = {ids:i for (ids, i) in zip(list(set(df['user_id'])),list(range(n_users)))}
df['user_id'] = df['user_id'].apply(lambda x: user_index_map[x])

hotel_index_map = {ids:i for (ids, i) in zip(list(set(df['hotel_id'])),list(range(n_movies)))}
df['hotel_id'] = df['hotel_id'].apply(lambda x: hotel_index_map[x])

user_ids = np.array(sorted(list(df.user_id)))
hotel_ids = np.array(sorted(list(df.hotel_id)))

model = keras.models.load_model("nn.h5")
results = model.predict([user_ids, hotel_ids])

print(results)
