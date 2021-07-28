import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from feature_extraction import extractAll


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


def indicatorsGraph(prices_data):
    """Generate the indicators graph for one month

    Args:
        prices_data (pandas dataframe object): prices data

    Returns:
        plotly figure object: technical indicators"""
    times = prices_data['time']
    indicators = extractAll(prices_data)

    indicators['time'] = times

    indicators = indicators.iloc[-(24 * 30):, :]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=indicators['time'], y=indicators['EMA_9'], name='EMA 9'))
    fig.add_trace(go.Scatter(
        x=indicators['time'], y=indicators['SMA_5'], name='SMA 5'))
    fig.add_trace(go.Scatter(
        x=indicators['time'], y=indicators['SMA_10'], name='SMA 10'))
    fig.add_trace(go.Scatter(
        x=indicators['time'], y=indicators['SMA_15'], name='SMA 15'))
    fig.add_trace(go.Scatter(
        x=indicators['time'], y=indicators['SMA_30'], name='SMA 30'))
    fig.add_trace(go.Scatter(
        x=indicators['time'], y=indicators['prices'], name='prices', opacity=0.2))

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10),
                      width=1010, height=300,
                      title='Price data with technical indicators for 30 days')

    return fig


def predictionGraph(prices_data, predicted_data):
    """Plot graph for predicted data

    Args:
        prices_data (pandas dataframe object): prices data
        predicted_data (pandas dataframe object): predicted prices
    Returns:
        plotly figure object: graph"""
    prices_data = prices_data.iloc[-(24*30):, :]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=prices_data['time'], y=prices_data['prices'], name='Real', marker_color='LightSkyBlue'))
    fig.add_trace(go.Scatter(
        x=predicted_data['time'], y=predicted_data['prices'], name='Predicted', marker_color='MediumPurple'))

    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10),
                      width=1010, height=300,
                      title='Prediction of future prices')

    return fig
