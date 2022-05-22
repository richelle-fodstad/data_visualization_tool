
from dash import Dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv('fires_cleaned.csv')

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Dash by Plotly: Forest Fires in Turkey"

bar_fig = px.bar(data, x='Year', y='Number of Fires', title='Number of Forest Fires in Turkey per Year')
line_fig = px.line(data, x='Year', y='Number of Fires', title='Number of Forest Fires in Turkey per Year')
pie_fig = px.pie(data, names='Status', title='Types of Forest Fires in Turkey')
histogram_fig = px.histogram(data, x='Hectares', title='Distribution of Frequency of Forest Fires in Turkey by Size (hectares)')

app.layout = html.Div(
	children=[
        html.Div(
            children=[
                html.P(children="📊", className="header-emoji"),
                html.H1(
                    children="Dash by Plotly", className="header-title"
                ),
                html.P(
                    children="Data visualisation of forest fires in Turkey from 1988 to 2020.  An example of a dashboard visualising a relatively small data set.",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Status", className="menu-title"),
                        dcc.Dropdown(
                            id="status-filter",
                            options=[
                                {"label": Status, "value": Status}
                                for Status in np.sort(data.Status.unique())
                            ],
                            value="Total",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Year Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="year-range",
                            min_date_allowed=data.Year.min(),
                            max_date_allowed=data.Year.max(),
                            start_date=data.Year.min(),
                            end_date=data.Year.max(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id='bar-chart',
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id='line-chart',
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id='pie-chart',
                        figure=pie_fig
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id='histogram-chart',
                        figure=histogram_fig
                    ),
                    className="card",
                ),
            ],
            className="wrapper"
        ),
    ]
)

@app.callback(
    [Output("bar-chart", "figure"), Output("line-chart", "figure")],
    [
        Input("status-filter", "value"),
        Input("year-range", "start_date"),
        Input("year-range", "end_date"),
    ],
)
def update_charts(Status, start_date, end_date):
    mask = (
        (data.Status == Status)
        & (data.Year >= start_date)
        & (data.Year <= end_date)
    )
    filtered_data = data.loc[mask, :]
    bar_chart = px.bar(filtered_data, x='Year', y='Number of Fires', title='Number of Forest Fires in Turkey per Year')
    line_chart = px.line(filtered_data, x='Year', y='Number of Fires', title='Number of Forest Fires in Turkey per Year')
 
    return bar_chart, line_chart

if __name__ == '__main__':
	app.run_server(debug=True)
