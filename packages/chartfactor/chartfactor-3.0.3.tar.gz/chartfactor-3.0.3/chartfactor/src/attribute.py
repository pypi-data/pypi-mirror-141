import json
from .resources.constants import Constants as cnts
from .metric import Metric


class Attribute(object):
    """
    Define a group using 'venuecity' field, limited to top 10 results sort ascending alphabetically:
    group = Attribute('venuecity').limit(10).sort('asc','venuecity')
    """

    def __init__(self, name, label=''):
        self.__name = name
        self.__label = label
        self.__limit = 100
        self.__granularity = None
        self.__time_zone = None
        self.__sort = {'name': '', 'func': cnts.SUM, 'dir': cnts.ASC}
        self.__has_sort = False
        self.__is_sort_by_metric = False

    @property
    def get_name(self):
        return self.__name

    @property
    def get_label(self):
        return self.__label

    @property
    def get_limit(self):
        return self.__limit

    @property
    def get_sort(self):
        return self.__sort

    @property
    def has_sort(self):
        return self.__has_sort

    @property
    def is_sort_by_metric(self):
        return self.__is_sort_by_metric

    @property
    def get_granularity(self):
        return self.__granularity

    @property
    def get_tz(self):
        return self.__time_zone

    def __repr__(self):
        attrs = self.__get_val__()
        return json.dumps(attrs)

    def __get_val__(self):
        return {
            'name': self.__name,
            'label': self.__label,
            'limit': self.__limit,
            'sort': self.__sort
        }

    def label(self, label):
        self.__label = label
        return self

    def limit(self, limit):
        if not isinstance(limit, int):
            raise Exception('The value for the limit must be integer')
        self.__limit = limit
        return self

    def sort(self, dir, metric):
        func = ''
        if isinstance(metric, Metric):
            self.__is_sort_by_metric = True
            name = metric.__get_val__()['name']
            func = metric.__get_val__()['func']
        elif isinstance(metric, str):
            name = metric
        else:
            raise Exception("The second parameter of the sort() function must be string or an instance of Metric() object")

        if str.upper(dir) not in [cnts.ASC, cnts.DESC]:
            raise Exception(f"Invalid sort direction '{dir}'. Use one of these: %s" % [cnts.ASC, cnts.DESC])

        self.__sort = {'name': name, 'func': func, 'dir': str.upper(dir)}
        self.__has_sort = True

        return self

    def func(self, granularity):
        self.__granularity = granularity
        return self

    def tz(self, tz):
        self.__time_zone = tz
        return self
