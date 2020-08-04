import pandas.io.sql as pandas_sql
from pandas import DataFrame
import urllib3
import json

from datetime import timedelta, date
import datetime
from calendar import monthrange
import copy

from url_builder.korbank.urls import UrlManager
from url_builder.korbank.parameters import kospi_kwargs

COLUMN_LIST = [
        'STAT_NAME',  'STAT_CODE',  'ITEM_CODE1', 'ITEM_CODE2', 'ITEM_CODE3',
        'ITEM_NAME1', 'ITEM_NAME2', 'ITEM_NAME3', 'DATA_VALUE', 'TIME'
    ]

api_key = '-'
MM = 'MM'
DD = 'DD'


def get_column_list():
    return COLUMN_LIST


# 컬럼매핑
arr_columns = get_column_list()

if __name__ == '__main__':
    url = "http://ecos.bok.or.kr/api/StatisticSearch/{}/json/kr/1/50000/064Y001/DD/20200728/20201231/0001000" \
        .format(api_key)

    print(" ####### URL #######")
    print(url)
    print(" #######     #######")

    http = urllib3.PoolManager()
    ret = http.request("GET", url, headers={'Content-Type': 'application/json'})

    str_response = ret.data.decode('utf-8')
    dict_data = json.loads(str_response)
    arr_data = dict_data['StatisticSearch']['row']

    # [{}, {}, {} ] -> [ [] [] [] [] ...]  변환 작업
    data_for_insert = [[datetime.datetime.strptime(dict_data[column_nm], '%Y%m%d').date() if column_nm == 'TIME' else dict_data[column_nm] for column_nm in arr_columns] for dict_data in arr_data]

    df_kospi_insert = DataFrame(data_for_insert, columns=arr_columns)
    df_kospi_insert.to_csv('csv/test.csv', sep=',', na_rep='NaN', index=False)

    # JSON 방식으로도 변환 필요 ( 샘플 형식 : https://github.com/soongujung/study_archives/blob/master/ELK/elasticsearch-basic/ElasticSearch_BUCKET_AGGREGATION.md#%EC%98%88%EC%A0%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C__
    # ElasticSearch 에서 받아들이는 데이터의 형식이 JSON의 일반형식과는 달라서 이게 잘 될지는 장담하지는 못하겠다.
    # 다양한 JSON 을 테스트 해봐야 할 듯하다.
