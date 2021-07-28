import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

import plotly.express as px
import plotly.graph_objects as go

from datetime import date

import pandas as pd
import requests
import calendar

from fetch_data import *
from model import quantPredictPrices
from make_graph import *

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
                    dbc.Input(placeholder='bitcoin',
                              id='code', value='bitcoin'),
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
                    dbc.Input(placeholder='1 - 30', id='days',
                              type='number', value=5),
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

        # Cache divs
        html.Div([], id='prices-data-cache', hidden=True),
        html.Div([], id='ohlc-data-cache', hidden=True),
        html.Div([], id='print')
    ],
    id='page_content', style=CONTENT_STYLE)


# app.layout = html.Div([dcc.Location(id='url'), sidebar, content])
app.layout = html.Div([sidebar, content])


@app.callback(
    [Output('prices-graph', 'figure'), Output('indicators-graph', 'figure')],
    [Input('code-submit', 'n_clicks'), Input('forecast-submit', 'n_clicks')],
    [State('code', 'value'), State('days', 'value')],
)
def updateOriginalGraph(code, forecast, id_, days):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Fetch cleaned data
    prices_data = fetchPriceData(id=id_)
    ohlc_data = fetchCandleData(id=id_)

    if button_id == 'code-submit':
        graphA, graphB = updateOriginalGraph(prices_data, ohlc_data)
    elif button_id == 'forecast-submit':
        graphA, graphB = updateForecastGraph(prices_data, days)

    return [graphA, graphB]


def updateOriginalGraph(prices_data, ohlc_data):
    # Now display the graph
    candle = candleStickGraph(ohlc_data)
    indicators = indicatorsGraph(prices_data)

    return [candle, indicators]


def updateForecastGraph(prices_data, n_days):
    predicted_data = quantPredictPrices(prices_data, n_days)

    pred = predictionGraph(prices_data, predicted_data)
    indi = indicatorsGraph(prices_data)

    return [pred, indi]


if __name__ == '__main__':
    app.run_server(debug=True)
