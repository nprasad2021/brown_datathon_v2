import pandas as pd
import plotly.graph_objs as go
import plotly

corr = pd.read_csv(r'C:\Users\Isaiah Nields\Documents\GitHub\brown_datathon\data\processed_data_corr.csv')

trace = go.Heatmap(z=corr,
                   x=corr.columns,
                   y=corr.columns)

layout = go.Layout(
        autosize=True,
        title='Correlation Heatmap',
        titlefont=dict(size=16),
    )

graph = go.Figure(data=[trace], layout=layout)