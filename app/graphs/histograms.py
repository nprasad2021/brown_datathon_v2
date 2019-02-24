from data.data import hotels, hotel_activity
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
import plotly


def create_scatter(x, title):
    # Create traces
    return go.Histogram(
        x=x,
        name=title
    )

fig = tools.make_subplots(rows=2, cols=2)


for name, title, i, j in [('star_rating', 'Star Ratings', 1, 1), ('bubble_score', 'Bubble Score', 1, 2),
                    ('review_count', 'Review Count', 2, 1)]:
    fig.append_trace(create_scatter(hotels[name], title), i, j)

p = hotel_activity.groupby(by='hotel_id').size().to_list()
fig.append_trace(go.Histogram(x=p, name='Number of Events'), 2, 2)

