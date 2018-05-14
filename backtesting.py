# -*- coding: UTF-8 -*-
"""
Name: backtesting.py
Author: Qi Yu
Date: 2018-04-18
Information: use for backtesting, read PDF for more information

"""


import pandas as pd
import numpy as np


def backtest(stock_data, buy, sell):
    """ backtesting
        由于没有大盘数据，使用一直持有该股票的收益曲线作为基准收益曲线

    Args:
        stock_data: stock data, type=pandas.Dataframe, ['id', 'date', 'close']
        buy: whether to buy, np.array
        sell: whether to sell, np.array

    Returns:
        backtest_result: backtesting result, type=pandas.Dataframe, ['date', 'income_rate', 'income_rate_base']
    """

    funds = 10000000.0
    shares = 0.0
    income_rate = np.zeros((buy.shape[0], ))
    income_rate_base = np.zeros((buy.shape[0], ))
    shares_base = funds / stock_data.loc[0]['close']

    for index in range(1, buy.shape[0]):
        if sell[index-1] == 1 and shares > 0:
            funds = shares * stock_data.loc[index]['close']     # if n-1 day's sell signal appear, use n day's close_price to sell stocks
            shares = 0
        elif buy[index-1] == 1 and funds > 0:
            shares = funds / stock_data.loc[index]['close']     # if n-1 day's buy signal appear, use n day's close_price to purchase stocks
            funds = 0
        income_rate[index] = (funds + shares * stock_data.loc[index]['close']) / 10000000.0 - 1
        income_rate_base[index] = shares_base * stock_data.loc[index]['close'] / 10000000.0 - 1

    backtest_result = pd.DataFrame()
    backtest_result['date'] = stock_data['date'].copy()
    backtest_result['income_rate'] = income_rate
    backtest_result['income_rate_base'] = income_rate_base
    backtest_result = backtest_result.set_index('date')

    return backtest_result




