import dash
import dash_core_components as dcc
import dash_html_components as html
from app.graphs.recommendation_graph import graph as recommendation
from app.graphs.city_map import graphs as maps
from app.graphs.heatmap import graph as heatmap
from app.graphs.line_plot import graph as line_graph
from app.graphs.histograms import fig as histograms

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='TripAdvisor Dataset: an in-depth exploration'),
    *[dcc.Graph(figure=map, style={'height': '1000px'}, config={'staticPlot': True}) for map in maps],
    dcc.Graph(figure=histograms, style={'height': '1000px'}),
    dcc.Graph(figure=heatmap, style={'height': '1000px'}),
    dcc.Graph(figure=recommendation, style={'height': '700px'}),
    dcc.Graph(figure=line_graph, style={'height': '1000px'})
])


if __name__ == '__main__':
    app.run_server(debug=True)
