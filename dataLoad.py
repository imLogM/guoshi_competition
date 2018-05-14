# -*- coding: UTF-8 -*-
"""
Name: dataLoad.py
Author: Qi Yu
Date: 2018-04-18
Information: read csv file, insert to database and load data from database, read PDF for more information

"""

import csv
import pymysql
import pandas as pd


def read_csv(csv_file_path):
    """ read csv from csv_file_path

    Args:
        csv_file_path: a path like "./002055.csv"

    Returns:
        date_list: list of date
        close_list: list of close price
    """
    date_list = []
    close_list = []
    with open(csv_file_path, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if csv_reader.line_num == 1:  # ignore the first line
                continue
            for ii, data in enumerate(row):  # save useful data to lists
                if ii == 0:
                    date_list.append(data)
                elif ii == 1:
                    close_list.append(data)
                else:
                    continue

    return date_list, close_list


def create_mysql():
    """ 1.remove old database named 'guoshi' if exist, and create a new database named 'guoshi'
        2.create table named 'all_data'
        +-------+-------------+------+-----+---------+-------+
        | Field | Type        | Null | Key | Default | Extra |
        +-------+-------------+------+-----+---------+-------+
        | id    | int(10)     | NO   | PRI | NULL    |       |
        | date  | varchar(20) | YES  |     | NULL    |       |
        | close | float       | YES  |     | NULL    |       |
        +-------+-------------+------+-----+---------+-------+
    """
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='', port=3306, charset='utf8')
    try:
        cursor = db.cursor()
        cursor.execute('show databases')
        rows = cursor.fetchall()
        # print(rows)
        for row in rows:
            tmp = "%2s" % row
            if tmp == 'guoshi':
                cursor.execute('drop database if exists ' + 'guoshi')
        cursor.execute('create database if not exists ' + 'guoshi')
        db.commit()
    except BaseException as e:
        raise e
    finally:
        db.close()

    db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='guoshi', port=3306, charset='utf8')
    try:
        cursor = db.cursor()
        cursor.execute('create table all_data (id int(10) primary key, date DATE, close FLOAT)')
        db.commit()
    except BaseException as e:
        raise e
    finally:
        db.close()


def insert_mysql(id, date, close):
    """ insert data into database
        database:'guoshi', table:'all_data'

     Args:
        id: index of data, 'int'
        date: date, 'string'
        close: close price, 'float'
    """
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='guoshi', port=3306, charset='utf8')
    try:
        cursor = db.cursor()
        cursor.execute('insert into all_data (id, date, close) values (%s, %s, %s)', [id, date, close])
        db.commit()
    except BaseException as e:
        raise e
    finally:
        db.close()


def query_mysql():
    """ query all data from database
        database:'guoshi', table:'all_data'

    Returns:
        stock_data: type=pandas.Dataframe
    """
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='guoshi', port=3306, charset='utf8')
    try:
        stock_data = pd.read_sql('select * from all_data;', con=db)
    except BaseException as e:
        raise e
    finally:
        db.close()

    return stock_data


if __name__ == "__main__":
    """"""
    # create_mysql()
    # date_list, close_list = read_csv("./002055.csv")
    # for ii in range(len(date_list)):
    #     insert_mysql(ii, date_list[ii], close_list[ii])
    # stock_data = query_mysql()
    # print(stock_data)




