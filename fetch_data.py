from pycoingecko import CoinGeckoAPI
import time
import datetime
from datetime import datetime as dt
import pandas as pd

# CoinGeckoAPI - https://www.coingecko.com/api/docs/v3
# CoinGeckoAPI wrapper -https://github.com/man-c/pycoingecko
cg = CoinGeckoAPI()

def convertUnixToUTC(data):
    """Convert UNIX time format to UTC time format"""
    # Check if returned data has miliseconds
    if data >= 5000000000:
        data = data/1000

    return dt.utcfromtimestamp(data).strftime("%Y-%m-%d %H:%M:%S")


def convertUTCtoUnix(data):
    """Convert UTC time format to UNIX time format"""
    return time.mktime(data.timetuple())


def fetchCandleData(id='bitcoin', vs_currency='usd', days=30):
    """Generate the OHLC data for a single coin.
       (1/7/14/30/90/180/365/max)
       Candle's body:
       1 - 2 days: 30 minutes
       3 - 30 days: 4 hours
       31 and before: 4 days
    Args:
        id (str, optional): Coin ID. Defaults to 'bitcoin'.
        vs_currency (str, optional): Against usd/eur/inr. Defaults to 'usd'.
        days (int, optional): Historical data for number of days. Defaults to 30.
    Returns:
        df(pandas dataframe): OHLC data
    """

    data = cg.get_coin_ohlc_by_id(id=id, vs_currency=vs_currency, days=days)
    df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close'])

    # Convert timestamp to UTC
    df['time'] = df['time'].apply(convertUnixToUTC)

    return df


def fetchPriceData(start_date, id='bitcoin', vs_currency='usd'):
    """Fetch the price and market cap data of a coin
        1 day from query time = 5 minute interval data
        1 - 90 days from query time = hourly data
        above 90 days from query time = daily data (00:00 UTC)
    Args:
        start_date (datetime): Start date of the query
        id (str, optional): Coin ID. Defaults to 'bitcoin'.
        vs_currency (str, optional): Against usd/eur/inr. Defaults to 'usd'.

    Returns:
        df(pandas dataframe): Price data
    """
    # Set date time (from -> to)
    query = start_date
    today = datetime.datetime.now()

    unix_query = time.mktime(query.timetuple())
    unix_today = time.mktime(today.timetuple())

    data = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='usd',
                                                from_timestamp=unix_query, to_timestamp=unix_today)
    # Convert to dataframe
    df = pd.DataFrame(data)

    # Get time stamps
    time_stamp = df.iloc[:, 0]
    time_stamp = time_stamp.apply(lambda x: x[0])

    # Remove time frame from each column (given by API by default)
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x[1])

    # Add timestamp to dataframe and convert to UTC format
    df['time'] = time_stamp
    df['time'] = df['time'].apply(convertUnixToUTC)

    return df

