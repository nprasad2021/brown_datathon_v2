import keras
import util
import numpy as np

NUM_SAMPLES = 40

df = util.create_rec_data('./colab_filter.csv')
df = df.sample(n=NUM_SAMPLES)
user_ids = np.array(sorted(list(df.user_id)))
hotel_ids = np.array(sorted(list(df.hotel_id)))

model = keras.models.load_model("nn.h5")
results = model.predict([user_ids, hotel_ids])

print(results)
