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
app = dash(__name__, external_stylesheets=[dbc.themes.LUX]))





if __name__ == '__main__':
    app.run_server(debug=True)
