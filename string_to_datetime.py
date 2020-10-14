import datetime
date_str = '20200101'
formatter = '%Y%m%d'
test_data = datetime.datetime.strptime(date_str, formatter)
print(test_data)
print(type(test_data))