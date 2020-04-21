#-*- coding:utf-8 -*-

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
from url_builder.korbank.parameters import kospi_kwargs, \
                                            corporate_loan_kwargs, \
                                            household_loan_kwargs, \
                                            exchange_rate_dollar_kwargs, \
                                            loan_usa_rate_kwargs, \
                                            loan_kor_rate_kwargs

mysql_dev = {
    'host': 'localhost',
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
    'TIME': 'str'
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


arr_columns = get_column_list()
dict_columns_type = get_column_types()


def get_korbank_result(_url, str_date_type):
    http = urllib3.PoolManager()
    ret = http.request("GET", _url, headers={'Content-Type': 'application/json'})

    str_response = ret.data.decode('utf-8')
    dict_data = json.loads(str_response)

    if str_date_type == DD:
        rest_data = dict_data['StatisticSearch']['row']

    else:
        # str_date_type == MM
        rest_data = dict_data['StatisticSearch']['row']

        # for i, row in enumerate(rest_data):
        for i in range(len(rest_data)):
            row = rest_data[i]
            s_start_date = row['TIME']

            if type(s_start_date) == datetime.datetime:
                dt_start_time = datetime.datetime.combine(s_start_date.today(), datetime.datetime.min.time())
            else:
                dt_start_time = datetime.datetime.strptime(s_start_date, '%Y%m')

            dt_start_len = monthrange(dt_start_time.year, dt_start_time.month)
            dt_end_time = dt_start_time + timedelta(dt_start_len[1])
            # dt_end_time = datetime.datetime.strptime(dt_start_time.date(), dt_end_time)

            for date_string in daterange(dt_start_time, dt_end_time):
                c_data = copy.copy(row)
                c_data['TIME'] = date_string
                rest_data.insert(i, c_data)
                # rest_data[i].append(c_data)

    return rest_data


def df_to_sql(rest_data, table_name):
    # [{}, {}, {} ] -> [ [] [] [] [] ...]  변환 작업
    data_for_insert = [[dict_data[column_nm] for column_nm in arr_columns] for dict_data in rest_data]

    df_insert = DataFrame(data_for_insert, columns=arr_columns)
    df_insert = df_insert.astype(dtype=dict_columns_type)

    # -- database insert
    df_insert.to_sql(name=table_name,
                     con=alchemy_conn,
                     index=False,
                     if_exists='replace',   # {'fail', 'replace', 'append'}, default : fail
                     schema='ec2_web_stockdata')

    # -- select database insert result
    df_select = pandas_sql.read_sql_query("select * from {}".format(table_name), alchemy_conn)
    print("database result ::: {}".format(table_name))
    print(df_select)


# https://stackoverflow.com/questions/8855183/strangeness-with-a-decorator
def korbank_url(insert_function):
    url_manager = UrlManager()

    def wrapper(*args, **kwargs):
        url_manager \
            .add_api_key(api_key) \
            .add_from(kwargs['from']) \
            .add_to(kwargs['to']) \
            .add_item_code1(kwargs['item_code1']) \
            .add_search_type(kwargs['search_type']) \
            .add_start_date(kwargs['start_date']) \
            .add_end_date(kwargs['end_date']) \
            .add_item_code2(kwargs['item_code2'])

        url = url_manager.build_url()
        insert_function(url)

    return wrapper


# 1) kospi
@korbank_url
def kospi_day_insert(url):
    df_to_sql(get_korbank_result(url, DD), 'kospi_day')


# 2) 기업대출
@korbank_url
def corporate_insert(url):
    df_to_sql(get_korbank_result(url, DD), 'loan_corporate_month')


# 3) 가계 대출
@korbank_url
def household_loan_month(url):
    df_to_sql(get_korbank_result(url, DD), 'loan_household_month')


# 4) 환율
@korbank_url
def exchange_rate_dollar_day(url):
    df_to_sql(get_korbank_result(url, DD), 'exchange_rate_dollar_day')


# 5) 중앙은행 금리 (미국)
@korbank_url
def loan_usa_month(url):
    df_to_sql(get_korbank_result(url, MM), 'loan_rate_usa')


# 6) 중앙은행 금리 (미국)
@korbank_url
def loan_kor_month(url):
    df_to_sql(get_korbank_result(url, MM), 'loan_rate_kor')


if __name__ == '__main__':
    kospi_day_insert(**kospi_kwargs)
    corporate_insert(**corporate_loan_kwargs)
    household_loan_month(**household_loan_kwargs)
    exchange_rate_dollar_day(**exchange_rate_dollar_kwargs)
    loan_usa_month(**loan_usa_rate_kwargs)
    loan_kor_month(**loan_kor_rate_kwargs)
