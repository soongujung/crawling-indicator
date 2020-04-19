
class UrlManager:
    # url = "http://ecos.bok.or.kr/api/StatisticSearch/{}/json/kr/1/5000/064Y001/DD/20140101/20191231/0001000".format(api_key)

    API_KEY = ""
    SEPARATOR = "/"
    BASE_URL = "http://ecos.bok.or.kr/api/StatisticSearch/{}/json/kr/{}/{}/{}/{}/{}/{}/{}"
    FROM = 1
    TO = 5000

    ITEM_CODE1 = ''
    ITEM_CODE2 = ''
    SEARCH_TYPE = 'DD'

    START_DATE = '20140101'
    END_DATE = '20191231'

    def __init__(self):
        print('init')
        super(UrlManager, self).__init__()

    def add_api_key(self, api_key):
        self.API_KEY = api_key
        return self

    def add_item_code1(self, item_code):
        self.ITEM_CODE1 = item_code
        return self

    def add_item_code2(self, item_code):
        self.ITEM_CODE2 = item_code
        return self

    def add_search_type(self, search_type):
        self.SEARCH_TYPE = search_type
        return self

    def add_start_date(self, start_date):
        self.START_DATE = start_date
        return self

    def add_end_date(self, end_date):
        self.END_DATE = end_date
        return self

    def add_from(self, _from):
        self.FROM = _from
        return self

    def add_to(self, _to):
        self.TO = _to
        return self

    def build_url(self):
        self.BASE_URL = self.BASE_URL.format(
            self.API_KEY, self.FROM, self.TO,
            self.ITEM_CODE1, self.SEARCH_TYPE,
            self.START_DATE, self.END_DATE,
            self.ITEM_CODE2
        )

        return self.BASE_URL
