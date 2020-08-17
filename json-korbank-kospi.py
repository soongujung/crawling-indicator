import urllib3
import json
import os

COLUMN_LIST = [
        'STAT_NAME',  'STAT_CODE',  'ITEM_CODE1', 'ITEM_CODE2', 'ITEM_CODE3',
        'ITEM_NAME1', 'ITEM_NAME2', 'ITEM_NAME3', 'DATA_VALUE', 'TIME'
    ]

api_key = '--'
MM = 'MM'
DD = 'DD'


def get_column_list():
    return COLUMN_LIST


# 컬럼매핑
arr_columns = get_column_list()

if __name__ == '__main__':
    url = "http://ecos.bok.or.kr/api/StatisticSearch/{}/json/kr/1/50000/064Y001/DD/20200813/20201231/0001000" \
        .format(api_key)

    print(" ####### URL #######")
    print(url)

    http = urllib3.PoolManager()
    ret = http.request("GET", url, headers={'Content-Type': 'application/json'})

    str_response = ret.data.decode('utf-8')
    dict_data = json.loads(str_response)

    arr_data = dict_data['StatisticSearch']['row']

    directory = 'json/document/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open('json/document/test_data.json', 'w+') as f:
        for e in arr_data:
            stringified_json = json.dumps(e)
            stringified_json = stringified_json + "\n"
            print(stringified_json)
            f.write(stringified_json)
