
import re
from .provider import Provider
from .resources.constants import Constants as cnts
from colorama import Fore, Style, Back
from IPython import get_ipython
from IPython.display import display, HTML, Javascript, Markdown
from .resources.html_template import HtmlTemplate
from .resources.static_files_manager import StaticFilesManager
from .code_generator import CodeGenerator
from .metric import Metric
from .attribute import Attribute
from .grid import Grid
from .color import Color
from .filter import Filter
from .compare_metric import CompareMetric
from .row import Row
from .column import Column
from .legend import Legend
from .field import Field
from .markline import MarkLine
try:
    from importlib.metadata import version
except ImportError:
    # Try backport to PY<37 `importlib_resources`.
    from importlib_metadata import version
from .build_info import __BUILD_VERSION__
import urllib.parse
import warnings

warnings.filterwarnings('ignore')

html = HtmlTemplate()
static = StaticFilesManager()
version = version('chartfactor')


class CFToolkit(object):
    """
    CFToolkit is the root module. It provides the necessary methods to instantiate
    and get access to other components. It's responsible for getting the list of
    providers configuration and create the Provider instances to connect
    to your data source.
    """

    def __init__(self):
        self.__prompt_number = 0
        self.__kernel_id = ''
        self.__provider = None
        self.__source = ''
        self.__options = {}
        self.__graph = ''
        self.__title = None
        self.__metadata = None
        self.__width = '100%'
        self.__height = '400px'
        self.__iframe_height = '300px'

    @property
    def get_source(self):
        return self.__source

    @property
    def get_provider (self):
        return self.__provider

    @property
    def get_chart(self):
        return self.__graph

    @property
    def get_options(self):
        return self.__options

    # region Privates methods
    def __add_js_functions(self):
        try:
            get_ipython().ex("from IPython.display import display, HTML")
            get_ipython().ex("import json")
            get_ipython().ex("import ipykernel")
            get_ipython().ex("import re")

            display(Javascript(cnts.DEFINE_EXECUTE_PYTHON_JS_FUNC))
            display(Javascript(cnts.DEFINE_SEND_MESSAGE_JS_FUNC))
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')

    def __add_message_listener(self):
        try:
            comm = cnts.EXECUTE_PYTHON_COMMAND_JS
            df = 'event.data.df'
            conf = 'event.data.conf'
            get_data_sources_code = comm % (cnts.GET_DATA_SOURCES_PY_COMMAND)
            get_data_source_meta_code = comm % ((cnts.GET_DATA_SOURCE_META_PY_COMMAND % (df, df)))
            visualize_code = comm % ((cnts.VISUALIZE_PY_COMMAND % (df, conf)))
            count_query_code = comm % ((cnts.COUNT_QUERY_PY_COMMAND % (df, conf)))
            raw_query_code = comm % ((cnts.RAW_QUERY_PY_COMMAND % (df, conf)))

            listener_func = \
                cnts.DEFINE_EVENT_LISTENER_FUNC \
                % \
                (get_data_sources_code,
                 get_data_source_meta_code,
                 visualize_code,
                 count_query_code,
                 raw_query_code)

            display(Javascript(
                "try{ window.removeEventListener('message', window.cfMessageEventListener, false); } catch(e) {}"))
            add_event_listener = "window.addEventListener('message', window.cfMessageEventListener = " + listener_func + ", false);"
            display(Javascript(add_event_listener))
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')

    def __get_dataframe_by_name(self, name):
        try:
            get_ipython().ex("import pandas as pd")
            df = get_ipython().ev(f"[eval(g) for g in globals() if isinstance(eval(g), pd.core.frame.DataFrame) and g == '{name}']")
            if len(df) > 0:
                return df[0]
            else:
                raise Exception(f'The dataframe {name} is not defined.')
        except Exception as e:
            raise Exception(e)

    # endregion

    def provider(self, dataframe, json_config=None):
        """
        Creates a new instance of the Provider class from a given dataframe and json config
        :param dataframe: A Pandas DataFrame instance.
        :param json_config: A json configuration to perform the query.
        :return: A Provider instance.
        """
        self.__provider = Provider(dataframe, json_config)
        return self.__provider

    def studio(self, app=None, url="https://chartfactor.com/studio-dev/"):
        """
        Opens an instance of ChartFactor Studio inside of an IFrame.
        :param app: The name of a Studio app. A new application will be created if app=None of not found.
        :param url: The ChartFactor Studio host url. By default will be "https://chartfactor.com/studio/".
        :return: IFrame
        """
        self.__add_js_functions()

        self.__prompt_number = get_ipython().ev("len(In)-1")
        iframe_id = f'iframe{self.__prompt_number}'
        self.__kernel_id = get_ipython().ev("re.search('kernel-(.*).json', ipykernel.connect.get_connection_file()).group(1)")

        if isinstance(self.__kernel_id, str) and self.__kernel_id != '':
            iframe_id = f'{iframe_id}_{self.__kernel_id}'

        if app is None:
            display(HTML(
                f'<iframe id={iframe_id} name={iframe_id} src={url}dashboard.html#/new width=100% height=764 frameborder=0 allow="clipboard-read; clipboard-write"></iframe>'))
        else:
            display(HTML(
                f'<iframe id={iframe_id} name={iframe_id} src={url}dashboard.html#/appName={urllib.parse.quote(app)} width=100% height=764 frameborder=0 allow="clipboard-read; clipboard-write"></iframe>'))

        self.__add_message_listener()

    # region Standalone app functions
    @classmethod
    def source(cls, source):
        """
        Sets the source name which must be the name of a DataFrame instance.
        :param source: The name of a DataFrame instance.
        :return: A new CFToolkit instance
        """
        self = cls()
        try:
            if source and source != '':
                self.__source = source
                dataframe = self.__get_dataframe_by_name(source)
                self.__provider = Provider(dataframe)
                return self
            else:
                raise Exception('Provide a valid string dataframe name.')
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')
            return self

    def set(self, option, value):
        """
        Sets the specifics options to be configured in the current chart
        :param option: A string value with the option name.
        :param value: The value of the option.
        :return: The current CFToolkit instance.
        """
        try:
            if self.__provider is not None:
                if not isinstance(option, str):
                    print(f'{Style.BRIGHT}{Fore.RED}{"The value for the option must be string"}{Style.RESET_ALL}')
                    return self
                self.__options[option] = value
                return self
            else:
                raise Exception("The source() function must be called before the execute() one")
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')
            return self

    def graph(self, graph):
        """
        Sets the name of the chart to be rendered.
        :param graph: A string value with the name of the chart e.g.("Bar", "Pie", "Raw Data Table", ...)
        :return: The current CFToolkit instance.
        """
        try:
            if self.__provider is not None:
                if not isinstance(graph, str):
                    print(f'{Style.BRIGHT}{Fore.RED}{"The value for the graph must be string"}{Style.RESET_ALL}')
                    return self
                self.__graph = graph
                return self
            else:
                raise Exception("The source() function must be called before the execute() one")
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')
            return self

    def filters(self, *args):
        """
        Sets the filters to be applied to the current chart.
        :param args: The Filter instances to be applied to the current chart.
        :return: The current CFToolkit instance.
        """
        if self.__provider is not None:
            list_args = list(args)
            if len(list_args) > 0 and isinstance(list_args[0], list):
                parameters = list_args[0]
            else:
                parameters = list(args)
            self.__provider.filters(parameters)
        else:
            raise Exception("The source() function must be called before the filters() one")
        return self

    def filter(self, filter):
        """
        Sets a single filter instance to be applied to the current chart.
        :param filter: A Filter instance.
        :return: The current CFToolkit instance.
        """
        if self.__provider is not None:
            self.__provider.filter(filter)
        else:
            raise Exception("The source() function must be called before the filter() one")
        return self

    def metrics(self, *args):
        """
        Sets the metrics to be applied to the current chart.
        :param args: The Metric instances to be applied to the current chart.
        :return: The current CFToolkit instance.
        """
        if self.__provider is not None:
            list_args = list(args)
            if len(list_args) > 0 and isinstance(list_args[0], list):
                parameters = list_args[0]
            else:
                parameters = list(args)
            self.__provider.metrics(parameters)
        else:
            raise Exception("The source() function must be called before the metrics() one")
        return self

    def groupby(self, *args):
        """
        Sets the attributes to be grouped in the current chart.
        :param args: The Attribute instances to be grouped in the current chart.
        :return: The current CFToolkit instance.
        """
        if self.__provider is not None:
            list_args = list(args)
            if len(list_args) > 0 and isinstance(list_args[0], list):
                parameters = list_args[0]
            else:
                parameters = list(args)
            self.__provider.groupby(parameters)
        else:
            raise Exception("The source() function must be called before the groupby() one")
        return self

    def rows(self, *args):
        if self.__provider is not None:
            list_args = list(args)
            if len(list_args) > 0 and isinstance(list_args[0], list):
                parameters = list_args[0]
            else:
                parameters = list(args)
            self.__provider.rows(parameters)
        else:
            raise Exception("The source() function must be called before the rows() one")
        return self

    def columns(self, *args):
        if self.__provider is not None:
            list_args = list(args)
            if len(list_args) > 0 and isinstance(list_args[0], list):
                parameters = list_args[0]
            else:
                parameters = list(args)
            self.__provider.columns(parameters)
        else:
            raise Exception("The source() function must be called before the columns() one")
        return self

    def fields(self, *args):
        if self.__provider is not None:
            list_args = list(args)
            if len(list_args) > 0 and isinstance(list_args[0], list):
                parameters = list_args[0]
            else:
                parameters = list(args)
            self.__provider.fields(parameters)
        else:
            raise Exception("The source() function must be called before the fields() one")
        return self

    def exclude(self, *args):
        if self.__provider is not None:
            list_args = list(args)
            if len(list_args) > 0 and isinstance(list_args[0], list):
                parameters = list_args[0]
            else:
                parameters = list(args)
            self.__provider.exclude(parameters)
        else:
            raise Exception("The source() function must be called before the exclude() one")
        return self

    def limit(self, limit):
        if self.__provider is not None:
            self.__provider.limit(limit)
        else:
            raise Exception("The source() function must be called before the limit() one")
        return self

    def location(self, location_field):
        if self.__provider is not None:
            self.__provider.location(location_field)
        else:
            raise Exception("The source() function must be called before the location() one")
        return self

    def precision(self, precision):
        if self.__provider is not None:
            self.__provider.precision(precision)
        else:
            raise Exception("The source() function must be called before the precision() one")
        return self

    def timeField(self, time_field):
        if self.__provider is not None:
            self.__provider.timeField(time_field)
        else:
            raise Exception("The source() function must be called before the timeField() one")
        return self

    def onlyWithFilters(self, obj):
        if self.__provider is not None:
            self.__provider.onlyWithFilters(obj)
        else:
            raise Exception("The source() function must be called before the onlyWithFilters() one")
        return self

    def title(self, title):
        self.__title = title
        return self

    def metadata(self, metadata):
        if not isinstance(metadata, str):
            raise Exception("metadata function parameter must be a string value")
        self.__metadata = metadata
        return self

    def width(self, width):
        self.__width = width
        return self

    def height(self, height):
        try:
            height = int(height)
        except:
            pass

        if isinstance(height, int):
            height = f'{height}px'
        else:
            match = re.match(r"^[0-9]+(px)$", height)
            if not match:
                height = '400px'

        self.__height = height
        self.__set_iframe_height()
        return self

    def __set_iframe_height(self):
        chart_height = int(self.__height.split("px")[0])
        iframe_height = chart_height + 100 if chart_height > 200 else 300
        self.__iframe_height = f'{iframe_height}px'

    def execute(self):
        """Set up of the final code snippet to be rendered"""
        try:
            if self.__provider is not None:
                self.__add_js_functions()
                self.__add_message_listener()

                self.__prompt_number = get_ipython().ev("len(In)-1")
                pn = self.__prompt_number
                iframe_id = f'iframe{pn}'
                self.__kernel_id = get_ipython().ev(
                    "re.search('kernel-(.*).json', ipykernel.connect.get_connection_file()).group(1)")

                if isinstance(self.__kernel_id, str) and self.__kernel_id != '':
                    iframe_id = f'{iframe_id}_{self.__kernel_id}'

                style = static.css()
                if self.__width:
                    if isinstance(self.__width, int):
                        self.__width = f'{self.__width}px'
                    style = style.replace('width: 100%;', f'width: {self.__width};')
                if self.__height:
                    style = style.replace('height: 400px;', f'height: {self.__height};')
                self.__set_iframe_height()
                visual_code = self.get_visualization_js_code(pn)
                metadata = self.__metadata if self.__metadata is not None else ''
                # Setting the html code for ' to avoid quote issue in IFrame
                visual_code = re.sub(r"\'", '&apos;', visual_code)
                metadata = re.sub(r"\'", '&apos;', metadata)

                graph = self.__graph
                title = self.__title if self.__title is not None else graph
                iframe = html.iframe.format(iframe_id, iframe_id, self.__iframe_height, html.google_font_1, html.google_font_2, html.bootstrap, style, title, pn, metadata, visual_code)

                return HTML(iframe)
            else:
                raise Exception("The source() function must be called before the execute() one")
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')
            return HTML('<div></div>')

    def _getJavaScriptCode(self):
        try:
            if self.__provider is not None:
                self.__prompt_number = get_ipython().ev("len(In)-1")
                pn = self.__prompt_number
                visual_code = self.get_visualization_js_code(pn)
                mkd = '```js\n' + visual_code + '\n' + '```\n'
                return Markdown(mkd)
            else:
                raise Exception("The source() function must be called before the execute() one")
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')

    def get_visualization_js_code(self, pn=0):
        code_gen = CodeGenerator(self)
        code = ''
        pv = self.__provider
        if pv is not None and not pv.get_error:
            graph = self.__graph if self.__graph != '' else self.__provider.get_chart if self.__provider.get_chart != '' else ''
            if graph != '':
                code = code_gen.generate_code(graph, pn)
                # if code_gen.can_generate_code(graph):
                #     code = code_gen.generate_code(graph, pn)
                # else:
                #     raise Exception(f'The javascript code for the chart {graph} could not be generated')
            else:
                raise Exception('The graph() function must be called before the execute() one')
        return code

    def fullWidth(self):
        """
        Sets the 100% width for the current notebook
        :return:
        """
        display(HTML("<style>.container { width:100% !important; }</style>"))

    def fullCellWidth(self):
        """
        Sets the 100% width for the current notebook
        :return:
        """
        pn = str(get_ipython().ev("len(In)-1"))
        display(Javascript("""
        javascript:(function(){
            var cellCounters = document.querySelectorAll("#notebook-container > div > div.input > div.prompt_container > div.prompt.input_prompt");
            var numbers = [].map.call(cellCounters, a=> parseInt(a.innerText.match(/\[(.+)\]/)[1].replace("*", '999999999999999999').replace(" ", '-1')));
            var maxNumber = Math.max(...numbers);
            var maxIndex = numbers.indexOf(maxNumber);
            $('#notebook-container').children('.cell.code_cell.rendered').eq(maxIndex).prop('id', 'code_cell_' + """ + pn + """);
        })();
        """))
        display(HTML(f"""
        <style>
            #code_cell_{pn} {{ 
                width: 99vw !important;
                position: relative !important;
                left: calc(-49vw + 49%) !important;
                background-color: white !important;
            }}
        </style>
        """))

    def version(self):
        """
        Display the current charfactor version
        :return: version string
        """
        return version

    def build(self):
        """
        Display the current charfactor build version
        :return: build version string
        """
        return __BUILD_VERSION__

    def Metric(self, name='count', func=cnts.SUM):
        """
        Define a metric using the sum of 'pricepaid' field: metric = cf.Metric('pricepaid','sum')
        :param name: name of the field
        :param func: metric function ('sum','avg','min','max')
        :return: Metric
        """
        return Metric(name, func)

    def Attribute(self, name, label=''):
        """
        Define a group using 'venuecity' field, limited to top 10 results sort ascending alphabetically:
        group = cf.Attribute('venuecity').limit(10).sort('asc','venuecity')
        :param name: name of the field
        :param label: label of the field
        :return: Attribute
        """
        return Attribute(name, label)

    def Grid(self):
        """
        Create a new Grid definition.
        Define a grid with top 10px,bottom 15px,left 20px and right 10px:
        grid = Grid().top('10px').bottom('15px').left('20px').right('10px')
        :return: Grid
        """
        return Grid()

    def Color(self):
        """
        Create a new Color definition.
        Define a color configuration using theme 'intense' and coloring by metric value:
        color = Color().theme('intense').metric(metric0)
        :return:
        """
        return Color()

    def Filter(self, path):
        """
        Create a new Filter
        Define a filter using field 'venuestate' in ['CA','FL']:
        filter = cf.Filter('venuestate').operation('IN').value(['CA','FL'])
        :param path: name of the field
        :return: Filter
        """
        return Filter(path)

    def CompareMetric(self, name='count', func=cnts.SUM):
        return CompareMetric(name, func)

    def Field(self, name, label=''):
        """
        Create a new Field
        Define field for Raw data queries:
        field = cf.Field('venuestate','Venue State')
        :param name: name of the field
        :param label: label to show
        :return: Field
        """
        return Field(name, label)

    def Row(self, name, label=''):
        """
        Create a new Row
        Define field for Pivot queries:
        row = cf.Row('venuestate','Venue State').sort('asc')
        :param name: name of the column
        :param label: label to show
        :return: Row
        """
        return Row(name, label)

    def Column(self, name, label=''):
        """
        Create a new Column
        Define field for Pivot queries:
        column = cf.Column('venuestate','Venue State').sort('desc')
        :param name: name of the column
        :param label: label to show
        :return: Column
        """
        return Column(name, label)

    def Legend(self):
        """
        Create a new Legend definition
        legend = cf.Legend().position('right').width(150)
        :return: Legend
        """
        return Legend()

    def MarkLine(self):
        """
        Create a new MarkLine
        :return:
        """
        return MarkLine()

    # endregion
