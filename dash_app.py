
from dash import Dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

data = pd.read_csv('fires.csv')

app = Dash(__name__)

bar_fig = px.bar(data, x='year', y='#fires', title='Number of Forest Fires in Turkey per Year')
pie_fig = px.pie(data, names='status', title='Types of Forest Fires in Turkey')
line_fig = px.line(data, x='year', y='#fires', title='Size of Forest Fires in Turkey per Year')
histogram_fig = px.histogram(data, x='hectares', title='Distribution of Frequency of Forest Fires in Turkey by Size (hectares)')

app.layout = html.Div(
	children=[
		html.H1(children='Dash',),
		html.P(
			children='Data visualization of forest fires in Turkey from 1988 to 2020',
        ),
        dcc.Graph(
            id='bar-chart',
            figure=bar_fig
        ),
        dcc.Graph(
            id='pie-chart',
            figure=pie_fig
        ),
        dcc.Graph(
            id='line-chart',
            figure=line_fig
        ),
        dcc.Graph(
            id='histogram-chart',
            figure=histogram_fig
        ),
    ]
)

if __name__ == '__main__':
	app.run_server(debug=True)