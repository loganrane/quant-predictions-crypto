import pandas as pd
import numpy as np

import datetime
import xgboost as xgb
from feature_extraction import *


def trainModel(prices_data):
    """Train the model on historical data

    Args:
        prices_data (pandas dataframe object): prices _data

    Returns:
        model: XGBRegressor model trained on live data
    """
    X_train = prices_data.drop(['prices'], axis=1)
    y_train = prices_data['prices'].copy()

    # Make the model on given parameters
    parameters = {'gamma': 0.01, 'learning_rate': 0.05,
                  'max_depth': 8, 'n_estimators': 400}
    model = xgb.XGBRegressor(**parameters, objective='reg:squarederror')
    # Train model
    model.fit(X_train, y_train, verbose=False)

    return model


def quantPredictPrices(prices_data, num_days):
    """Predict prices based on historical data

    Args:
        prices_data (pandas dataframe object): prices data
        num_ticks (int): number of days in future to predict the results
    Returns:
        (pandas dataframe object): dataframe with future predicted prices
    """
    # Store time for plotting
    latest_time = prices_data.iloc[-1]['time']
    future_times = []
    predictions = pd.DataFrame(columns=[
                               'prices', 'EMA_9', 'SMA_5', 'SMA_10', 'SMA_15', 'SMA_30', 'RSI',	'MACD',	'MACD_signal'])

    prediction_data = extractAll(prices_data)
    model = trainModel(prediction_data)
    # Now lets do predictions

    latest_ticks = prediction_data.iloc[-14:, :]

    # Get the data for that many days (6 * num_days as we have 4-hour ticks data)
    for i in range(1, num_days*6 + 1):
        X = latest_ticks.drop(['prices'], axis=1)
        y = latest_ticks.iloc[-1]['prices']

        features = X.iloc[-1:, :]
        predict_features = np.array(features).reshape(-1, 8)

        # Get the next price
        price = model.predict(predict_features)[0]

        # Calculate other features based on todays price
        ema9 = (y * (1 - 2/(9 + 1)) + price * (2/(9 + 1)))
        sma5 = ((features['SMA_5'].values[0] * 4 + price) / 5)
        sma10 = ((features['SMA_10'].values[0] * 9 + price) / 10)
        sma15 = ((features['SMA_15'].values[0] * 14 + price) / 15)
        sma30 = ((features['SMA_30'].values[0] * 29 + price) / 30)

        rsi = calculateRSI(
            prices_data=latest_ticks.iloc[-13:, :], today_price=price).iloc[-1]

        macd = (sma30 - sma15)
        macd_signal = (features['MACD_signal'].values[0]
                       * (1 - 2/(9+1)) + macd * (2/(9+1)))

        latest_ticks.loc[len(latest_ticks)] = [price, ema9,
                                               sma5, sma10, sma15, sma30, rsi, macd, macd_signal]
        predictions.loc[len(predictions)] = [price, ema9,
                                             sma5, sma10, sma15, sma30, rsi, macd, macd_signal]
        future_times.append(latest_time + datetime.timedelta(hours=i))

    # Add date and time
    predictions['time'] = pd.Series(future_times)
    predictions['date'] = predictions['time'].dt.date

    return predictions
