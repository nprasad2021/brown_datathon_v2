import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import pickle as pk

import numpy as np
from itertools import product
import random

n1 = set()
n2 = set()
e = dict()

with open(r'C:\Users\Isaiah Nields\Documents\GitHub\brown_datathon_v2\data\recommendations.pkl','rb') as handle:
    for k, v in pk.load(handle).items():
        n1.add(k)
        n2.update(v)
        e[k] = v

n1 = list(n1)
n2 = list(n2)


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

for x, id_ in zip(np.linspace(-20.0, 20.0, 40), n1):
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([0.0])
    node_trace['marker']['color'] += tuple(['#42b0f4'])
    node_trace['text'] += tuple([str(id_)])

for x, id_ in zip(np.linspace(-20.0, 20.0, 40), n2):
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([-5.0])
    node_trace['marker']['color'] += tuple(['#f44141'])
    node_trace['text'] += tuple([str(id_)])

for x, o in zip(product(np.linspace(-20.0, 20.0, 40), np.linspace(-20.0, 20.0, 40)), product(n1, n2)):
    edges.append(go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#4286f4'),
        opacity=float(o[1] in e[o[0]]),
        hoverinfo='none',
        mode='lines'))

    edges[-1]['x'] += tuple([x[0], x[1], None])
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
