import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def candleStickGraph(ohlc_data):
    """Generate the candle stick graph for one month data

    Args:
        ohlc_data (pandas dataframe object): open-high-low-close data

    Returns:
        plotly figure object: candlestick data
    """
    fig = go.Figure(go.Ohlc(x=ohlc_data['time'],
                            open=ohlc_data['open'],
                            high=ohlc_data['high'],
                            low=ohlc_data['low'],
                            close=ohlc_data['close'],
                            name='Price'))

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10),
                      width=900, height=300,
                      title='Candlestick chart for last one month')
    return fig
