import json
from .resources.constants import Constants as cnts


class Metric(object):
    """
    Define a metric using the sum of 'pricepaid' field: metric = Metric('pricepaid','sum')
    """
    def __init__(self, name='count', func=cnts.SUM):
        self.__name = name
        self.__func = func
        self.__interval = None
        self.__fixed_bars = 8
        self.__has_fixed_bars = False
        self.__show_empty_intervals = False
        self.__has_show_empty_intervals = False
        self.__offset = 0
        self.__hide_function = False
        self.__is_sort_metric = False

    @property
    def name(self):
        return self.__name

    @property
    def func(self):
        return self.__func

    @property
    def get_interval(self):
        return self.__interval

    @property
    def get_fixed_bars(self):
        return self.__fixed_bars

    @property
    def has_fixed_bars(self):
        return self.__has_fixed_bars

    @property
    def get_show_empty_intervals(self):
        return self.__show_empty_intervals

    @property
    def has_show_empty_intervals(self):
        return self.__has_show_empty_intervals

    @property
    def get_offset(self):
        return self.__offset

    @property
    def get_hide_function(self):
        return self.__hide_function

    @property
    def is_sort_metric(self):
        return self.__is_sort_metric

    def __repr__(self):
        attr = self.__get_val__()
        return json.dumps(attr)

    def __get_val__(self):
        metric = {'name': self.__name, 'func': self.__func, "isSortMetric": self.__is_sort_metric}
        if self.__name == "count":
            metric['func'] = ""
        return metric

    def interval(self, interval):
        if interval < 0:
            raise Exception('The interval must be a positive decimal.')
        if interval < self.__offset:
            raise Exception('The interval must be greater than the offset.')
        self.__interval = interval
        return self

    def fixedBars(self, fixed_bars):
        if fixed_bars < 0:
            raise Exception('The fixedBars must be a positive decimal.')
        self.__fixed_bars = fixed_bars
        self.__has_fixed_bars = True
        return self

    def showEmptyIntervals(self, show):
        self.__show_empty_intervals = show
        self.__has_show_empty_intervals = True
        return self

    def offset(self, offset):
        if offset < 0:
            raise Exception('The offset must be a positive decimal.')
        if self.__interval is not None and offset > self.__interval:
            raise Exception('The offset must be less than the interval.')
        self.__offset = offset
        return self

    def hideFunction(self):
        self.__hide_function = True
        return self

    def isSortMetric(self):
        self.__is_sort_metric = True
        return self
