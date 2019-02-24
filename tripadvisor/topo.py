import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

def load_topo_map():

    sparse_matrix = np.load("topo_map.npz")['sparse_matrix']
    data = [
        go.Surface(
            z=sparse_matrix[:1000, :]
        )
    ]
    layout = go.Layout(
        title='Sparse Matrix Topography',
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
    return py.plot(fig, filename='elevations-3d-surface')