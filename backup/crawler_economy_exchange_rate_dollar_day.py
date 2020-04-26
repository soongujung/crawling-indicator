#-*- coding:utf-8 -*-

import psycopg2
import pandas.io.sql as pandas_sql
from pandas import DataFrame
from sqlalchemy import create_engine
import urllib3
import json

dict_account = {
    'host': 'localhost',
    'dbname': 'stock_data',
    'user': 'postgres',
    'password': '1234'
}

conn_str = "host='{}' dbname='{}' user={} password={}"\
    .format(
        dict_account['host'],
        dict_account['dbname'],
        dict_account['user'],
        dict_account['password']
    )

alchemy_conn = create_engine(
    "postgresql://{}:{}@localhost:5432/{}"
        .format(
            dict_account['user'],
            dict_account['password'],
            dict_account['dbname']
        )
)

arr_columns = [
        'STAT_NAME',  'STAT_CODE',  'ITEM_CODE1', 'ITEM_CODE2', 'ITEM_CODE3',
        'ITEM_NAME1', 'ITEM_NAME2', 'ITEM_NAME3', 'DATA_VALUE', 'TIME'
    ]


if __name__ == '__main__':
    conn = psycopg2.connect(conn_str)
    cursor = conn.cursor()

    # --  api 크롤링
    url = "http://ecos.bok.or.kr/api/StatisticSearch/[api키]/json/kr/1/5000/036Y001/DD/20140101/20191231/0000001"

    http = urllib3.PoolManager()
    ret = http.request("GET", url, headers={'Content-Type': 'application/json'})

    print("REST API RESULT ===== ")
    str_response = ret.data.decode('utf-8')
    dict_data = json.loads(str_response)
    arr_data = dict_data['StatisticSearch']['row']

    df_exchange_rate_insert = DataFrame(arr_data, columns=arr_columns)
    print('df_kospi_insert : ' + df_exchange_rate_insert)

    # -- database insert/select
    df_exchange_rate_insert.to_sql(name='economy_exchange_rate_dollar_day',
                                   con=alchemy_conn,
                                   index=False,
                                   if_exists='replace',  #{'fail', 'replace', 'append'}, default : fail
                                   schema='public')

    df_exchange_rate = pandas_sql.read_sql_query("select * from economy_exchange_rate_dollar_day", alchemy_conn)
    print("database result ::: stock_kospi_month")
    print(df_exchange_rate)





