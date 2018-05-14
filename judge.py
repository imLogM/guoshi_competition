# -*- coding: UTF-8 -*-
"""
Name: judge.py
Author: Qi Yu
Date: 2018-04-18
Information: judge whether to 'sell' / 'buy' / 'warn', read PDF for more information

"""


import pandas as pd
import numpy as np

days_wait_gold_cross = 10
days_wait_death_cross = 10


def judge(BOLL, short_RSI, long_RSI, start_index):
    """ judge whether any condition is satisfied, give 'buy' / 'sell' / 'warning' signals
        condition_1: short_RSI在50以下，上穿long_RSI，形成金叉，有价格在BOLL_middle上方，买入信号
        condition_2: short_RSI下穿70，下穿long_RSI形成死叉，卖出信号
        condition_3: 价格下穿BOLL中轨，卖出信号
        condition_4: 价格下穿BOLL上轨，卖出警告

    Args:
        RSI: RSI, type=pandas.Dataframe, ['id', 'date', 'close', 'delta', 'up', 'down', 'roll_up', 'roll_down', 'RSI']
        BOLL: BOLL, type=pandas.Dataframe, ['id', 'date', 'close', 'middle', 'std', 'up', 'down']
        start_index: use start_index because the first N days' BOLL and RSI are not make sense

    Returns:
        buy: whether to buy, np.array
        warning: whether to warn, np.array
        sell: whether to sell, np.array
    """
    condition_1 = judge_condition_1(BOLL, short_RSI, long_RSI, start_index)
    condition_2 = judge_condition_2(short_RSI, long_RSI, start_index)
    condition_3 = judge_condition_3(BOLL, start_index)
    condition_4 = judge_condition_4(BOLL, start_index)

    buy = np.zeros((condition_1.shape[0]), )
    sell = np.zeros((condition_1.shape[0]), )
    warning = np.zeros((condition_1.shape[0]), )

    for index in range(start_index, condition_1.shape[0]):
        if condition_2[index] == 1 or condition_3[index] == 1:
            sell[index] = 1
        elif condition_4[index] == 1:
            warning[index] = 1
        elif condition_1[index] == 1:
            buy[index] = 1
        else:
            continue

    return buy, warning, sell


def judge_condition_1(BOLL, short_RSI, long_RSI, start_index):
    """ condition_1: short_RSI在50以下，上穿long_RSI，形成金叉，有价格在BOLL_middle上方，买入信号

    Args:
        RSI: RSI, type=pandas.Dataframe, ['id', 'date', 'close', 'delta', 'up', 'down', 'roll_up', 'roll_down', 'RSI']
        BOLL: BOLL, type=pandas.Dataframe, ['id', 'date', 'close', 'middle', 'std', 'up', 'down']
        start_index: use start_index because the first N days' BOLL and RSI are not make sense

    Returns:
        condition_1: whether satisfy condition_1, np.array
    """
    condition_1 = np.zeros((len(BOLL['id']), ))
    RSI_up_cross = np.zeros((len(BOLL['id']), ))        # monitor whether a up_cross appear

    for index in range(start_index, len(BOLL['id'])):
        if short_RSI.loc[index]['RSI'] < 50 and short_RSI.loc[index - 1]['RSI'] < long_RSI.loc[index - 1]['RSI'] \
                    and short_RSI.loc[index]['RSI'] >= long_RSI.loc[index]['RSI']:  # short_RSI < 50 and up cross
            RSI_up_cross[index] = days_wait_gold_cross
        else:
            if RSI_up_cross[index - 1] >= 1:
                RSI_up_cross[index] = RSI_up_cross[index - 1] - 1          # patient decrease
            else:
                RSI_up_cross[index] = 0

    begin_new_search = False            # when condition is satisified in a period, we will not judge again in same period
    for index in range(start_index, len(BOLL['id'])):
        if RSI_up_cross[index] == days_wait_gold_cross:
            begin_new_search = True
        if begin_new_search and RSI_up_cross[index] >= 1 and BOLL.loc[index]['close'] >= BOLL.loc[index]['middle']:
            condition_1[index] = 1
            begin_new_search = False

    return condition_1


def judge_condition_2(short_RSI, long_RSI, start_index):
    """ condition_2: short_RSI下穿70，下穿long_RSI形成死叉，卖出信号

    Args:
        RSI: RSI, type=pandas.Dataframe, ['id', 'date', 'close', 'delta', 'up', 'down', 'roll_up', 'roll_down', 'RSI']
        BOLL: BOLL, type=pandas.Dataframe, ['id', 'date', 'close', 'middle', 'std', 'up', 'down']
        start_index: use start_index because the first N days' BOLL and RSI are not make sense

    Returns:
        condition_2: whether satisfy condition_2, np.array
    """
    condition_2 = np.zeros((len(short_RSI['id']), ))
    RSI_down_cross = np.zeros((len(short_RSI['id']), ))      # monitor whether a down_cross appear

    for index in range(start_index, len(short_RSI['id'])):
        if short_RSI.loc[index - 1]['RSI'] > 70 and short_RSI.loc[index]['RSI'] <= 70:   # down cross 70
            RSI_down_cross[index] = days_wait_death_cross
        else:
            if RSI_down_cross[index - 1] >= 1:
                RSI_down_cross[index] = RSI_down_cross[index - 1] - 1       # patient decrease
            else:
                RSI_down_cross[index] = 0

    begin_new_search = False            # when condition is satisified in a period, we will not judge again in same period
    for index in range(start_index, len(short_RSI['id'])):
        if RSI_down_cross[index] == days_wait_death_cross:
            begin_new_search = True
        if begin_new_search and RSI_down_cross[index] >= 1:
            if short_RSI.loc[index - 1]['RSI'] > long_RSI.loc[index - 1]['RSI'] \
                    and short_RSI.loc[index]['RSI'] <= long_RSI.loc[index]['RSI']:  # down cross
                condition_2[index] = 1
                begin_new_search = False

    return condition_2


def judge_condition_3(BOLL, start_index):
    """ condition_3: 价格下穿BOLL中轨，卖出信号

    Args:
        BOLL: BOLL, type=pandas.Dataframe, ['id', 'date', 'close', 'middle', 'std', 'up', 'down']
        start_index: use start_index because the first N days' BOLL and RSI are not make sense

    Returns:
        condition_3: whether satisfy condition_3, np.array
    """
    condition_3 = np.zeros((len(BOLL['id']),))
    for index in range(start_index, len(BOLL['id'])):
        if BOLL.loc[index - 1]['close'] > BOLL.loc[index - 1]['middle'] \
                and BOLL.loc[index]['close'] <= BOLL.loc[index]['middle']:
            condition_3[index] = 1

    return condition_3


def judge_condition_4(BOLL, start_index):
    """ condition_4: 价格下穿BOLL上轨，卖出警告

    Args:
        BOLL: BOLL, type=pandas.Dataframe, ['id', 'date', 'close', 'middle', 'std', 'up', 'down']
        start_index: use start_index because the first N days' BOLL and RSI are not make sense

    Returns:
        condition_4: whether satisfy condition_4, np.array
    """
    condition_4 = np.zeros((len(BOLL['id']),))
    for index in range(start_index, len(BOLL['id'])):
        if BOLL.loc[index - 1]['close'] > BOLL.loc[index - 1]['up'] \
                and BOLL.loc[index]['close'] <= BOLL.loc[index]['up']:
            condition_4[index] = 1

    return condition_4


if __name__ == "__main__":
    """"""
