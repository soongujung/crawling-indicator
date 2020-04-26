#-*- coding:utf-8 -*-

import pandas.io.sql as pandas_sql
from pandas import DataFrame
import urllib3
import json

# 사용자 정의 패키지
from credentials.restapi.api_keys import KEY_MAPPINGS
from credentials.connection.database import postgresql_dev
from db_connector.alchemy.connection_manager import ConnectionManager
from mapper.column_mapping.korbank import get_column_list, get_column_types

# Connection 생성
alchemy_conn = ConnectionManager.create_connection(postgresql_dev)

# Column Mapping
arr_columns = get_column_list()
dict_columns_type = get_column_types()

# API KEY
api_key = KEY_MAPPINGS['korbank']

if __name__ == '__main__':

    # --  api 크롤링
    url = "http://ecos.bok.or.kr/api/StatisticSearch/{}/json/kr/1/5000/064Y001/DD/20140101/20191231/0001000".format(api_key)

    http = urllib3.PoolManager()
    ret = http.request("GET", url, headers={'Content-Type': 'application/json'})

    str_response = ret.data.decode('utf-8')
    dict_data = json.loads(str_response)
    arr_data = dict_data['StatisticSearch']['row']

    # [{}, {}, {} ] -> [ [] [] [] [] ...]  변환 작업
    data_for_insert = [[ dict_data[column_nm] for column_nm in arr_columns] for dict_data in arr_data]

    df_kospi_insert = DataFrame(data_for_insert, columns=arr_columns)
    df_kospi_insert = df_kospi_insert.astype(dtype=dict_columns_type)

    # -- database insert
    df_kospi_insert.to_sql(name='stock_kospi_day',
                           con=alchemy_conn,
                           index=False,
                           if_exists='replace', #{'fail', 'replace', 'append'}, default : fail
                           schema='public')

    # -- select database insert result
    df_kospi_select = pandas_sql.read_sql_query("select * from stock_kospi_day", alchemy_conn)
    print("database result ::: stock_kospi_month")
    print(df_kospi_select)

