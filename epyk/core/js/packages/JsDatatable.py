"""
Javascript Interface to the Datatable Module

https://datatables.net/reference/api/
"""

from epyk.core.js import JsUtils
from epyk.core.js.primitives import JsObjects
from epyk.core.js.packages import JsQuery
from epyk.core.js.packages import JsPackage


class SelectAPI(JsPackage):
  """

  """

  def blurable(self):
    """
    Get the blurable state for the table

    Documentation
    https://datatables.net/reference/api/select.blurable()

    :return:
    """
    return JsObjects.JsBoolean.JsBoolean("%s.blurable()" % self._selector)

  def info(self, jsFlag=None):
    """
    Get / set the information summary display state.

    Documentation
    https://datatables.net/reference/api/select.info()

    :param jsFlag: Value to set for the information summary display state - true to enable, false to disable.
    :return:
    """
    if jsFlag is None:
      return JsObjects.JsBoolean.JsBoolean("%s.info()" % self._selector)

    return JsObjects.JsObject.JsObject("%s.info(%s)" % (self._selector, JsUtils.jsConvertData(jsFlag, None)))

  def items(self):
    """
    Get / set the items that Select will select based on user interaction (rows, columns or cells).

    Documentation
    https://datatables.net/reference/api/select.items()

    :return:
    """
    return JsObjects.JsString.JsString("%s.items()" % self._selector)

  def selector(self):
    """
    Get the current item selector string applied to the table.

    Documentation
    https://datatables.net/reference/api/select.selector()

    :return:
    """
    return JsObjects.JsString.JsString("%s.selector()" % self._selector)

  def style(self):
    """
    Get / set the style by which the end user can select items in the table.

    Documentation
    https://datatables.net/reference/api/select.style()

    :return:
    """
    return JsObjects.JsString.JsString("%s.style()" % self._selector)


class CellAPI(JsPackage):
  """

  """
  def deselect(self):
    """

    Documentation
    https://datatables.net/reference/api/column().deselect()

    :return:
    """
    self._js.append("deselect()")
    return self

  def select(self):
    """

    Documentation
    https://datatables.net/reference/api/cell().select()

    :return:
    """
    self._js.append("select()")
    return self

  def render(self):
    """
    Get rendered data for a cell

    Documentation
    https://datatables.net/reference/api/cell().render()

    :return:
    """

  def nodes(self):
    """

    Documentation
    https://datatables.net/reference/api/cell().node()

    :return:
    """
    self._js.append("nodes()")
    return self

  def jquery_nodes(self):
    """
    Get the cell nodes for the selected column.

    Documentation
    https://datatables.net/reference/api/column().nodes()

    :return:
    """
    self.nodes()
    self._js.append("nodes().to$()")
    return JsQuery.JQuery(jqId=self.toStr())

  def invalidate(self):
    """

    Documentation
    https://datatables.net/reference/api/cell().invalidate()

    :return:
    """

  def index(self):
    """

    Documentation
    https://datatables.net/reference/api/cell().index()

    :return:
    """

  def cache(self):
    """
    Get cached data of the cache type specified

    Documentation
    https://datatables.net/reference/api/cell().cache()

    :return:
    """

  def data(self):
    """
    Get / set data for the selected cell.

    Documentation
    https://datatables.net/reference/api/cell().data()

    :return:
    """
    self._js.append("data()")
    return self

  def focus(self):
    """
    Focus on a cell.

    Documentation
    https://datatables.net/reference/api/cell().focus()

    :return:
    """
    self._js.append("focus()")
    return self

  def blur(self):
    """
    Blur focus from the table.

    Documentation
    https://datatables.net/reference/api/cell.blur()

    :return:
    """
    self._js.append("blur()")
    return self


class ColumnAPI(JsPackage):
  """

  """
  def deselect(self):
    """

    Documentation
    https://datatables.net/reference/api/column().deselect()

    :return:
    """
    self._js.append("deselect()")
    return self

  def select(self):
    """

    Documentation
    https://datatables.net/reference/api/column().select()

    :return:
    """
    self._js.append("select()")
    return self

  def cache(self):
    """
    Get the DataTables cached data for the selected column.

    Documentation
    https://datatables.net/reference/api/column().cache()

    :return:
    """

  def data(self):
    """
    Get the data for the cells in the selected column.

    Documentation
    https://datatables.net/reference/api/column().data()

    :return:
    """

  def dataSrc(self):
    """
    Get the data source property for the selected column.

    Documentation
    https://datatables.net/reference/api/column().dataSrc()

    :return:
    """

  def footer(self):
    """
    Get the footer node for the selected column.

    Documentation
    https://datatables.net/reference/api/column().footer()

    :return:
    """

  def header(self):
    """
    Get the header node for the selected column.

    Documentation
    https://datatables.net/reference/api/column().header()

    :return:
    """

  def index(self):
    """
    Get the column index of the selected column.

    Documentation
    https://datatables.net/reference/api/column().index()

    :return:
    """

  def nodes(self):
    """
    Get the cell nodes for the selected column.

    Documentation
    https://datatables.net/reference/api/column().nodes()

    :return:
    """
    self._js.append("nodes()")
    return self

  def jquery_nodes(self):
    """
    Get the cell nodes for the selected column.

    Documentation
    https://datatables.net/reference/api/column().nodes()

    :return:
    """
    self.nodes()
    self._js.append("to$()")
    return JsQuery.JQuery(jqId=self.toStr())

  def order(self):
    """
    Order the table by the selected column.

    Documentation
    https://datatables.net/reference/api/column().order()

    :return:
    """

  def search(self, jsData):
    """
    Search for data in the selected column.

    Documentation
    https://datatables.net/reference/api/column().search()

    :return:
    """
    self._js.append("search(%s)" % JsUtils.jsConvertData(jsData, None))
    return self

  def visible(self):
    """
    Get / set the visibility of a single selected column.

    Documentation
    https://datatables.net/reference/api/column().visible()

    :return:
    """

  def draw(self, target=None):
    """
    Redraw the DataTables in the current context, optionally updating ordering, searching and paging as required.

    Documentation
    https://datatables.net/reference/api/draw()

    :return:
    """
    if target is not None:
      self._js.append("draw(%s)" % JsUtils.jsConvertData(target, None))
    else:
      self._js.append("draw()")
    return self


class RowAPI(JsPackage):
  """

  """
  def deselect(self):
    """

    Documentation
    https://datatables.net/reference/api/row().deselect()

    :return:
    """
    self._js.append("deselect()")
    return self

  def select(self):
    """

    Documentation
    https://datatables.net/reference/api/row().select()

    :return:
    """
    self._js.append("select()")
    return self

  def scrollTo(self, animate=True):
    """
    Redraw the table's scrolling display to show the row selected by the row() method.

    Documentation
    https://datatables.net/reference/api/row().scrollTo()

    :param animate: Animate the scroll (true) or not (false).
    :return:
    """
    self._js.append("scrollTo()")
    return self

  def cache(self):
    """
    Get the DataTables cached data for the selected row.

    Documentation
    https://datatables.net/reference/api/row().cache()

    :return:
    """

  def child(self):
    """
    Row child method namespace.

    Documentation
    https://datatables.net/reference/api/row().child

    :return:
    """

  def data(self):
    """
    Get / set the data for the selected row.

    Documentation
    https://datatables.net/reference/api/row().data()

    :return:
    """

  def id(self):
    """
    Get the id of the selected row.

    Documentation
    https://datatables.net/reference/api/row().id()

    :return:
    """

  def index(self):
    """
    Get the row index of the selected row.

    Documentation
    https://datatables.net/reference/api/row().index()

    :return:
    """

  def invalidate(self):
    """
    Invalidate the data held in DataTables for the selected row.

    Documentation
    https://datatables.net/reference/api/row().invalidate()

    :return:
    """

  def node(self):
    """
    Get the row TR node for the selected row.

    Documentation
    https://datatables.net/reference/api/row().node()

    :return:
    """
    self._js.append("node()")
    return self

  def jquery_node(self):
    """
    Get the cell nodes for the selected column.

    Documentation
    https://datatables.net/reference/api/column().nodes()

    :return:
    """
    self.node()
    self._js.append("to$()")
    return JsQuery.JQuery(jqId=self.toStr())

  def remove(self):
    """
    Delete the selected row from the DataTable.

    Documentation
    https://datatables.net/reference/api/row().remove()

    :return:
    """

  def add(self, jsData):
    """
    Add a new row to the table.

    Documentation
    https://datatables.net/reference/api/row.add()

    :return:
    """

  def draw(self, target=None):
    """
    Redraw the DataTables in the current context, optionally updating ordering, searching and paging as required.

    Documentation
    https://datatables.net/reference/api/draw()

    :return:
    """
    if target is not None:
      self._js.append("draw(%s)" % JsUtils.jsConvertData(target, None))
    else:
      self._js.append("draw()")
    return self


class DatatableAPI(JsPackage):
  lib_alias = {'js': "datatables", 'css': 'datatables'}
  lib_selector = 'datatable'

  def body(self):
    """
    Get the tbody node for the table in the API's context.

    Documentation
    https://datatables.net/reference/api/table().body()

    :return:
    """
    return

  def container(self):
    """
    Get the div container node for the table in the API's context.

    Documentation
    https://datatables.net/reference/api/table().container()

    :return:
    """

  def footer(self):
    """
    Get the tfoot node for the table in the API's context

    Documentation
    https://datatables.net/reference/api/table().footer()

    :return:
    """

  def header(self):
    """
    Get the thead node for the table in the API's context

    Documentation
    https://datatables.net/reference/api/table().header()

    :return:
    """

  def nodes(self):
    """
    Get the table node for the table in the API's context.

    Documentation
    https://datatables.net/reference/api/table().node()

    :return:
    """
    return self.fnc("nodes()")

  def jquery_node(self):
    """
    Get the cell nodes for the selected column.

    Documentation
    https://datatables.net/reference/api/column().nodes()

    :return:
    """
    return JsQuery.JQuery(selector="%s.nodes().to$()" % self.varId, setVar=False)

  def clear(self):
    """
    Clear the table of all data:

    Documentation
    https://datatables.net/reference/api/clear()

    :return:
    """
    return self.fnc("clear()")

  def data(self):
    """
    Retrieve the data for the whole table, in row index order.

    Documentation
    https://datatables.net/reference/api/data()

    :return:
    """
    return JsObjects.JsArray.JsArray.get("%s.data()" % self.varId)

  def destroy(self):
    """
    Restore the tables in the current context to its original state in the DOM by removing all of DataTables enhancements,
    alterations to the DOM structure of the table and event listeners.

    Documentation
    https://datatables.net/reference/api/destroy()

    :return:
    """
    return self.fnc_closure("destroy()")

  def draw(self, target=None):
    """
    Redraw the DataTables in the current context, optionally updating ordering, searching and paging as required.

    Documentation
    https://datatables.net/reference/api/draw()

    :return:
    """
    if target is not None:
      return self.fnc_closure("draw(%s)" % JsUtils.jsConvertData(target, None))

    return self.fnc_closure("draw()")

  def order(self, data=None):
    """

    Example


    DOcumentation
    https://datatables.net/reference/api/order()

    :return:
    """
    if data is not None:
      data = JsUtils.jsConvertData(data, None)
      return self.fnc("order(%s)" % data)

    return self.fnc("order()")

  def page(self, action):
    """

    Documentation
    https://datatables.net/reference/api/page()

    :return:
    """
    if not action in ("first", "next", "previous", "last"):
      raise Exception("Action not defined")

    return self

  def search(self, jsData):
    """

    Documentation
    https://datatables.net/reference/api/search()

    :param jsData:
    :return:
    """

    return self

  def settings(self):
    """

    Documentation
    https://datatables.net/reference/api/settings()

    :return:
    """
    return self.fnc("settings()")

  def state(self):
    """
    Get the last saved state of the table.

    Documentation
    https://datatables.net/reference/api/state()

    :return:
    """
    return JsObjects.JsObject.JsObject.get("%s.state()" % self.varId)

  def cell(self, cellSelector=None, rowColSelector=None):
    """
    Select cells found by both row and column selectors

    Documentation
    https://datatables.net/reference/api/cells()
    https://datatables.net/reference/api/cell()

    :return:
    """
    if cellSelector is not None:
      selector = "%s.cell(%s)" % self.toStr()
    elif rowColSelector is not None:
      selector = "%s.cell(%s, %s)" % (self.toStr(), rowColSelector[0], rowColSelector[1])
    else:
      selector = "%s.cell()" % self.toStr()
    return CellAPI(selector)

  def column(self, colSelector):
    """

    :param colSelector:
    :return:
    """
    if colSelector is not None:
      selector = "%s.column(%s)" % (self.toStr(), JsUtils.jsConvertData(colSelector, None))
    else:
      selector = "%s.column()" % self.toStr()
    return ColumnAPI(selector)

  def columns(self, colSelector):
    """

    :param colSelector:
    :return:
    """
    if colSelector is not None:
      selector = "%s.column(%s)" % (self.varId, JsUtils.jsConvertData(colSelector, None))
    else:
      selector = "%s.column()" % self.varId
    return ColumnAPI(selector)

  def select(self):
    """
    Initialise Select from outside of the constructor

    Documentation
    https://datatables.net/reference/api/select()

    TODO add the select true
    :return:
    """
    return SelectAPI(selector="%s.select()", setVar=False)
