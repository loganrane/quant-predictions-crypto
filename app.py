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
                dbc.CardHeader([html.H1('Quant Crypto Forecasting')]),
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
                        dbc.InputGroup([
                            dbc.Input(placeholder='bitcoin', id='code'),
                            dbc.InputGroupAddon(
                                dbc.Button('Submit', color='dark', id='code-submit', n_clicks=0), addon_type='append'
                            )
                        ])
                    ]),
                ], className='mt-2')
            ], width=12)
        ], className='my-5'),

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
        ], className='my-5'),

        # Stock Price and Indicators button
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.Col([
                        dbc.Row([
                            dbc.Button('Price', color='dark',
                                       style={'width': '121px'}),
                            dbc.Button('Indicators', color='dark'),

                        ], justify='around', style={'margin-top': '10px', 'margin-bottom': '15px'}),

                        dbc.Row([
                            dbc.InputGroup([
                                dbc.Input(id='days', placeholder='60',
                                          type='number'),
                                dbc.InputGroupAddon(
                                    dbc.Button('Forecast', color='dark', id='forecast-submit', n_clicks=0), addon_type='append'
                                )
                            ])
                        ], justify='center')
                    ], width=11, className='ml-2 my-2')
                ])
            ], width=12),
        ], justify='center', className='my-5'),

    ], width=3),

    # Charts and predictions
    dbc.Col([

    ], width=8)
], fluid=True)


if __name__ == '__main__':
    app.run_server(debug=True)
