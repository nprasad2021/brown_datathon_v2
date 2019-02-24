import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

results = np.load(r"C:\Users\Isaiah Nields\Documents\GitHub\brown_datathon_v2\tripadvisor\results.npz")['results']
results = results[:9969820]
print(results.shape)
sparse_matrix = np.array(results).reshape(24140,-1)

data = [
    go.Surface(
        z=sparse_matrix[:1000, :]
    )
]
layout = go.Layout(
    title='Dense Matrix Topography',
    autosize=True
)

fig = go.Figure(data=data, layout=layout)