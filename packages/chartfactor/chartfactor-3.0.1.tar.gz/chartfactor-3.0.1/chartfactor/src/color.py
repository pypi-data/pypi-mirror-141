import json
from .resources.constants import Constants as cnts
from .resources.commons import Commons as cmms
from .metric import Metric

eol = '\n'
tab = '\t'


class Color(object):
    """
    Create a new Color definition.
    Define a color configuration using theme 'intense' and coloring by metric value:
    color = Color().theme('intense').metric(metric0)
    """

    def __init__(self):
        self.__metric = None
        self.__skin = None
        self.__palette = None
        self.__range = None
        self.__auto_range_options = None

    @property
    def get_theme(self):
        return self.__skin

    @property
    def get_metric(self):
        return self.__metric

    @property
    def get_palette(self):
        return self.__palette

    @property
    def get_range(self):
        return self.__range

    @property
    def get_auto_range_options(self):
        return self.__auto_range_options

    def theme(self, skin):
        self.__skin = skin
        return self

    def metric(self, metric=None):
        if metric is not None and not isinstance(metric, Metric):
            raise Exception('The metric function parameter must be an instance of Metric object')
        self.__metric = metric
        return self

    def palette(self, palette):
        self.__palette = palette
        return self

    def range(self, range):
        self.__range = range
        return self

    def autoRange(self, options):
        self.__auto_range_options = options
        return self

    def toJs(self):
        metric_call = ''
        if self.__metric is not None:
            cm_func = self.__metric.func
            cm_name = self.__metric.name
            func_declaration = f', "{cm_func}"' if cm_func and cm_func != 'derived' else ''
            metric_call = f'.metric(cf.Metric("{cm_name}"{func_declaration}))' if self.__metric is not None else ''

        palette_call = f'.palette({json.dumps(self.__palette)})' if self.__palette is not None else ''
        range_call = f'.range({json.dumps(self.__range)})' if self.__range is not None else ''
        theme_call = f'.theme({json.dumps(self.__skin)})' if self.__skin is not None else ''
        auto_range_call = f'.autoRange({json.dumps(self.__auto_range_options)})' if self.__auto_range_options is not None else ''

        return f'cf.Color(){palette_call}{metric_call}{range_call}{theme_call}{auto_range_call}'
