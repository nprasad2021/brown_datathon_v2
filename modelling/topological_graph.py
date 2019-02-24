import pandas as pd
import numpy as np
import datetime
import time
import math
import util

start = time.time()
sparse_df = util.create_sparse_matrix("new.csv", replace=False)
print("time", time.time() - start)

sparse_matrix = np.array(sparse_df['user_action']).reshape(len(set(sparse_df['user_id'])),-1)

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
    title='Mt Bruno Elevation',
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

