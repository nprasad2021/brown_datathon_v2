import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

results = np.load("results.npz")['results']
sparse_matrix = np.array(results).reshape(len(set(sparse_df['user_id'])),-1)

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