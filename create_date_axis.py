#-*- coding:utf-8 -*-

import pandas.io.sql as pandas_sql
from pandas import DataFrame
import urllib3
import json
from datetime import timedelta, date

from db_connector.alchemy.connection_manager import ConnectionManager

mysql_dev = {
    'host': 'localhost',
    'dbname': 'ec2_web_stockdata',
    'user': 'admin',
    'password': '--'
}

alchemy_conn = ConnectionManager.create_connection(mysql_dev)

# column
# v_yyyy, v_mm, v_dd, v_date
arr_columns = ['v_yyyy', 'v_mm', 'v_dd', 'v_date']
type_mapper = {
    'v_yyyy': 'str',
    'v_mm': 'str',
    'v_dd': 'str',
    'v_date': 'str',
}


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = date(1970, 1, 1)
end_date = date(2040, 12, 31)

for date_string in daterange(start_date, end_date):
    print(date_string.strftime("%Y%m%d"))

    date_yy = date_string.strftime("%Y")
    date_mm = date_string.strftime("%m")
    date_dd = date_string.strftime("%d")
    date_all = date_string.strftime("%Y%m%d")

    # data_insert = [date_yy, date_mm, date_dd, date_all]
    dict_insert = {
        'v_yyyy': date_yy,
        'v_mm': date_mm,
        'v_dd': date_dd,
        'v_date': date_all
    }
    data_insert = [dict_insert]
    df_insert = DataFrame(data_insert, columns=arr_columns)
    df_insert = df_insert.astype(dtype=type_mapper)

    df_insert.to_sql(name="DATE_AXIS_DD",
                     con=alchemy_conn,
                     index=False,
                     if_exists="replace",
                     schema="ec2_web_stockdata")
