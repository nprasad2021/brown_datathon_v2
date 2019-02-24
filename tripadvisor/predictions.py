import keras
import util
import numpy as np

NUM_SAMPLES = 40
DATAFRAME_NAME = "new.csv"

df = util.create_sparse_matrix(DATAFRAME_NAME, replace=False)

n_users, n_movies = len(df.user_id.unique()), len(df.hotel_id.unique())

with open('user_id_map.pkl', 'rb') as handle:
            user_index_map = pickle.load(handle)
with open('hotel_id_map.pkl', 'rb') as handle:
            hotel_index_map = pickle.load(handle)

inverse_user_map = {value:key for key, value in user_index_map.items()}
inverse_hotel_map = {value:key for key, value in hotel_index_map.items()}

df['user_id'] = df['user_id'].apply(lambda x: user_index_map[x])

df['hotel_id'] = df['hotel_id'].apply(lambda x: hotel_index_map[x])

user_ids = np.array(sorted(list(df.user_id)))
hotel_ids = np.array(sorted(list(df.hotel_id)))

model = keras.models.load_model("nn.h5")
results = model.predict([user_ids, hotel_ids])

user_ids = [inverse_user_map[id] for id in user_ids]
hotel_ids = [inverse_hotel_map[id] for id in hotel_ids]

results_df = pd.DataFrame(data = [user_ids, hotel_ids, results], columns = ['user_ids','hotel_ids','results'])

def topo_graph(results)
	sparse_matrix = np.array(results).reshape(len(set(sparse_df['user_id'])),-1)

	import plotly.plotly as py
	import plotly.graph_objs as go

	import pandas as pd

	z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
	print(z_data.as_matrix().shape)
	data = [
	    go.Surface(
	        z=sparse_matrix[:1000, :]
	    )
	]
	layout = go.Layout(
	    title='Dense Matrix Topography',
	    autosize=False,
	    width=500,
	    height=500,
	    margin=dict(
	        l=65,
        	r=50,
        	b=65,
        	t=90
    		)
	)
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename='elevations-3d-surface')
	return fig

def get_recs(results):
	sample_users = np.random.choice(user_ids, NUM_SAMPLES)
	recommendations = {}

	for user in sample_users:
		sub_result = results.loc[results['user_id']==user].sort_values('results',ascending=False)
		recommendations[user] = list(sub_result['hotel_id'])[:5]
	return recommendations	

with open('recommendations.pkl', 'wb') as handle:
	pickle.dump(get_recs(results_df),handle)
