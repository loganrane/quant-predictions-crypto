import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

import plotly.express as px
import plotly.graph_objects as go

from datetime import date

import pandas as pd
import requests
import calendar

from fetch_data import *
from model import quantPredictPrices

# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
app = dash.Dash("Quant Predictions", external_stylesheets=[dbc.themes.LUX])


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "27rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


sidebar = html.Div(
    [
        html.H2("Quant Crypto", className="display-5"),
        html.H2("Forecasting", className="display-5"),
        html.Hr(),
        html.P(
            "A quant prediction app that uses machine learning to predict future prices of crypto currency.", className="lead"
        ),

        # Input the code
        dbc.Card([
            dbc.CardHeader([
                html.H5('Input Crypto Code: '),
            ]),
            dbc.CardBody([
                dbc.InputGroup([
                    dbc.Input(placeholder='bitcoin', id='code'),
                    dbc.InputGroupAddon(
                        dbc.Button('Submit', color='dark', id='code-submit', n_clicks=0), addon_type='append'
                    )
                ])
            ]),
        ], className='mt-2'),

        dbc.Card([
            dbc.CardHeader([
                html.H5('Number of days to forecast: '),
            ]),
            dbc.CardBody([
                dbc.InputGroup([
                    dbc.Input(placeholder='1 - 30', id='days', type='number'),
                    dbc.InputGroupAddon(
                        dbc.Button('Submit', color='dark', id='forecast-submit', n_clicks=0), addon_type='append'
                    )
                ])
            ]),
        ], className='mt-2'),
    ],
    style=SIDEBAR_STYLE,
)


content = html.Div(
    [
        dbc.Row([
            dcc.Graph(id='prices-graph'),
        ]), 

        dbc.Row([
            dcc.Graph(id='indicators-graph'),
        ]), 
    ],
    id='page_content', style=CONTENT_STYLE)

# Cache divs
prices_cache = html.Div([], id='prices-data-cache', hidden=True)
ohlc_cache = html.Div([], id='ohlc-data-cache', hidden=True)

# app.layout = html.Div([dcc.Location(id='url'), sidebar, content])
app.layout = html.Div([sidebar, content])

# First goal -> call back banao for both the charts -> prices and moving average + candles
@app.callback(
    Output('prices-graph', 'figure'),
    Output('prices-data-cache', 'children'),
    Output('ohlc-data-cache', 'children'),
    Input('code', 'value'),
    Input('code-submit', 'n_clicks'),
)
def updateOriginalGraph(id_, clicks):
    # Fetch cleaned data
    prices_data = fetchPriceData(id=id_)
    ohlc_data = fetchCandleData(id=id_)

    # Cache the data to store into a div so that we dont have to the API again
    prices_cache_json = prices_data.to_json()
    ohlc_cache_json = ohlc_data.to_json()

    # Now display the graph

def updatePredictedGraph():
    pass

if __name__ == '__main__':
    app.run_server(debug=True)
