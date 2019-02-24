from data.data import activity
import plotly.plotly as py
import plotly.graph_objs as go

l = go.Layout(
        autosize=True,
        title='Activity vs. Time for April 2019',
        titlefont=dict(size=16),
    )

def create_scatter(y, title):
    # Create traces
    return go.Scatter(
        x=['01/' + str(i) + '/2019' for i in range(1, 32)],
        y= [i / max(y) for i in y],
        mode='lines',
        name=title,
        line={'shape': 'spline', 'smoothing': 1.3}
    )


activity = activity.groupby(by=['user_action', 'date']).size()
graphs = []

for t, title in [('booking', 'Booking'), ('view', 'View'), ('hotel_website_click', 'Website Click'),
             ('price_click', 'Price Click')]:
    x = activity[t].to_list()
    graphs.append(create_scatter(x, title))

graph = go.Figure(data=graphs, layout=l)