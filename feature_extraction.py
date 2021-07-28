import pandas as pd

def calculateRSI(prices_data, n=14):
    """Calculate the Relative Strength Index of an asset.

    Args:
        prices_data (pandas dataframe object): prices data
        n (int, optional): number of . Defaults to 14.
    Return:
        rsi (pandas series object): relative strength index
    """
    price = prices_data['prices']
    delta = price.diff()
    delta = delta[1:]

    prices_up = delta.copy()
    prices_up[prices_up < 0] = 0
    prices_down = delta.copy()
    prices_down[prices_down > 0] = 0

    roll_up = prices_up.rolling(n).mean()
    roll_down = prices_down.abs().rolling(n).mean()

    relative_strength = roll_up / roll_down
    rsi = 100.0 - (100.0 / (1.0 + relative_strength))

    return rsi


def calculateMACD(prices_data):
    """Calculate the MACD of EMA12 and EMA26 of an asset

    Args:
        prices_data (dataframe): prices data

    Returns:
        macd (pandas series object): macd of the asset
        macd_signal (pandas series object): macd signal of the asset
    """
    ema12 = pd.Series(prices_data['prices'].ewm(
        span=12, min_periods=12).mean())
    ema26 = pd.Series(prices_data['prices'].ewm(
        span=26, min_periods=26).mean())

    macd = pd.Series(ema12 - ema26)
    macd_signal = pd.Series(macd.ewm(span=9, min_periods=9).mean())

    return macd, macd_signal