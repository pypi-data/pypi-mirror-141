import json
from .resources.constants import Constants as cnts


class Filter(object):
    """
    Create a new Filter
    Define a filter using field 'venuestate' in ['CA','FL']:
    filter = Filter('venuestate').operation('IN').value(['CA','FL'])
    """

    def __init__(self, path):
        self.__path = path
        self.__label = path
        self.__operation = 'IN'
        self.__value = []
        self.__relative = False
        self.__is_text_filter = False

    def __repr__(self):
        attrs = self.__get_val__()
        return json.dumps(attrs)

    def __get_val__(self):
        return {
            'path': self.__path,
            'operation': self.__operation,
            'value': self.__value
        }

    @property
    def get_path(self):
        return self.__path

    @property
    def get_label(self):
        return self.__label

    @property
    def get_operation(self):
        return self.__operation

    @property
    def get_value(self):
        return self.__value

    @property
    def get_relative(self):
        return self.__relative

    @property
    def is_text_filter(self):
        return self.__is_text_filter

    def __translate_operation__(self, op):
        op = op.replace('<=', 'LE')
        op = op.replace('>=', 'GE')
        op = op.replace('<', 'LT')
        op = op.replace('>', 'GT')
        op = op.replace('!=', 'NOT EQUAL')
        op = op.replace('<>', 'NOT EQUAL')
        op = op.replace('=', 'EQUAL')
        op = op.replace('EQUALS', 'EQUAL')
        op = op.replace('NOT EQUALS', 'NOT EQUAL')
        return op

    def label(self, label):
        self.__label = label
        return self

    def operation(self, op):
        if not isinstance(op, str):
            raise Exception('The value for the operation must be string')

        op = op.upper()
        op = self.__translate_operation__(op)

        if op not in cnts.FILTER_OPERATIONS:
            raise Exception(f'Invalid filter operation {op}. Use one of these: %s' % cnts.FILTER_OPERATIONS)

        self.__operation = op
        return self

    def value(self, *args):
        if args and isinstance(args[0], list):
            self.__value = args[0]
        else:
            self.__value = list(args)
        return self

    def isRelative(self):
        self.__relative = True
        return self

    def isTextFilter(self):
        self.__is_text_filter = True
        return self
