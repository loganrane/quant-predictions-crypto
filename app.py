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

# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
app = dash.Dash("Quant Predictions", external_stylesheets=[dbc.themes.LUX])

# Layout and Components of the app
app.layout = dbc.Container([
    # Dashboard
    dbc.Col([
        # Header
        dbc.Row([
            dbc.Card([
                dbc.CardHeader([html.H1('~Quant Predictions~')]),
            ], className='mx-3 mt-5')
        ], style={'width': '105'}),

        # Input
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5('Input Crypto Code: '),
                    ]),
                    dbc.CardBody([
                        dbc.Input(
                            placeholder='bitcoin', bs_size='md', className='mb-3', id='code'
                        )
                    ]),
                ], className='mt-2')
            ], width=12)
        ]),

        # Start Date
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5('Start Date'),
                    ]),
                    dbc.CardBody([
                        dcc.DatePickerSingle(
                            id='start-date',
                            date=date(2021, 1, 1),
                            className='mt-2'
                        ),
                    ]),
                ]),
            ]),
        ]),

        # Stock Price and Indicators button
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([

                    ])
                ])
            ], width=6),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([

                    ])
                ])
            ], width=6),
        ]),

        # Forecast input and button
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([

                    ])
                ])
            ], width=6),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([

                    ])
                ])
            ], width=6),
        ]),

    ], width=3),

    # Charts and predictions
    dbc.Col([

    ], width=8)
], fluid=True)


if __name__ == '__main__':
    app.run_server(debug=True)
