# -*- coding: UTF-8 -*-
"""
Name: drawCurves.py
Author: Qi Yu
Date: 2018-04-18
Information: draw BOLL curve, RSI curve, trade_signals curve and backtesting curve, read PDF for more information

"""

import pandas as pd
import matplotlib.pyplot as plt


def draw_BOLL_and_RSI(stock_data, BOLL, short_RSI, long_RSI):
    """ draw BOLL curve and RSI curve

    Args:
        stock_data: stock data, type=pandas.Dataframe, ['id', 'date', 'close']
        RSI: RSI, type=pandas.Dataframe, ['id', 'date', 'close', 'delta', 'up', 'down', 'roll_up', 'roll_down', 'RSI']
        BOLL: BOLL, type=pandas.Dataframe, ['id', 'date', 'close', 'middle', 'std', 'up', 'down']
    """
    BOLL_ready_to_draw = pd.DataFrame()
    BOLL_ready_to_draw['date'] = stock_data['date'].copy()
    BOLL_ready_to_draw['close_price'] = stock_data['close'].copy()
    BOLL_ready_to_draw['BOLL_middle'] = BOLL['middle'].copy()
    BOLL_ready_to_draw['BOLL_up'] = BOLL['up'].copy()
    BOLL_ready_to_draw['BOLL_down'] = BOLL['down'].copy()
    BOLL_ready_to_draw = BOLL_ready_to_draw.set_index('date')

    RSI_ready_to_draw = pd.DataFrame()
    RSI_ready_to_draw['date'] = stock_data['date'].copy()
    RSI_ready_to_draw['short_RSI'] = short_RSI['RSI'].copy()
    RSI_ready_to_draw['long_RSI'] = long_RSI['RSI'].copy()
    RSI_ready_to_draw = RSI_ready_to_draw.set_index('date')

    fig1 = plt.figure()
    ax2 = plt.subplot(212)
    ax1 = plt.subplot(211, sharex=ax2)
    BOLL_ready_to_draw.plot(title='BOLL', rot=45, ax=ax1, sharex=ax2, alpha=0.8)
    RSI_ready_to_draw.plot(title='RSI', rot=45, ax=ax2, alpha=0.8)
    plt.show()


def draw_trade_signals(stock_data, BOLL, short_RSI, long_RSI, buy, warning, sell):
    """ draw BOLL curve and trade signals

    Args:
        stock_data: stock data, type=pandas.Dataframe, ['id', 'date', 'close']
        RSI: RSI, type=pandas.Dataframe, ['id', 'date', 'close', 'delta', 'up', 'down', 'roll_up', 'roll_down', 'RSI']
        BOLL: BOLL, type=pandas.Dataframe, ['id', 'date', 'close', 'middle', 'std', 'up', 'down']
    """
    BOLL_ready_to_draw = pd.DataFrame()
    BOLL_ready_to_draw['date'] = stock_data['date'].copy()
    BOLL_ready_to_draw['close_price'] = stock_data['close'].copy()
    BOLL_ready_to_draw['BOLL_middle'] = BOLL['middle'].copy()
    BOLL_ready_to_draw['BOLL_up'] = BOLL['up'].copy()
    BOLL_ready_to_draw['BOLL_down'] = BOLL['down'].copy()
    BOLL_ready_to_draw['buy'] = buy * 30
    BOLL_ready_to_draw['warning'] = warning * 20
    BOLL_ready_to_draw['sell'] = sell * 10
    BOLL_ready_to_draw = BOLL_ready_to_draw.set_index('date')

    RSI_ready_to_draw = pd.DataFrame()
    RSI_ready_to_draw['date'] = stock_data['date'].copy()
    RSI_ready_to_draw['short_RSI'] = short_RSI['RSI'].copy()
    RSI_ready_to_draw['long_RSI'] = long_RSI['RSI'].copy()
    RSI_ready_to_draw = RSI_ready_to_draw.set_index('date')

    fig2 = plt.figure()
    ax2 = plt.subplot(212)
    ax1 = plt.subplot(211, sharex=ax2)
    BOLL_ready_to_draw.plot(title='Trade Signals', rot=45, ax=ax1, sharex=ax2, alpha=0.8)
    RSI_ready_to_draw.plot(title='RSI', rot=45, ax=ax2, alpha=0.8)
    plt.show()


def draw_backtesting(backtest_result):
    """ draw backtesting curves

    Args:
        backtest_result: backtesting result, type=pandas.Dataframe, ['date', 'income_rate', 'income_rate_base']
    """
    fig3 = plt.figure()
    ax1 = plt.subplot(111)
    backtest_result.plot(title='Backtesting', rot=45, ax=ax1, alpha=0.8)
    plt.show()

