import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from data.data import geocodes, hotels, hotel_activity
from math import exp

mapbox_access_token = 'pk.eyJ1IjoiaXNhaWFobmllbGRzIiwiYSI6ImNqc2k2MzIxbDB3MGMzeWs2ZTI0NGo4emsifQ.yMgpcq_uvWM8nkxdH0DE9Q'

geocodes = pd.merge(hotels, geocodes, on='hotel_id', how='left')
geocodes = geocodes.dropna()


def create_data(key, title):
    return [
        go.Scattermapbox(
            lat=geocodes['lat'],
            lon=geocodes['lng'],
            mode='markers',
            marker=dict(
                size=12,
                color=geocodes[key]
            ),
            text=['Name: ' + str(i) + '\n' + title + ': ' + str(j) for i, j in zip(geocodes['hotel_name'], geocodes[key])]
        )
    ], go.Layout(
        autosize=True,
        hovermode='closest',
        title=title,
        titlefont=dict(size=16),
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=40.7272,
                lon=-73.991251
            ),
            pitch=0,
            zoom=12.0
        ),
    )

graphs = []
for key, title in [('star_rating', 'Star Ratings'), ('bubble_score', 'Bubble Score'), ('review_count', 'Review Count')]:
    d = create_data(key, title)
    graphs.append(dict(data=d[0], layout=d[1]))

#--------------------------------------------------------------------------

p = hotel_activity.groupby(by='hotel_id').size()

d, l = [
        go.Scattermapbox(
            lat=geocodes['lat'],
            lon=geocodes['lng'],
            mode='markers',
            marker=dict(
                size=12,
                color=[ i / (1.01 ** i) for i in p.to_list()]
            ),
            text=['Name: ' + str(i) + '\n' + title + ': ' + str(j) for i, j in zip(geocodes['hotel_name'], p.to_list())]
        )
    ], go.Layout(
        autosize=True,
        hovermode='closest',
        title='Number of Events',
        titlefont=dict(size=16),
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=40.7272,
                lon=-73.991251
            ),
            pitch=0,
            zoom=12.0
        ),
    )

graphs.append(dict(data=d, layout=l))

