import pandas.io.sql as pandas_sql
from pandas import DataFrame
import urllib3
import json
import numpy as np
import pandas as pd

from datetime import timedelta, date
import datetime
from calendar import monthrange
import copy
import pandas as pd

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
        'UNIT_NAME', 'STAT_NAME',  'STAT_CODE',  'ITEM_CODE1', 'ITEM_CODE2', 'ITEM_CODE3',
        'ITEM_NAME1', 'ITEM_NAME2', 'ITEM_NAME3', 'DATA_VALUE', 'TIME'
    ]

COLUMN_TYPE_MAPPER = {
    'UNIT_NAME': 'str',
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


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


# Column Mapping
arr_columns = get_column_list()
dict_columns_type = get_column_types()

if __name__ == '__main__':
    url = "http://ecos.bok.or.kr/api/StatisticSearch/{}/json/kr/1/50000/I10Y014/MM/19600101/20201231/US".format(
        api_key)

    http = urllib3.PoolManager()
    ret = http.request("GET", url, headers={'Content-Type': 'application/json'})

    str_response = ret.data.decode('utf-8')
    dict_data = json.loads(str_response)
    arr_data = dict_data['StatisticSearch']['row']

    # [{}, {}, {} ] -> [ [] [] [] [] ...]  변환 작업
    data_for_insert = [[dict_data[column_nm] for column_nm in arr_columns] for dict_data in arr_data]

    df_loan_rate_insert = DataFrame(data_for_insert, columns=arr_columns)

    # '202004' 같은 형태로 오는 데이터를 datetime.date 형태로 변환한 후에 넘겨주기
    dateformat = '%Y%m'
    df_loan_rate_insert['TIME'] = df_loan_rate_insert.TIME.map(
        lambda x: datetime.datetime.strptime(x, dateformat).date()
    )
    df_loan_rate_insert = df_loan_rate_insert.astype(dtype=dict_columns_type)

    df_loan_rate_insert.to_sql(name='loan_rate_usa',
                               con=alchemy_conn,
                               index=False,
                               index_label='TIME',
                               if_exists='replace',  # {'fail', 'replace', 'append'}, default : fail
                               schema='ec2_web_stockdata')

    # -- select database insert result
    df_loan_rate = pandas_sql.read_sql_query("select * from loan_rate_usa", alchemy_conn)
    print("database result ::: loan_rate_usa")
    print(df_loan_rate)

    df_alternative = DataFrame(columns=arr_columns)
    df_alternative = df_alternative.astype(dtype=dict_columns_type)

    for i, row in df_loan_rate.iterrows():
        dt_start_time = row['TIME']
        dt_start_len = monthrange(dt_start_time.year, dt_start_time.month)
        dt_end_time = dt_start_time + timedelta(dt_start_len[1])

        for date_string in daterange(dt_start_time, dt_end_time):
            dt_date = date_string.date()
            dt_day = dt_date.day

            if dt_day == 1:
                row['TIME'] = dt_date
            else:
                series_temp = pd.Series(row.values, index=arr_columns)
                series_temp['TIME'] = dt_date
                df_as_row = DataFrame([series_temp])
                df_alternative = pd.concat([df_as_row, df_alternative], ignore_index=True)

    print("####### #######")
    print(df_alternative)
    df_alternative.to_sql(name='loan_rate_usa',
                               con=alchemy_conn,
                               index=False,
                               index_label='TIME',
                               if_exists='append',  # {'fail', 'replace', 'append'}, default : fail
                               schema='ec2_web_stockdata')
