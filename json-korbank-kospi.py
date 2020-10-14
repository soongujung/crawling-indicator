import urllib3
import json
import os
import datetime

date_formatter = '%Y%m%d'

COLUMN_LIST = [
        'STAT_NAME',  'STAT_CODE',  'ITEM_CODE1', 'ITEM_CODE2', 'ITEM_CODE3',
        'ITEM_NAME1', 'ITEM_NAME2', 'ITEM_NAME3', 'DATA_VALUE', 'TIME'
    ]

api_key = '--'


# TODO 정리필요 (1)
# Object of type datetime is not JSON serializable 에러에 대해서 아래의 custom_converter() 함수를 사용하면 된다.
# 원리는 datetime 객체내의 __str__ 을 통해 toString 효과를 내도록 하는 것.
# datetime 객체 자체가 json 모듈안에서 기본으로 지원되지 않는 듯 하다.
# https://code-maven.com/serialize-datetime-object-as-json-in-python


def custom_converter(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat().__str__()

# TODO 정리필요 (2)
# 매핑코드 변경된 내용들 정리(원리 및 벨로그 업데이트) 필요함


if __name__ == '__main__':
    url = "http://ecos.bok.or.kr/api/StatisticSearch/{}/json/kr/1/50000/064Y001/DD/20190101/20201231/0001000" \
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

    # index, id 추가 안할 때의 데이터
    # with open('json/document/kospi_data.json', 'w+') as f:
    #     for e in arr_data:
    #         stringified_json = json.dumps(e)
    #         stringified_json = stringified_json + "\n"
    #         print(stringified_json)
    #         f.write(stringified_json)

    # index, id 추가 한 후의 데이터
    # type 역시 추가
    with open('json/document/kospi_data_20201014_isoformat.json', 'w+') as f:
        for e in arr_data:
            # type 을 지정할 경우
            # dict_index = {'index': {'_index': 'indicators', '_type': 'kospi', '_id': e['TIME']}}
            # type 을 지정하지 않을 경우

            # datetime 타입으로 변환
            e['TIME'] = datetime.datetime.strptime(e['TIME'], date_formatter)

            dict_index = {'index': {'_index': 'kospi', '_id': e['TIME']}}
            str_index_id = json.dumps(dict_index, default=custom_converter)
            stringified_json = str_index_id + "\n"

            stringified_json = stringified_json + json.dumps(e, default=custom_converter)
            stringified_json = stringified_json + "\n"
            print(stringified_json)
            f.write(stringified_json)
