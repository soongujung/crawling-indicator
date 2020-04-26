#-*- coding:utf-8 -*-

import pandas.io.sql as pandas_sql
from pandas import DataFrame
import urllib3
import json
from datetime import timedelta, date
import datetime

from db_connector.alchemy.connection_manager import ConnectionManager

mysql_dev = {
    'host': '--',
    'dbname': 'ec2_web_stockdata',
    'user': 'admin',
    'password': '--'
}

alchemy_conn = ConnectionManager.create_connection(mysql_dev)

# column
# v_yyyy, v_mm, v_dd, v_date
arr_columns = ['yyyy', 'mm', 'dd', 'yyyymmdd']
type_mapper = {
    'yyyy': 'str',
    'mm': 'str',
    'dd': 'str',
    'yyyymmdd': 'datetime64',
}


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = date(1970, 1, 1)
end_date = date(2040, 12, 31)

data_insert_list = []
for date_string in daterange(start_date, end_date):
    print(date_string.strftime("%Y%m%d"))

    date_yy = date_string.strftime("%Y")
    date_mm = date_string.strftime("%m")
    date_dd = date_string.strftime("%d")
    # date_all = date_string.strftime("%Y%m%d")

    # yyyymmdd = datetime.datetime.strptime(date_string.strftime("%Y%m%d"), '%Y%m%d')
    # date_all = yyyymmdd

    yyyymmdd = date_string

    # data_insert = [date_yy, date_mm, date_dd, date_all]
    dict_insert = {
        'yyyy': date_yy,
        'mm': date_mm,
        'dd': date_dd,
        'yyyymmdd': yyyymmdd
    }
    data_insert_list.append(dict_insert)

df_insert = DataFrame(data_insert_list, columns=arr_columns)
df_insert = df_insert.astype(dtype=type_mapper)

df_insert.to_sql(name="date_axis_dd",
                 con=alchemy_conn,
                 index=False,
                 if_exists="replace",
                 schema="ec2_web_stockdata")
