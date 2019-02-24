import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

import pandas as pd

sparse_matrix = np.load(r"C:\Users\Isaiah Nields\Documents\GitHub\brown_datathon_v2\tripadvisor\topo_map.npz")['sparse_matrix']
data = [
    go.Surface(
        z=sparse_matrix[:1000, :]
    )
]
layout = go.Layout(
    title='Sparse Matrix Topography',
    autosize=True
    # margin=dict(
    #     l=65,
    #     r=50,
    #     b=65,
    #     t=90
    # )
)
fig = go.Figure(data=data, layout=layout)

