import pandas as pd
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, GRU
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam, SGD

import xgboost as xgb


def trainModel(prices_data):
    """Train the model on historical data

    Args:
        prices_data (pandas dataframe object): prices _data

    Returns:
        model: XGBRegressor model trained on live data
    """
    X_train = clean.drop(['prices'], axis=1)
    y_train = clean['prices'].copy()

    # Make the model on given parameters
    parameters = {'gamma':0.01, 'learning_rate':0.05, 'max_depth':8, 'n_estimators':400}
    model = xgb.XGBRegressor(**parameters, objective='reg:squarederror')
    # Train model
    model.fit(X_train, y_train, verbose=False)

    return model