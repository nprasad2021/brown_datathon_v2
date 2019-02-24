import plotly.plotly as py
import plotly
import plotly.graph_objs as go

import numpy as np
from itertools import product
import random

r = lambda: random.randint(0, 255)
from data.data import geocodes, hotels

edges = []

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=False,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

for x in np.linspace(-20.0, 20.0, 20):
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([0.0])
    node_trace['marker']['color'] += tuple(['#42b0f4'])

for x in np.linspace(-20.0, 20.0, 20):
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([-5.0])
    node_trace['marker']['color'] += tuple(['#f44141'])

for x1, x2 in product(np.linspace(-20.0, 20.0, 20), np.linspace(-20.0, 20.0, 20)):
    edges.append(go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#4286f4'),
        opacity=random.random(),
        hoverinfo='none',
        mode='lines'))

    edges[-1]['x'] += tuple([x1, x2, None])
    edges[-1]['y'] += tuple([0.0, -5.0, None])

graph = go.Figure(data=[*edges, node_trace],
              layout=go.Layout(
                  title='Recommendation Graph',
                  titlefont=dict(size=16),
                  showlegend=False,
                  hovermode='closest',
                  margin=dict(b=20, l=5, r=5, t=40),
                  annotations=[dict(
                      text="",
                      showarrow=False,
                      xref="paper", yref="paper",
                      x=0.005, y=-0.002)],
                  xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
