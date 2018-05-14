# -*- coding: UTF-8 -*-
"""
Name: main.py
Author: Qi Yu
Date: 2018-04-18
Information: 'main' of whole program, read PDF for more information

"""

import dataLoad
import dataProcess
import judge
import drawCurves
import backtesting

# 1.remove old database named 'guoshi' if exist, and create a new database named 'guoshi'
# 2.create table named 'all_data'
dataLoad.create_mysql()

# 3.read csv from csv_file_path
date_list, close_list = dataLoad.read_csv("./002055.csv")

# 4.insert data into database
for ii in range(len(date_list)):
    dataLoad.insert_mysql(ii, date_list[ii], close_list[ii])

# 5.query all data from database
stock_data = dataLoad.query_mysql()
# print(stock_data)

# 6.calculate RSI curve
short_RSI = dataProcess.calculate_RSI(stock_data, 6)
long_RSI = dataProcess.calculate_RSI(stock_data, 12)

# 7.calculate BOLL curve
BOLL = dataProcess.calculate_BOLL(stock_data, 20, 2)

# 8.judge whether any condition is satisfied, give 'buy' / 'sell' / 'warning' signals
buy, warning, sell = judge.judge(BOLL, short_RSI, long_RSI, start_index=20)

# 9.backtesting
backtest_result = backtesting.backtest(stock_data, buy, sell)

# 10.draw BOLL curve, RSI curve, trade_signals curve and backtesting curve
drawCurves.draw_BOLL_and_RSI(stock_data, BOLL, short_RSI, long_RSI)
drawCurves.draw_trade_signals(stock_data, BOLL, short_RSI, long_RSI, buy, warning, sell)
drawCurves.draw_backtesting(backtest_result)

