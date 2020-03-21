
from epyk.core.html import Html

from epyk.core.js.packages import JsTabulator

from epyk.core.data import DataClass
from epyk.core.data import DataEnum

# The list of CSS classes
# from epyk.core.css.styles import CssGrpClsTable


class Table(Html.Html):
  name, category, callFnc = 'Table', 'Tables', 'table'
  __reqCss, __reqJs = ['datatables'], ['datatables']

  def __init__(self, report, records, width, height, htmlCode, options, profile):
    data, columns, self.__config = [], [], None
    super(Table, self).__init__(report, [], code=htmlCode, css_attrs={"width": width, "height": height}, profile=profile)
    if records is not None:
      self.config.data = records

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

  def get_column(self, by_title):
    for c in self.config._attrs.get('columns', []):
      if c.title == by_title:
        return c

    return None

  def build(self, data=None, options=None, profile=False):
    print(self.config)
    return 'var %s =  new Tabulator("%s", %s)' % (self.tableId, self.dom.varId, self.config)

  def __str__(self):
    self._report._props.setdefault('js', {}).setdefault("builders", []).append(self.refresh())
    return "<div %s></div>" % (self.get_attrs(pyClassNames=self.style.get_classes()))


class EnumLayout(DataEnum):

  def fitDataStretch(self): return self.set("fitDataStretch")

  def fitColumns(self): return self.set("fitColumns")

  def fitDataStretch(self): return self.set("fitDataStretch")

  def fitDataFill(self): return self.set("fitDataFill")


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


class EnumEditor(DataEnum):

  def autocomplete(self):
    """

    http://tabulator.info/examples/4.5#editable
    """
    return self.set()

  def input(self):
    """

    http://tabulator.info/examples/4.5#editable
    """
    return self.set()

  def select(self):
    """

    http://tabulator.info/examples/4.5#editable
    """
    return self.set()

  def star(self):
    """
    """
    return self.set()

  def true(self):
    """

    http://tabulator.info/examples/4.5#editable

    :return:
    """
    return self.set()


class EnumFormatter(DataEnum):

  def money(self):
    """
    Formats a number into a currency notation (eg. 1234567.8901 -> 1,234,567.89)

    http://tabulator.info/examples/4.5#formatters
    """
    return self.set()

  def image(self):
    """
    Creates an img element with the src set as the value. (triggers the normalizeHeight function on the row on image load)

    http://tabulator.info/examples/4.5#formatters
    """
    return self.set()

  def link(self):
    """
    Renders data as an anchor with a link to the given value

    http://tabulator.info/examples/4.5#formatters
    """
    return self.set()

  def textarea(self):
    """

    """
    return self.set()

  def tick(self):
    """
    Displays a green tick if the value is (true|'true'|'True'|1) and an empty cell if not

    http://tabulator.info/examples/4.5#formatters
    """
    return self.set()

  def tickCross(self):
    """
    Displays a green tick if the value is (true|'true'|'True'|1) and a red cross if not

    http://tabulator.info/examples/4.5#formatters
    """
    return self.set()

  def color(self):
    """
    Sets the background color of the cell to the value.
    Can be any valid css colour eg. #ff0000, #f00, rgb(255,0,0), red, rgba(255,0,0,0), hsl(0, 100%, 50%)

    http://tabulator.info/examples/4.5#formatters
    """
    return self.set()

  def star(self):
    """
    Displays a graphical 0-5 star rating based on integer values from 0-5

    http://tabulator.info/examples/4.5#formatters
    """
    return self.set()

  def progress(self):
    """
    Displays a progress bar that fills the cell from left to right, using values 0-100 as a percentage of width

    http://tabulator.info/examples/4.5#formatters
    """
    return self.set()

  def buttonTick(self):
    """
    displays a tick icon on each row (for use as a button)

    http://tabulator.info/examples/4.5#formatters
    """
    return self.set()

  def buttonCross(self):
    """
    Displays a cross icon on each row (for use as a button)

    http://tabulator.info/examples/4.5#formatters
    """
    return self.set()

  def rownum(self):
    """
    Shows an incrementing row number for each row.

    http://tabulator.info/examples/4.5#formatters
    """
    return self.set()


class FormatterParams(DataClass):

  @property
  def color(self):
    return self._attrs["color"]

  @color.setter
  def color(self, val):
    self._attrs["color"] = val

  @property
  def stars(self):
    return self._attrs["stars"]

  @stars.setter
  def stars(self, val):
    self._attrs["stars"] = val


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


class EditorParams(DataClass):

  @property
  def allowEmpty(self):
    return self._attrs["allowEmpty"]

  @allowEmpty.setter
  def allowEmpty(self, val):
    self._attrs["allowEmpty"] = val

  @property
  def showListOnEmpty(self):
    return self._attrs["showListOnEmpty"]

  @showListOnEmpty.setter
  def showListOnEmpty(self, val):
    self._attrs["showListOnEmpty"] = val

  @property
  def values(self):
    return self._attrs["values"]

  @values.setter
  def values(self, val):
    self._attrs["values"] = val


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
  def editable(self):
    return self._attrs["editable"]

  @editable.setter
  def editable(self, val):
    self._attrs["editable"] = val

  def editor_autocomplete(self, allowEmpty=True, showListOnEmpty=True, values=True):
    """

    :param allowEmpty:
    :param showListOnEmpty:
    :param values:
    """
    self.editor.autocomplete()
    self.editorParams.allowEmpty = allowEmpty
    self.editorParams.showListOnEmpty = showListOnEmpty
    self.editorParams.values = values
    return self

  def editor_select(self, values):
    """

    :param values:
    """
    self.editor.select()
    self.editorParams.values = values
    return self

  @property
  def editor(self):
    """

    :rtype: EnumEditor
    """
    return self.has_attribute(EnumEditor)

  @property
  def editorParams(self):
    return self.sub_data("editorParams", EditorParams)

  @property
  def field(self):
    return self._attrs["field"]

  @field.setter
  def field(self, val):
    self._attrs["field"] = val

  @property
  def formatter(self):
    """

    :rtype: EnumFormatter
    """
    return self.has_attribute(EnumFormatter)

  def formatter_star(self, starts):
    """

    :param starts:
    """
    self.formatter.star()
    self.formatterParams.stars = starts
    return self

  def formatter_progress(self, colors):
    """

    :param colors:
    """
    self.formatter.progress()
    self.formatterParams.color = colors
    return self

  @property
  def formatterParams(self):
    """

    :rtype: FormatterParams
    """
    return self.has_attribute(FormatterParams)

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
