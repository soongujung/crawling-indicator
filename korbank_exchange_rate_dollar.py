import pandas.io.sql as pandas_sql
from pandas import DataFrame
import urllib3
import json

from datetime import timedelta, date
import datetime
from calendar import monthrange
import copy

from db_connector.alchemy.connection_manager import ConnectionManager
from url_builder.korbank.urls import UrlManager
from url_builder.korbank.parameters import kospi_kwargs


mysql_dev = {
    'host': '--',
    'dbname': 'ec2_web_stockdata',
    'user': 'admin',
    'password': '--'
}

alchemy_conn = ConnectionManager.create_connection(mysql_dev)

COLUMN_LIST = [
        'STAT_NAME',  'STAT_CODE',  'ITEM_CODE1', 'ITEM_CODE2', 'ITEM_CODE3',
        'ITEM_NAME1', 'ITEM_NAME2', 'ITEM_NAME3', 'DATA_VALUE', 'TIME'
    ]

COLUMN_TYPE_MAPPER = {
    'STAT_NAME': 'str',
    'STAT_CODE': 'str',
    'ITEM_CODE1': 'str',
    'ITEM_CODE2': 'str',
    'ITEM_CODE3': 'str',
    'ITEM_NAME1': 'str',
    'ITEM_NAME2': 'str',
    'ITEM_NAME3': 'str',
    'DATA_VALUE': 'float',
    'TIME': 'datetime64'
}

api_key = '--'
MM = 'MM'
DD = 'DD'


def get_column_list():
    return COLUMN_LIST


def get_column_types():
    return COLUMN_TYPE_MAPPER


# Column Mapping
arr_columns = get_column_list()
dict_columns_type = get_column_types()

if __name__ == '__main__':
    url = "http://ecos.bok.or.kr/api/StatisticSearch/{}/json/kr/1/50000/036Y001/DD/19600101/20201231/0000001".format(
        api_key)

    http = urllib3.PoolManager()
    ret = http.request("GET", url, headers={'Content-Type': 'application/json'})

    str_response = ret.data.decode('utf-8')
    dict_data = json.loads(str_response)
    arr_data = dict_data['StatisticSearch']['row']

    # [{}, {}, {} ] -> [ [] [] [] [] ...]  변환 작업
    data_for_insert = [[dict_data[column_nm] for column_nm in arr_columns] for dict_data in arr_data]

    df_exchange_rate_insert = DataFrame(data_for_insert, columns=arr_columns)
    df_exchange_rate_insert = df_exchange_rate_insert.astype(dtype=dict_columns_type)

    df_exchange_rate_insert.to_sql(name='exchange_rate_dollar_day',
                                   con=alchemy_conn,
                                   index=False,
                                   index_label='TIME',
                                   if_exists='replace',  # {'fail', 'replace', 'append'}, default : fail
                                   schema='ec2_web_stockdata')

    # -- select database insert result
    df_kospi_select = pandas_sql.read_sql_query("select * from exchange_rate_dollar_day", alchemy_conn)
    print("database result ::: exchange_rate_dollar_day")
    print(df_kospi_select)
