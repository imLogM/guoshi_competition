# -*- coding: UTF-8 -*-
"""
Name: dataProcess.py
Author: Qi Yu
Date: 2018-04-18
Information: get RSI / BOLL, read PDF for more information

"""


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdate


def calculate_RSI(stock_data, N):
    """ calculate RSI curve

    Args:
        stock_data: stock data, type=pandas.Dataframe, ['id', 'date', 'close']
        N: number of days

    Returns:
        RSI: RSI, type=pandas.Dataframe,
        ['id', 'date', 'close', 'delta', 'up', 'down', 'roll_up', 'roll_down', 'RSI'],
        you can get long-term RSI and short-term RSI by changing N
    """

    RSI = stock_data.copy()

    RSI['delta'] = RSI['close'] - RSI['close'].shift(1)

    up = RSI['delta'].copy()
    up[up < 0] = 0
    RSI['up'] = up

    down = RSI['delta'].copy()
    down[down > 0] = 0
    RSI['down'] = down

    roll_up = pd.Series.ewm(up, span=N).mean()
    roll_down = pd.Series.ewm(down.abs(), span=N).mean()
    RSI['roll_up '] = roll_up
    RSI['roll_down'] = roll_down

    RS = roll_up / roll_down
    RSI['RSI'] = 100.0 - (100.0 / (1.0 + RS))

    return RSI


def calculate_BOLL(stock_data, N, M=2):
    """ calculate BOLL curve

    Args:
        stock_data: stock data, type=pandas.Dataframe, ['id', 'date', 'close']
        N: number of days
        M: magnification, usually M = 2

    Returns:
        BOLL: BOLL, type=pandas.Dataframe,
        ['id', 'date', 'close', 'middle', 'std', 'up', 'down'],
        you can get long-term BOLL and short-term BOLL by changing N
    """
    BOLL = stock_data.copy()

    BOLL['middle'] = pd.Series.rolling(BOLL['close'], window=N).mean()
    BOLL['std'] = pd.Series.rolling(BOLL['close'], window=N).std()

    BOLL['up'] = BOLL['middle'] + M * BOLL['std']
    BOLL['down'] = BOLL['middle'] - M * BOLL['std']

    return BOLL


if __name__ == "__main__":
    """"""


