
import hashlib

from epyk.core.html import Html

from epyk.core.js.packages import packageImport
from epyk.core.js.packages import JsTabulator

from epyk.core.data import DataClass
from epyk.core.data import DataEnum
from epyk.core.data import DataEnumMulti

# The list of CSS classes
from epyk.core.css.styles import GrpClsTable


class Table(Html.Html):
  name, category, callFnc = 'Table', 'Tables', 'table'
  __reqCss, __reqJs = ['tabulator'], ['tabulator']

  def __init__(self, report, records, width, height, htmlCode, options, profile):
    data, columns, self.__config = [], [], None
    super(Table, self).__init__(report, [], code=htmlCode, css_attrs={"width": width, "height": height}, profile=profile)
    if records is not None:
      self.config.data = records
    self.style.css.background = None

  @property
  def style(self):
    if self._styleObj is None:
      self._styleObj = GrpClsTable.Tabulator(self)
    return self._styleObj

  @property
  def tableId(self):
    """
    Return the Javascript variable of the chart
    """
    return "%s_obj" % self.htmlId

  @property
  def config(self):
    if self.__config is None:
      self.__config = TableConfig(self._report)
    return self.__config

  @property
  def js(self):
    """
    Return the Javascript internal object

    :return: A Javascript object

    :rtype: JsTabulator.Tabulator
    """
    if self._js is None:
      self._js = JsTabulator.Tabulator(self._report, selector=self.tableId, setVar=False, parent=self)
    return self._js

  def add_column(self, field, title=None):
    """

    :param field:
    :param title:
    """
    col_def = self.config.columns
    col_def.field = field
    col_def.title = field if title is None else title
    return col_def

  def get_column(self, by_title):
    """

    :param by_title:
    """
    for c in self.config._attrs.get('columns', []):
      if c.title == by_title:
        return c

    return None

  def build(self, data=None, options=None, profile=False):
    print(self.config)
    return 'var %s =  new Tabulator("#%s", %s)' % (self.tableId, self.htmlId, self.config)

  def __str__(self):
    self._report._props.setdefault('js', {}).setdefault("builders", []).append(self.refresh())
    return "<div %s></div>" % (self.get_attrs(pyClassNames=self.style.get_classes()))


class EnumLayout(DataEnum):

  def fitDataStretch(self): return self.set()

  def fitColumns(self): return self.set()

  def fitDataStretch(self): return self.set()

  def fitDataFill(self): return self.set()


class EnumSorter(DataEnum):

  def string(self):
    """
    Sorts column as strings of characters

    http://tabulator.info/examples/4.5#sorters
    """
    return self.set("string")

  def number(self):
    """
    Sorts column as numbers (integer or float, will also handle numbers using "," separators)

    http://tabulator.info/examples/4.5#sorters
    """
    return self.set("number")

  def alphanum(self):
    """
    Sorts column as alpha numeric code

    http://tabulator.info/examples/4.5#sorters
    """
    return self.set("alphanum")

  def boolean(self):
    """
    Sorts column as booleans

    http://tabulator.info/examples/4.5#sorters
    """
    return self.set("boolean")

  def date(self):
    """
    Sorts column as dates

    http://tabulator.info/examples/4.5#sorters
    """
    return self.set("date")

  def time(self):
    """
    Sorts column as dates

    sorts column as times
    """
    return self.set("time")


class EnumColCss(DataEnumMulti):
  js_conversion = True
  delimiter = " "

  def center(self):
    """

    """
    self._report.body.style.custom_class({'_attrs': {'text-align': 'center'}}, classname="tb-center")
    return self.set("tb-center")

  def color(self, color):
    """

    :param color:
    """
    self._report.body.style.custom_class({'_attrs': {'color': color}}, classname="tb-color-%s" % color)
    return self.set("tb-color-%s" % color)

  def background(self, color):
    """

    :param color:
    """
    self._report.body.style.custom_class({'_attrs': {'background-color': color}}, classname="tb-background-%s" % color)
    return self.set("tb-background-%s" % color)

  def css(self, css_attrs, css_attrs_hover=None):
    """

    col_def.cssClass.css({'background': 'orange'}, {'background': 'white', 'color': 'blue'})

    :param css_attrs:
    :param css_attrs_hover:
    """
    has_style = str(hashlib.sha1(str(css_attrs).encode()).hexdigest())
    self._report.body.style.custom_class({'_attrs': css_attrs, '_hover': css_attrs_hover}, classname="tb-style-%s" % has_style)
    return self.set("tb-style-%s" % has_style)


class Persistence(DataClass):

  @property
  def sort(self):
    return self._attrs["sort"]

  @sort.setter
  def sort(self, val):
    self._attrs["sort"] = val

  @property
  def filter(self):
    return self._attrs["filter"]

  @filter.setter
  def filter(self, val):
    self._attrs["filter"] = val

  @property
  def columns(self):
    return self._attrs["columns"]

  @columns.setter
  def columns(self, val):
    self._attrs["columns"] = val


class BottomCalcParams(DataClass):

  @property
  def precision(self):
    return self._attrs["precision"]

  @precision.setter
  def precision(self, val):
    self._attrs["precision"] = val


class ColumnsGroup(DataClass):

  @property
  def title(self):
    return self._attrs["title"]

  @title.setter
  def title(self, val):
    self._attrs["title"] = val

  @property
  def columns(self):
    return self.sub_data_enum("columns", Column)


class Column(DataClass):

  @property
  def align(self):
    return self._attrs["align"]

  @align.setter
  def align(self, val):
    self._attrs["align"] = val

  @property
  def autoColumns(self):
    return self._attrs["autoColumns"]

  @autoColumns.setter
  def autoColumns(self, val):
    self._attrs["autoColumns"] = val

  @property
  def bottomCalc(self):
    return self._attrs["bottomCalc"]

  @bottomCalc.setter
  def bottomCalc(self, val):
    self._attrs["bottomCalc"] = val

  @property
  def bottomCalcParams(self):
    return self.sub_data("bottomCalcParams", BottomCalcParams)

  @property
  def cssClass(self):
    return self.has_attribute(EnumColCss)

  @property
  def editable(self):
    return self._attrs["editable"]

  @editable.setter
  def editable(self, val):
    self._attrs["editable"] = val

  def editor_input(self, search=True, elementAttributes=None, **kwargs):
    """
    Description:
    -----------
    The input editor allows entering of a single line of plain text

    Related Pages:
    --------------
    http://tabulator.info/docs/4.5/edit#edit-builtin

    Attributes:
    ----------
    :param search: use search type input element with clear button
    :param elementAttributes: set attributes directly on the input element
    """
    self._attrs["editor"] = 'input'
    self._attrs["editorParams"] = {'search': search}
    if elementAttributes is not None:
      self._attrs["editorParams"][elementAttributes] = elementAttributes
    self._attrs["editorParams"].update(self._attrs["editorParams"].pop('kwargs'))
    return self

  def editor_textarea(self, verticalNavigation="editor", elementAttributes=None, **kwargs):
    """
    Description:
    -----------
    The textarea editor allows entering of multiple lines of plain text

    Related Pages:
    --------------
    http://tabulator.info/docs/4.5/edit#edit-builtin

    Attributes:
    ----------
    :param verticalNavigation: set attributes directly on the textarea element
    :param elementAttributes: determine how use of the up/down arrow keys will affect the editor,
    """
    self._attrs["editor"] = 'textarea'
    self._attrs["editorParams"] = {'verticalNavigation': verticalNavigation, "elementAttributes": elementAttributes}
    self._attrs["editorParams"].update(self._attrs["editorParams"].pop('kwargs'))
    return self

  def editor_number(self, min=None, max=None, step=1, elementAttributes=None, verticalNavigation="table", **kwargs):
    """
    Description:
    -----------
    The number editor allows for numeric entry with a number type input element with increment and decrement buttons.

    Related Pages:
    --------------
    http://tabulator.info/docs/4.5/edit#edit-builtin

    Attributes:
    ----------
    :param min: the maximum allowed value
    :param max: the minimum allowed value
    :param step: the step size when incrementing/decrementingthe value (default 1)
    :param elementAttributes: set attributes directly on the input element
    :param verticalNavigation: determine how use of the up/down arrow keys will affect the editor,
    :param kwargs:
    """
    self._attrs["editor"] = 'number'
    self._attrs["editorParams"] = {'step': step, 'verticalNavigation': verticalNavigation, "elementAttributes": elementAttributes}
    if min is not None:
      self._attrs["editorParams"]['min'] = min
    if max is not None:
      self._attrs["editorParams"]['max'] = max
    self._attrs["editorParams"].update(self._attrs["editorParams"].pop('kwargs'))
    return self

  def editor_range(self, min=None, max=None, step=1, elementAttributes=None, **kwargs):
    """
    Description:
    -----------
    The range editor allows for numeric entry with a range type input element.

    Related Pages:
    --------------
    http://tabulator.info/docs/4.5/edit#edit-builtin

    Attributes:
    ----------
    :param min: the maximum allowed value
    :param max: the minimum allowed value
    :param step: the step size when incrementing/decrementingthe value (default 1)
    :param elementAttributes: set attributes directly on the input element
    :param kwargs:
    """
    self._attrs["editor"] = 'range'
    self._attrs["editorParams"] = {'step': step, "elementAttributes": elementAttributes}
    if min is not None:
      self._attrs["editorParams"]['min'] = min
    if max is not None:
      self._attrs["editorParams"]['max'] = max
    self._attrs["editorParams"].update(self._attrs["editorParams"].pop('kwargs'))
    return self

  def editor_tick(self, tristate=False, indeterminateValue=None, elementAttributes=None, **kwargs):
    """
    Description:
    -----------
    The tick editor allows for boolean values using a checkbox type input element.

    Related Pages:
    --------------
    http://tabulator.info/docs/4.5/edit#edit-builtin

    Attributes:
    ----------
    :param tristate: allow tristate tickbox (default false)
    :param indeterminateValue:  when using tristate tickbox what value should the third indeterminate state have (default null)
    :param elementAttributes: set attributes directly on the input element
    :param kwargs:
    """
    self._attrs["editor"] = 'tick'
    self._attrs["editorParams"] = {'tristate': tristate, 'indeterminateValue': indeterminateValue}
    if elementAttributes is not None:
      self._attrs["editorParams"]['elementAttributes'] = elementAttributes
    self._attrs["editorParams"].update(self._attrs["editorParams"].pop('kwargs'))
    return self

  def editor_stars(self, elementAttributes=None, **kwargs):
    """
    Description:
    -----------
    The star editor allows entering of numeric value using a star rating indicator.

    This editor will automatically detect the correct number of stars to use if it is used on the same column as the star formatter.

    Related Pages:
    --------------
    http://tabulator.info/docs/4.5/edit#edit-builtin

    Attributes:
    ----------
    :param elementAttributes: set attributes directly on the star holder elemen
    :param kwargs:
    """
    self._attrs["editor"] = 'star'
    self._attrs["editorParams"] = {}
    if elementAttributes is not None:
      self._attrs["editorParams"]['elementAttributes'] = elementAttributes
    self._attrs["editorParams"].update(self._attrs["editorParams"].pop('kwargs'))
    return self

  def editor_select(self, values, listItemFormatter=None, sortValuesList=None, defaultValue=None, elementAttributes=None,
                    verticalNavigation="hybrid", **kwargs):
    """
    Description:
    -----------
    The select editor creates a dropdown select box to allow the user to select from some predefined options passed into the values property of the editorParams option.

    Related Pages:
    --------------
    http://tabulator.info/docs/4.5/edit#edit-builtin

    Attributes:
    ----------
    :param values: a list of values to be displayed to the user
    :param listItemFormatter: a function that should return the HTML contents for each item in the value list
    :param sortValuesList: if values property is set to true this option can be used to set how the generated list should be sorted
    :param defaultValue: set the value that should be selected by default if the cells value is undefined
    :param elementAttributes: set attributes directly on the input element
    :param verticalNavigation: determine how use of the up/down arrow keys will affect the editor,
    :param kwargs:
    """
    self._attrs["editor"] = 'select'
    self._attrs["editorParams"] = {k: v for k, v in locals().items() if k != 'self'}
    self._attrs["editorParams"].update(self._attrs["editorParams"].pop('kwargs'))
    return self

  def editor_autocomplete(self, values, showListOnEmpty=None, freetext=None, allowEmpty=None, searchFunc=None,
                          listItemFormatter=None, sortValuesList=None, defaultValue=None, elementAttributes=None,
                          verticalNavigation=None, **kwargs):
    """
    Description:
    -----------
    The autocomplete editor allows users to search a list of predefined options passed into the values property of the editorParams option.

    Related Pages:
    --------------
    http://tabulator.info/docs/4.5/edit#edit-builtin

    Attributes:
    ----------
    :param values: a list of values to be displayed to the user
    :param showListOnEmpty: show all values in the list when the input element is empty (default false)
    :param freetext: allow the user to press enter to save a value to the cell that is not in the list (default false)
    :param allowEmpty: allow the user to save an empty value to the cell (default false)
    :param searchFunc: unction to search through array of value objects and return those that match the search term
    :param listItemFormatter: a function that should return the HTML contents for each item in the value list
    :param sortValuesList:  if values property is set to true this option can be used to set how the generated list should be sorted
    :param defaultValue: set the value that should be selected by default if the cells value is undefined
    :param elementAttributes: set attributes directly on the input element
    :param verticalNavigation: determine how use of the up/down arrow keys will affect the editor,
    """
    self._attrs["editor"] = 'autocomplete'
    self._attrs["editorParams"] = {k: v for k, v in locals().items() if k != 'self'}
    self._attrs["editorParams"].update(self._attrs["editorParams"].pop('kwargs'))
    return self

  @property
  def field(self):
    return self._attrs["field"]

  @field.setter
  def field(self, val):
    self._attrs["field"] = val

  def formatter_text(self, **kwargs):
    """
    Description:
    -----------
    The plaintext formater is the default formatter for all cells and will simply dispay the value of the cell as text.

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format

    Attributes:
    ----------
    :param kwargs:
    """
    self._attrs["formatter"] = 'plaintext'
    if kwargs:
      self._attrs["editorParams"] = kwargs
    return self

  def formatter_textarea(self, **kwargs):
    """
    Description:
    -----------
    The textarea formater shows text with carriage returns intact (great for multiline text), this formatter will also adjust the height of rows to fit the cells contents when columns are resized.

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format

    Attributes:
    ----------
    :param kwargs:
    """
    self._attrs["formatter"] = 'textarea'
    if kwargs:
      self._attrs["editorParams"] = kwargs
    return self

  def formatter_html(self, **kwargs):
    """
    Description:
    -----------
    he html formater displays un-sanitized html.

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format

    Attributes:
    ----------
    :param kwargs:
    """
    self._attrs["formatter"] = 'html'
    if kwargs:
      self._attrs["editorParams"] = kwargs
    return self

  def formatter_money(self, decimal=",", thousand=".", precision=False, symbol=None, symbolAfter=None, **kwargs):
    """
    Description:
    -----------
    The money formater formats a number into currency notation (eg. 1234567.8901 -> 1,234,567.89).

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format

    Attributes:
    ----------
    :param decimal: Symbol to represent the decimal point (default ".")
    :param thousand: Symbol to represent the thousands seperator (default ",")
    :param precision: the number of decimals to display (default is 2), setting this value to false will display however many decimals are provided with the number
    :param symbol: currency symbol (no default)
    :param symbolAfter: position the symbol after the number (default false)
    :param kwargs:
    """
    self._attrs["formatter"] = 'formatterParams'
    if kwargs:
      self._attrs["editorParams"] = kwargs
    return self

  def formatter_icon(self, css=None, tags=None, **kwargs):
    """

    :param css:
    :param tags:
    :param kwargs:
    """
    self._report.jsImports.add('tabulator-icons')
    self._attrs["formatter"] = 'icon'
    self._attrs["formatterParams"] = {}
    if css is not None:
      self._attrs["css"] = css
    if tags is not None:
      self._attrs["tags"] = tags
    for k, v in kwargs.items():
      self._attrs["formatterParams"][k] = v
    return self

  def formatter_image(self, height=None, width=None, **kwargs):
    """
    Description:
    -----------
    The image formater creates an img element with the src set as the value. (triggers the normalizeHeight function on the row on image load).

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format

    Attributes:
    ----------
    :param height: a CSS value for the height of the image
    :param width: a CSS value for the width of the image
    :param kwargs:
    """
    self._attrs["formatter"] = 'image'
    formatParams = {}
    if height is not None:
      formatParams['height'] = height
    if width is not None:
      formatParams['width'] = width
    self._attrs["formatterParams"] = formatParams
    for k, v in kwargs.items():
      self._attrs["formatterParams"][k] = v
    return self

  def formatter_link(self, label=None, url=None, target='_blank', urlPrefix=None, labelField=None, urlField=None, **kwargs):
    """
    Description:
    -----------
    The link formater renders data as an anchor with a link to the given value (by default the value will be used as both the url and the label of the tag).

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format

    Attributes:
    ----------
    :param label: a string representing the lable, or a function which must return the string for the label, the function is passed the Cell Component as its first argument
    :param url:  a string representing the url, or a function which must return the string for the url, the function is passed the Cell Component as its first argument
    :param target: a string representing the value of the anchor tags target artibute (eg. set to "_blank" to open link in new tab)
    :param urlPrefix: a prefix to put before the url value (eg. to turn a emaill address into a clickable mailto link you should set this to "mailto:")
    :param labelField: the field in the row data that should be used for the link lable
    :param urlField: the field in the row data that should be used for the link url
    :param kwargs:
    """
    self._attrs["formatterParams"] = {k: v for k, v in locals().items() if k != 'self'}
    self._attrs["formatterParams"].update(self._attrs["formatterParams"].pop('kwargs'))
    self._attrs["formatter"] = 'link'
    return self

  def formatter_datetime(self, inputFormat="YYYY-MM-DD", outputFormat="YYYY-MM-DD", invalidPlaceholder="(invalid date)", **kwargs):
    """
    Description:
    -----------
    The datetime formater transforms on format of date or time into another.

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format

    Attributes:
    ----------
    :param inputFormat:
    :param outputFormat:
    :param invalidPlaceholder:
    :param kwargs:
    """
    self._attrs["formatter"] = 'datetime'
    self._attrs["formatterParams"] = {"inputFormat": inputFormat, "outputFormat": outputFormat, "invalidPlaceholder": invalidPlaceholder}
    if kwargs:
      self._attrs["formatterParams"].update(kwargs)
    return self

  def formatter_tickcross(self, allowEmpty=True, allowTruthy=True, tickElement="<i class='fa fa-check'></i>",
                          crossElement="<i class='fa fa-times'></i>", **kwargs):
    """
    Description:
    -----------
    The tickCross formatter displays a green tick if the value is (true|'true'|'True'|1) and a red cross if not.

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format

    Attributes:
    ----------
    :param allowEmpty: set to true to cause empty values (undefined, null, "") to display an empty cell instead of a cross (default false)
    :param allowTruthy: set to true to allow any truthy value to show a tick (default false)
    :param tickElement: custom HTML for the tick element, if set to false the tick element will not be shown (it will only show crosses)
    :param crossElement: custom HTML for the cross element, if set to false the cross element will not be shown (it will only show ticks)
    :param kwargs:
    """
    self._attrs["formatter"] = 'tickCross'
    self._attrs["formatterParams"] = {'allowEmpty': allowEmpty, 'allowTruthy': allowTruthy, 'tickElement': tickElement,
                                      'crossElement': crossElement}
    if kwargs:
      self._attrs["formatterParams"].update(kwargs)
    return self

  def formatter_color(self, **kwargs):
    """
    Description:
    -----------
    The color formater sets the background colour of the cell to the value. The cell's value can be any valid CSS color eg. #ff0000, #f00, rgb(255,0,0), red, rgba(255,0,0,0), hsl(0, 100%, 50%)

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format
    """
    self._attrs["formatter"] = 'color'
    if kwargs:
      self._attrs["formatterParams"] = kwargs
    return self

  def formatter_star(self, starts, **kwargs):
    """
    Description:
    -----------
    The star formater displays a graphical star rating based on integer values.

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format

    Attributes:
    ----------
    :param starts: maximum number of stars to be displayed (default 5)
    """
    self._attrs["formatter"] = 'star'
    formatParams = {"starts": starts}
    for k, v in kwargs.items():
      formatParams[k] = v
    self._attrs["formatterParams"] = formatParams
    return self

  def formatter_password(self, css=None, **kwargs):
    """
    Description:
    -----------
    Change the content of the cell to ****

    Attributes:
    ----------
    :param css: Dictionary. The CSS attributes for the cell (Optional)
    :param kwargs:
    """
    self._report.jsImports.add('tabulator-inputs')
    self._attrs["formatter"] = 'password'
    formatParams = {}
    if css is not None:
      formatParams['css'] = css
    for k, v in kwargs.items():
      formatParams[k] = v
    return self

  def formatter_progress(self, min, max, color, legend, legendColor, legendAlign, **kwargs):
    """

    :param min:
    :param max:
    :param color:
    :param legend:
    :param legendColor:
    :param legendAlign:
    :param kwargs:
    """
    self._attrs["formatter"] = 'progress'
    if kwargs:
      self._attrs["formatterParams"] = kwargs
    return self

  def formatter_label_thresholds(self, thresholds, labels, css=None, **kwargs):
    """
    Description:
    -----------
    Set a label based on a list of values

    Attributes:
    ----------
    :param thresholds: List. The different values to compare to deduce the category
    :param labels: List. The resulting category
    :param css: Dictionary. The CSS attributes for the cell (Optional)
    :param kwargs:
    """
    self._report.jsImports.add('tabulator-inputs')
    self._attrs["formatter"] = 'labelThresholds'
    formatParams = {'thresholds': thresholds, 'labels': labels}
    if css is not None:
      formatParams['css'] = css
    if kwargs:
      self._attrs["formatterParams"].update(kwargs)
    return self

  def formatter_label_thresholds_pivot(self, pivot, thresholds, labels, css=None, **kwargs):
    """
    Description:
    -----------
    Set a label based on a list of values from another column

    Attributes:
    ----------
    :param pivot: String. The column name to use to get the data to lookup from te row
    :param thresholds: List. The different values to compare to deduce the category
    :param labels: List. The resulting category
    :param css: Dictionary. The CSS attributes for the cell (Optional)
    :param kwargs:
    """
    self._report.jsImports.add('tabulator-inputs')
    self._attrs["formatter"] = 'flagThresholdsPivot'
    formatParams = {'thresholds': thresholds, 'labels': labels, 'pivot': pivot}
    if css is not None:
      formatParams['css'] = css
    if kwargs:
      self._attrs["formatterParams"].update(kwargs)
    return self

  def formatter_number(self, decimal=None, thousand=None, precision=None, symbol=None, format=None, css=None, **kwargs):
    """

    :param decimal: String. decimal point separator default "."
    :param thousand: String. thousands separator default ","
    :param precision: Integer. decimal places default 0
    :param symbol: default currency symbol is ''
    :param format:
    :param css: Dictionary. The CSS attributes for the cell (Optional)
    :param kwargs:
    """
    self._report.jsImports.add('tabulator-numbers')
    self._attrs["formatter"] = 'numbers'
    self._attrs["formatterParams"] = {k: v for k, v in locals().items() if k != 'self'}
    self._attrs["formatterParams"].update(self._attrs["formatterParams"].pop('kwargs'))
    return self

  def formatter_number_format(self, decimal, thousand, precision, symbol, format, colors=None, threshold=0, css=None, **kwargs):
    """

    :param decimal: String. decimal point separator default "."
    :param thousand: String. thousands separator default ","
    :param precision: Integer. decimal places default 0
    :param symbol: default currency symbol is ''
    :param format: String. "%s%v" controls output: %s = symbol, %v = value/number (can be object: see below)
    :param css: Dictionary. The CSS attributes for the cell (Optional)
    :param kwargs:
    """
    self._report.jsImports.add('tabulator-numbers')
    if colors is None:
      colors = [self._report.theme.danger[1], self._report.theme.success[1]]
    self._attrs["formatter"] = 'numbersFormat'
    self._attrs["formatterParams"] = {k: v for k, v in locals().items() if k != 'self'}
    self._attrs["formatterParams"].update(self._attrs["formatterParams"].pop('kwargs'))
    return self

  def formatter_number_difference(self, decimal=None, thousand=None, precision=None, symbol=None, format=None,
                                  colors=None, threshold=0, css=None, **kwargs):
    """

    :param decimal: String. decimal point separator default "."
    :param thousand: String. thousands separator default ","
    :param precision: Integer. decimal places default 0
    :param symbol: default currency symbol is ''
    :param format: String. "%s%v" controls output: %s = symbol, %v = value/number (can be object: see below)
    :param colors: List. Color before and after the threshold (default red and green according to the theme)
    :param threshold: Integer. The threshold number
    :param css: Dictionary. The CSS attributes for the cell (Optional)
    :param kwargs:
    """
    self._report.jsImports.add('tabulator-numbers')
    if colors is None:
      colors = [self._report.theme.danger[1], self._report.theme.success[1]]
    self._attrs["formatter"] = 'numbersDifference'
    self._attrs["formatterParams"] = {k: v for k, v in locals().items() if k != 'self'}
    self._attrs["formatterParams"].update(self._attrs["formatterParams"].pop('kwargs'))
    return self

  def formatter_number_thresholds(self, thresholds, css, **kwargs):
    """

    :param thresholds:
    :param css:
    :param kwargs:
    """
    self._report.jsImports.add('tabulator-numbers')
    self._attrs["formatter"] = 'numbersThreshold'
    self._attrs["formatterParams"] = {'thresholds': thresholds, 'css': css}
    self._attrs["formatterParams"].update(self._attrs["formatterParams"].pop('kwargs'))
    return self

  def formatter_number_thresholds_pivot(self, pivot, thresholds, css, **kwargs):
    """

    :param pivot:
    :param thresholds:
    :param css:
    :param kwargs:
    :return:
    """
    self._report.jsImports.add('tabulator-numbers')
    self._attrs["formatter"] = 'numbersThresholdPivot'
    self._attrs["formatterParams"] = {'thresholds': thresholds, 'css': css, 'pivot': pivot}
    self._attrs["formatterParams"].update(self._attrs["formatterParams"].pop('kwargs'))
    return self

  def formatter_intensity(self, steps, colors, intensity, css=None, **kwargs):
    """

    :param steps:
    :param colors:
    :param intensity: String, The column used to deduce the intensity. Default the cell value
    :param css:
    :param kwargs:
    """
    self._report.jsImports.add('tabulator-numbers')
    self._attrs["formatter"] = 'numbersIntensity'
    self._attrs["formatterParams"] = {'steps': steps, 'colors': colors, 'intensity': intensity}
    if css is not None:
      self._attrs["formatterParams"]['css'] = css
    self._attrs["formatterParams"].update(self._attrs["formatterParams"].pop('kwargs'))
    return self

  def formatter_quality(self, steps, colors, intensity, quality, css=None, **kwargs):
    """

    :param steps:
    :param colors:
    :param intensity:
    :param quality:
    :param css:
    :param kwargs:
    """
    self._report.jsImports.add('tabulator-numbers')
    self._attrs["formatter"] = 'numbersIntensity'
    self._attrs["formatterParams"] = {'steps': steps, 'colors': colors, 'intensity': intensity, 'quality': quality}
    if css is not None:
      self._attrs["formatterParams"]['css'] = css
    self._attrs["formatterParams"].update(self._attrs["formatterParams"].pop('kwargs'))
    return self

  def formatter_lookup(self, data, **kwargs):
    """
    Description:
    -----------
    The lookup formater looks up the value to display from a object passed into the formatterParams property, if not present it displays the current cell value

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format

    Attributes:
    ----------
    :param data: Dictionary for the lookup
    """
    self._attrs["formatter"] = 'lookup'
    self._attrs['formatterParams'] = data
    if kwargs:
      self._attrs["formatterParams"].update(kwargs)
    return self

  @packageImport('tabulator-inputs')
  def formatter_lookup_pivot(self, lookups, pivot, css=None, **kwargs):
    """
    Description:
    -----------
    Set a label based on a list of values

    Attributes:
    ----------
    :param lookups:
    :param pivot:
    :param css: Dictionary. The CSS attributes for the cell (Optional)
    """
    self._attrs["formatter"] = 'lookupPivot'
    formatParams = {'lookups': lookups, "pivot": pivot}
    if css is not None:
      formatParams['css'] = css
    for k, v in kwargs.items():
      formatParams[k] = v
    self._attrs['formatterParams'] = formatParams
    return self

  def formatter_buttonTick(self, **kwargs):
    """
    Description:
    -----------
    The buttonTick formater displays a tick icon on each row (for use as a button)

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format
    """
    self._attrs["formatter"] = 'buttonTick'
    if kwargs:
      self._attrs["editorParams"] = kwargs
    return self

  def formatter_buttonCross(self, **kwargs):
    """
    Description:
    -----------
    The buttonCross formater displays a cross icon on each row (for use as a button)

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format
    """
    self._attrs["formatter"] = 'buttonCross'
    if kwargs:
      self._attrs["editorParams"] = kwargs
    return self

  def formatter_rownum(self, **kwargs):
    """
    Description:
    -----------
    The rownum formatter shows an incrementing row number for each row as it is displayed

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format
    """
    self._attrs["formatter"] = 'rownum'
    if kwargs:
      self._attrs["editorParams"] = kwargs
    return self

  def formatter_handle(self, **kwargs):
    """
    Description:
    -----------
    The handle formatter fills the cell with hamburger bars, to be used as a row handle

    Related Pages:
    --------------
    http://tabulator.info/docs/4.1/format
    """
    self._attrs["formatter"] = 'handle'
    if kwargs:
      self._attrs["editorParams"] = kwargs
    return self

  def formatter(self, formatter, formatterParams, moduleAlias):
    """

    :param formatter:
    :param formatterParams:
    :param moduleAlias:
    """
    self._report.jsImports.add(moduleAlias)
    self._attrs["formatter"] = formatter
    self._attrs['formatterParams'] = formatterParams
    return self

  @property
  def frozen(self):
    return self._attrs["frozen"]

  @frozen.setter
  def frozen(self, val):
    self._attrs["frozen"] = val

  @property
  def headerVertical(self):
    return self._attrs["headerVertical"]

  @headerVertical.setter
  def headerVertical(self, val):
    self._attrs["headerVertical"] = val

  @property
  def headerSort(self):
    return self._attrs["headerSort"]

  @headerSort.setter
  def headerSort(self, val):
    self._attrs["headerSort"] = val

  @property
  def headerVisible(self):
    return self._attrs["headerVisible"]

  @headerVisible.setter
  def headerVisible(self, val):
    self._attrs["headerVisible"] = val

  @property
  def sorter(self):
    """
    By default Tabulator will attempt to guess which sorter should be applied to a column based on the data contained in the first row.

    http://tabulator.info/examples/4.5#sorters

    :rtype: EnumSorter
    """
    return self.sub_data("sorter", EnumSorter)

  @property
  def width(self):
    return self._attrs["width"]

  @width.setter
  def width(self, val):
    self._attrs["width"] = val

  @property
  def minwidth(self):
    return self._attrs["minwidth"]

  @minwidth.setter
  def minwidth(self, val):
    self._attrs["minwidth"] = val

  @property
  def widthGrow(self):
    return self._attrs["widthGrow"]

  @widthGrow.setter
  def widthGrow(self, val):
    self._attrs["widthGrow"] = val

  @property
  def responsive(self):
    return self._attrs["responsive"]

  @responsive.setter
  def responsive(self, val):
    self._attrs["responsive"] = val

  @property
  def resizable(self):
    return self._attrs["resizable"]

  @resizable.setter
  def resizable(self, val):
    self._attrs["resizable"] = val

  @property
  def title(self):
    return self._attrs["title"]

  @title.setter
  def title(self, val):
    self._attrs["title"] = val

  @property
  def titleFormatter(self):
    return self._attrs["titleFormatter"]

  @titleFormatter.setter
  def titleFormatter(self, val):
    self._attrs["titleFormatter"] = val

  @property
  def topCalc(self):
    return self._attrs["topCalc"]

  @topCalc.setter
  def topCalc(self, val):
    self._attrs["topCalc"] = val

  @property
  def validator(self):
    return self._attrs["validator"]

  @validator.setter
  def validator(self, val):
    self._attrs["validator"] = val


class TableConfig(DataClass):

  @property
  def ajaxURL(self):
    return self._attrs["ajaxURL"]

  @ajaxURL.setter
  def ajaxURL(self, val):
    self._attrs["ajaxURL"] = val

  @property
  def ajaxProgressiveLoad(self):
    return self._attrs["ajaxProgressiveLoad"]

  @ajaxProgressiveLoad.setter
  def ajaxProgressiveLoad(self, val):
    self._attrs["ajaxProgressiveLoad"] = val

  @property
  def autoColumns(self):
    return self._attrs["autoColumns"]

  @autoColumns.setter
  def autoColumns(self, val):
    self._attrs["autoColumns"] = val

  @property
  def addRowPos(self):
    return self._attrs["addRowPos"]

  @addRowPos.setter
  def addRowPos(self, val):
    self._attrs["addRowPos"] = val

  @property
  def clipboard(self):
    return self._attrs["clipboard"]

  @clipboard.setter
  def clipboard(self, val):
    self._attrs["clipboard"] = val

  @property
  def clipboardPasteAction(self):
    return self._attrs["clipboardPasteAction"]

  @clipboardPasteAction.setter
  def clipboardPasteAction(self, val):
    self._attrs["clipboardPasteAction"] = val

  @property
  def columns(self):
    """

    :rtype: Column
    """
    return self.sub_data_enum("columns", Column)

  @property
  def columns_group(self):
    return self.sub_data_enum("columns", ColumnsGroup)

  @property
  def columnVertAlign(self):
    """

    To align header contents to bottom of cell
    columnVertAlign = "bottom"
    :return:
    """
    return self._attrs["columnVertAlign"]

  @columnVertAlign.setter
  def columnVertAlign(self, val):
    self._attrs["columnVertAlign"] = val

  @property
  def data(self):
    return self._attrs["data"]

  @data.setter
  def data(self, val):
    self._attrs["data"] = val

  @property
  def groupBy(self):
    return self._attrs["groupBy"]

  @groupBy.setter
  def groupBy(self, val):
    self._attrs["groupBy"] = val

  @property
  def groupValues(self):
    return self._attrs["groupValues"]

  @groupValues.setter
  def groupValues(self, val):
    self._attrs["groupValues"] = val

  @property
  def height(self):
    return self._attrs["height"]

  @height.setter
  def height(self, val):
    if isinstance(val, int):
      val = "%spx" % val
    self._attrs["height"] = val

  @property
  def history(self):
    return self._attrs["history"]

  @history.setter
  def history(self, val):
    self._attrs["history"] = val

  @property
  def lang(self):
    return self._attrs["lang"]

  @lang.setter
  def lang(self, val):
    self._attrs["lang"] = val

  @property
  def layout(self):
    """

    :rtype: EnumLayout
    """
    return self.sub_data("layout", EnumLayout)

  @property
  def movableColumns(self):
    return self._attrs["movableColumns"]

  @movableColumns.setter
  def movableColumns(self, val):
    self._attrs["movableColumns"] = val

  @property
  def movableRows(self):
    return self._attrs["movableRows"]

  @movableRows.setter
  def movableRows(self, val):
    self._attrs["movableRows"] = val

  @property
  def movableRowsConnectedTables(self):
    return self._attrs["movableRowsConnectedTables"]

  @movableRowsConnectedTables.setter
  def movableRowsConnectedTables(self, val):
    self._attrs["movableRowsConnectedTables"] = val

  @property
  def movableRowsReceiver(self):
    return self._attrs["movableRowsReceiver"]

  @movableRowsReceiver.setter
  def movableRowsReceiver(self, val):
    self._attrs["movableRowsReceiver"] = val

  @property
  def movableRowsSender(self):
    return self._attrs["movableRowsSender"]

  @movableRowsSender.setter
  def movableRowsSender(self, val):
    self._attrs["movableRowsSender"] = val

  @property
  def pagination(self):
    return self._attrs["pagination"]

  @pagination.setter
  def pagination(self, val):
    self._attrs["pagination"] = val

  @property
  def paginationSize(self):
    return self._attrs["paginationSize"]

  @paginationSize.setter
  def paginationSize(self, val):
    self._attrs["paginationSize"] = val

  @property
  def paginationSizeSelector(self):
    return self._attrs["paginationSizeSelector"]

  @paginationSizeSelector.setter
  def paginationSizeSelector(self, val):
    self._attrs["paginationSizeSelector"] = val

  @property
  def persistenceID(self):
    return self._attrs["persistenceID"]

  @persistenceID.setter
  def persistenceID(self, val):
    self._attrs["persistenceID"] = val

  @property
  def persistence(self):
    return self.sub_data("persistence", Persistence)

  @property
  def placeholder(self):
    return self._attrs["placeholder"]

  @placeholder.setter
  def placeholder(self, val):
    self._attrs["placeholder"] = val

  @property
  def printAsHtml(self):
    return self._attrs["printAsHtml"]

  @printAsHtml.setter
  def printAsHtml(self, val):
    self._attrs["printAsHtml"] = val

  @property
  def printHeader(self):
    return self._attrs["printHeader"]

  @printHeader.setter
  def printHeader(self, val):
    self._attrs["printHeader"] = val

  @property
  def printFooter(self):
    return self._attrs["printFooter"]

  @printFooter.setter
  def printFooter(self, val):
    self._attrs["printFooter"] = val

  @property
  def reactiveData(self):
    return self._attrs["reactiveData"]

  @reactiveData.setter
  def reactiveData(self, val):
    self._attrs["reactiveData"] = val

  @property
  def responsiveLayout(self):
    return self._attrs["responsiveLayout"]

  @responsiveLayout.setter
  def responsiveLayout(self, val):
    self._attrs["responsiveLayout"] = val

  @property
  def resizableColumns(self):
    return self._attrs["resizableColumns"]

  @resizableColumns.setter
  def resizableColumns(self, val):
    self._attrs["resizableColumns"] = val

  @property
  def selectable(self):
    return self._attrs["selectable"]

  @selectable.setter
  def selectable(self, val):
    self._attrs["selectable"] = val


class TableTreeConfig(TableConfig):

  @property
  def dataTree(self):
    return self._attrs["dataTree"]

  @dataTree.setter
  def dataTree(self, val):
    self._attrs["dataTree"] = val

  @property
  def dataTreeStartExpanded(self):
    return self._attrs["dataTreeStartExpanded"]

  @dataTreeStartExpanded.setter
  def dataTreeStartExpanded(self, val):
    self._attrs["dataTreeStartExpanded"] = val


if __name__ == '__main__':
  t = TableConfig({})
  t.layout.fitColumns()
  t.layout.fitDataFill()

  c = t.columns
  c.sorter.number()
  c.title = "test"
  c.formatter.color()
  c.editor_select([1, 2, 4])
  print(t)
