
from epyk.core.js import JsUtils
from epyk.core.js.primitives import JsNumber
from epyk.core.js.primitives import JsArray
from epyk.core.js.primitives import JsObject
from epyk.core.js.packages import JsPackage

# All the predefined variable types
from epyk.core.js.fncs import JsFncs


class D3ScaleLinear(object):
  """

  """
  def __init__(self, range):
    self.range = range

  def range(self):
    pass


class D3Html(object):
  def __init__(self, src, selector, tag, setVar=False):
    self.src, self._selector, self.setVar, self.tag = src, selector, setVar, tag
    self._js = []

  def attr(self, key, val):
    """

    :param key:
    :param val:
    """
    key = JsUtils.jsConvertData(key, None)
    val = JsUtils.jsConvertData(val, None)
    self._js.append("attr(%s, %s)" % (key, val))
    return self

  def text(self, data):
    self._js.append("text(function(column) { return column; })")
    return self

  def html(self, data):
    self._js.append("html(function(d) { return d.value; })")
    return self

  def selectAll(self, d3Type):
    d3Type = JsUtils.jsConvertData(d3Type, None)
    self._js.append("selectAll(%s)" % d3Type)
    return D3Select(self.src, selector=self.toStr())

  def toStr(self):
    content = [self._selector] + self._js
    if self.setVar:
      self.setVar = False
      return "var %s = %s" % (self.tag, ".".join(content))

    return ".".join(content)


class D3Select(object):
  class __internal(object):
    # By default it will attach eveything to the body
    jqId, jsImports = 'd3.select("body")', set([])

  def __init__(self, src=None, id=None, d3Type=None, selector=None):
    self.src = src if src is not None else self.__internal()
    if id is None and d3Type is None and selector is None:
      raise Exception()

    if selector is not None:
      self._selector = selector
    elif id is not None:
      self._selector = self.select(id)
    else:
      self._selector = self.selectAll(d3Type)
    self.src.jsImports.add('d3')
    self._js = []

  def data(self, datasets=None):
    """
    Binds the specified array of data with the selected elements,
    returning a new selection that represents the update selection: the elements successfully bound to data.

    The data is specified for each group in the selection.
    If the selection has multiple groups (such as d3.selectAll followed by selection.selectAll), then data should typically be specified as a function.

    Documentation
    https://github.com/d3/d3-selection/blob/v1.4.0/README.md#selection_data

    :param datasets:
    """
    if datasets is None:
      self._js.append("data()")
    else:
      #datasets = JsUtils.jsConvertData(datasets, None)
      self._js.append("data(%s)" % datasets)
    return self

  def dataFncRows(self, columns):
    """

    :param columns:
    """
    self._js.append("data(function(row) {return %s.map(function(c, i) {return {column: c, value: row[i]}; }); })" % columns)
    return self

  def datum(self, datasets=None):
    """
    Gets or sets the bound data for each selected element.
    Unlike selection.data, this method does not compute a join and does not affect indexes or the enter and exit selections.

    Documentation
    https://github.com/d3/d3-selection/blob/v1.4.0/README.md#selection_datum

    :param datasets: If a value is not specified, returns the bound datum for the first (non-null) element in the selection.

    :return:
    """
    if datasets is None:
      self._js.append("datum()")
    else:
      datasets = JsUtils.jsConvertData(datasets, None)
      self._js.append("datum(%s)" % datasets)
    return self

  def filter(self, fnc):
    pass

  def enter(self):
    """
    Returns the enter selection: placeholder nodes for each datum that had no corresponding DOM element in the selection.
    (The enter selection is empty for selections not returned by selection.data.)

    Documentation
    https://github.com/d3/d3-selection/blob/v1.4.0/README.md#selection_enter

    :return:
    """
    self._js.append("enter()")
    return self

  def exit(self):
    """
    Returns the exit selection: existing DOM elements in the selection for which no new datum was found.
    (The exit selection is empty for selections not returned by selection.data.)

    Documentation
    https://github.com/d3/d3-selection/blob/v1.4.0/README.md#selection_exit

    :return:
    """
    self._js.append("exit()")
    return self

  def append(self, htmlType, setVar=True):
    """
    If the specified type is a string, appends a new element of this type (tag name) as the last child of each selected element, or before the next following sibling in the update selection if this is an enter selection.

    Documentation
    https://github.com/d3/d3-selection/blob/v1.4.0/README.md#selecting-elements

    :param htmlType:
    """
    cnv_htmlType = JsUtils.jsConvertData(htmlType, None)
    return D3Html(self.src, "%s.append(%s)" % (self.toStr(), cnv_htmlType), htmlType, setVar=setVar)

  def rappend(self, htmlType):
    return self.append(htmlType, setVar=False)

  def insert(self, htmlType, id):
    pass

  def style(self, key, val):
    pass

  def attr(self, key, val):
    """

    :param key:
    :param val:
    """
    key = JsUtils.jsConvertData(key, None)
    val = JsUtils.jsConvertData(val, None)
    self._js.append("attr(%s, %s)" % (key, val))
    return self

  def call(self, fnc_name):
    """

    :param fnc_name:

    :return:
    """
    fnc_name = JsUtils.jsConvertData(fnc_name, None)
    self._js.append("call(%s)" % fnc_name)
    return self

  def on(self, eventType, fnc):
    pass

  def remove(self):
    """
    Removes the selected elements from the document. Returns this selection (the removed elements) which are now detached from the DOM.
    There is not currently a dedicated API to add removed elements back to the document; however, you can pass a function to selection.append or selection.insert to re-add elements.

    Documentation
    https://github.com/d3/d3-selection/blob/v1.4.0/README.md#selecting-elements

    :return:
    """
    self._js.append("remove()")
    return self

  def clone(self, deep=False):
    """
    Inserts clones of the selected elements immediately following the selected elements and returns a selection of the newly added clones.

    Documentation
    https://github.com/d3/d3-selection/blob/v1.4.0/README.md#selecting-elements

    :param deep: If deep is truthy, the descendant nodes of the selected elements will be cloned as well

    :return:
    """
    deep = JsUtils.jsConvertData(deep, None)
    self._js.append("clone(%s)" % deep)
    return self

  def order(self):
    """
    Re-inserts elements into the document such that the document order of each group matches the selection order.
    This is equivalent to calling selection.sort if the data is already sorted, but much faster.

    Documentation
    https://github.com/d3/d3-selection/blob/v1.4.0/README.md#selection_append

    :return:
    """
    self._js.append("order()")
    return self

  def select(self, id):
    return 'd3.select("%s")' % id

  def selectAll(self, d3Type):
    d3Type = JsUtils.jsConvertData(d3Type, None)
    self._js.append("selectAll(%s)" % d3Type)
    return self

  def var(self, varName):
    """

    :param variable_name:
    :return:
    """
    return D3Select(self.src, selector=varName)

  def toStr(self):
    """
    Javascript representation

    :return: Return the Javascript String
    """
    if self._selector is None:
      raise Exception("Selector not defined, use this() or new() first")

    if len(self._js) == 0:
      return self._selector

    strData = "%(jqId)s.%(items)s" % {'jqId': self._selector, 'items': ".".join(self._js)}
    self._js = [] # empty the stack
    return strData


class D3ForceSimulation(object):
  _package = ['d3-force']

  def __init__(self, id=None, d3Type=None):
    """

    Documentation:
      - https://github.com/d3/d3-force

    :param id:
    :param d3Type:
    """
    pass

  def force(self, forceType, fnc):
    pass

  def restart(self):
    pass

  def stop(self):
    pass

  def tick(self, tick):
    pass

  def nodes(self, nodes):
    pass

  def alpha(self, number):
    pass

  def alphaDecay(self, number):
    pass

  def alphaTarget(self, target):
    pass

  def alphaTarget(self, number):
    pass

  def velocityDecay(self, decay):
    pass

  def find(self):
    pass

  def on(self):
    pass


class D3ForceManyBody(object):
  def strength(self):
    pass

  def distanceMax(self, x):
    pass

  def distanceMin(self, x):
    pass


class D3ForceCollide(object):
  def __init__(self, radius=None):
    """
    Creates a new circle collision force with the specified radius. If radius is not specified, it defaults to the constant one for all nodes.

    Documentation:
        - https://github.com/d3/d3-force#forceCollide

    :param radius:
    :return:
    """
    pass

  def radius(self, fnc):
    """
    If radius is specified, sets the radius accessor to the specified number or function, re-evaluates the radius accessor for each node, and returns this force. If radius is not specified, returns the current radius accessor

    Documentation:
      - https://github.com/d3/d3-force#forceCollide

    :param fnc:
    :return:
    """
    pass

  def strength(self, strength):
    """
    If strength is specified, sets the force strength to the specified number in the range [0,1] and returns this force. If strength is not specified, returns the current strength which defaults to 0.

    Documentation:
      - https://github.com/d3/d3-force#forceCollide

    :param strength:
    :return:
    """
    pass

  def iterations(self, iterations):
    """
    If iterations is specified, sets the number of iterations per application to the specified number and returns this force

    Documentation:
      - https://github.com/d3/d3-force#forceCollide

    :param iterations:
    :return:
    """
    pass


class D3ForceCenter(object):
  def __init__(self):
    pass

  def x(self):
    pass

  def y(self):
    pass


class D3Event(object):
  def __init__(self):
    """

    Documentation:
      - https://github.com/d3/d3-selection/blob/v1.4.0/README.md#event

    """
    pass

  def on(self):
    pass

  @property
  def active(self):
    pass

  @property
  def x(self):
    pass

  @property
  def y(self):
    pass

  def timeStamp(self):
    pass


class D3Pack(object):
  def __init__(self):
    """

    Documentation:
      - https://github.com/d3/d3-hierarchy/blob/v1.1.8/README.md#pack

    """

  def radius(self, number):
    pass

  def size(self, number):
    """
    If size is specified, sets this pack layout’s size to the specified two-element array of numbers [width, height] and returns this pack layout. If size is not specified, returns the current size, which defaults to [1, 1]

    Documentation:
      - https://github.com/d3/d3-hierarchy/blob/v1.1.8/README.md#pack

    :param number:
    :return:
    """
    pass

  def padding(self, number):
    """
    If padding is specified, sets this pack layout’s padding accessor to the specified number or function and returns this pack layout. If padding is not specified, returns the current padding accessor, which defaults to the constant zero

    Documentation:
      - https://github.com/d3/d3-hierarchy/blob/v1.1.8/README.md#pack

    :param number:
    :return:
    """
    pass

  def packSiblings(self, circles):
    """
    Packs the specified array of circles, each of which must have a circle.r property specifying the circle’s radius

    Documentation:
      - https://github.com/d3/d3-hierarchy/blob/v1.1.8/README.md#pack

    :param circles:
    :return:
    """
    pass

  def packEnclose(self, circles):
    """
    Computes the smallest circle that encloses the specified array of circles, each of which must have a circle.r property specifying the circle’s radius, and circle.x and circle.y properties specifying the circle’s center

    Documentation:
      - https://github.com/d3/d3-hierarchy/blob/v1.1.8/README.md#pack

    :param circles:
    :return:
    """
    pass


class D3Band(object):
  """
  https://github.com/d3/d3-scale/blob/master/README.md#band-scales
  """

  def __init__(self, selector):
    """

    """
    self._selector = selector
    self._js = []

  def domain(self, domain=None):
    """

    :param domain:
    :return:
    """
    if domain is None:
      self._js.append("domain()")
    return self

  def range(self, range=None):
    """

    :param range:
    :return:
    """

  def rangeRound(self, range):
    """

    :param range:
    :return:
    """

  def round(self):
    """

    :return:
    """

  def toStr(self):
    """
    Javascript representation

    :return: Return the Javascript String
    """
    if self._selector is None:
      raise Exception("Selector not defined, use this() or new() first")

    if len(self._js) == 0:
      return self._selector

    strData = "%(jqId)s.%(items)s" % {'jqId': self._selector, 'items': ".".join(self._js)}
    self._js = [] # empty the stack
    return strData


class D3File(object):

  def __init__(self, src, filename, selector):
    self._f, self.src, self._selector = filename, src, selector
    self._js_frg, self._js_ids = [], set()

  def records(self, jsId):
    """

    :param jsId:
    """
    self._js_frg.append("%s.push(row)" % jsId)
    return self

  def unpack(self, jsId, column=None):
    """

    :param jsId:
    :param column:
    """
    if not jsId in self._js_ids:
      column = JsUtils.jsConvertData(column, None)
      self._js_frg.append("%s.push(row[%s])" % (jsId, column))
      self._js_ids.add(jsId)
    return JsObject.JsObject(jsId, isPyData=False)

  def filter(self, rules):
    """

    csv.filter("row['direction'] != 'Decreasing'")

    :param rules:
    """
    if not isinstance(rules, list):
      rules = [rules]
    self._js_frg.append("if(%s){ return; }" % "&&".join(rules))
    return self

  def filterCol(self, column, value, type="=="):
    """

    :param value:
    :return:
    """
    column = JsUtils.jsConvertData(column, None)
    value = JsUtils.jsConvertData(value, None)
    self._js_frg.append("if(row[%s] %s %s){ return; }" % (column, type, value))
    return self

  def callback(self, jsFnc):
    """

    :param jsFnc:
    """
    self._js_frg.append(jsFnc)
    return self

  def toStr(self):
    file = JsUtils.jsConvertData(self._f, None)
    return "%s; %s(%s, function(row, err){%s})" % (";".join(["var %s = []" % i for i in self._js_ids]), self._selector, file, ";".join(self._js_frg))


class D3Svg(object):
  def __init__(self, src, selector, varName=None):
    self.src, self._selector, self.varName = src, selector, varName
    self._js = []

  def line(self):
    self._js.append("line()")
    return self

  def x(self):
    self._js.append("x(function(d) { return x(d.date1); })")
    return self

  def y(self):
    self._js.append("y(function(d) { return x(d.date1); })")
    return self

  def toStr(self):
    content = [self._selector] + self._js
    if self.varName is not None:
      return "var %s = %s" % (self.varName, ".".join(content))

    return ".".join(content)


class JsD3(JsPackage):

  lib_alias = {"js": 'd3'}
  lib_selector = 'd3'

  @property
  def svg(self):
    return D3Svg(self.src, selector="%s.svg" % self._selector)

  def csv(self, url):
    """

    """
    #url = JsUtils.jsConvertData(url, None)
    #return JsFncs.JsFunction("d3.csv(%s)" % (url, JsUtils.jsConvertFncs(callback, toStr=True)))
    return D3File(self.src, url, selector="%s.csv" % self._selector)

  def tsv(self, url):
    """

    """
    #url = JsUtils.jsConvertData(url, None)
    #return JsFncs.JsFunction("d3.csv(%s)" % (url, JsUtils.jsConvertFncs(callback, toStr=True)))
    return D3File(self.src, url, selector="%s.tsv" % self._selector)

  def json(self, url):
    """

    """
    #url = JsUtils.jsConvertData(url, None)
    #return JsFncs.JsFunction("d3.csv(%s)" % (url, JsUtils.jsConvertFncs(callback, toStr=True)))
    return D3File(self.src, url, selector="%s.json" % self._selector)

  def dsv(self, url, delimiter):
    """

    """
    #url = JsUtils.jsConvertData(url, None)
    #return JsFncs.JsFunction("d3.csv(%s)" % (url, JsUtils.jsConvertFncs(callback, toStr=True)))
    return D3File(self.src, url, selector="%s.tsv" % self._selector)

  def min(self, dataset, jsFnc):
    return JsNumber.JsNumber("d3.min(%s, %s)" % (dataset, jsFnc))

  def max(self, dataset, jsFnc):
    return JsNumber.JsNumber("d3.max(%s, %s)" % (dataset, jsFnc))

  def select(self, id):
    return D3Select(self.src, id)

  def selectAll(self, d3Type):
    return D3Select(d3Type=d3Type)

  def scaleLinear(self, range):
    return D3ScaleLinear(range)

  def scaleBand(self, range=None):
    """
    Constructs a new band scale with the specified domain and range, no padding, no rounding and center alignment.
    If domain is not specified, it defaults to the empty domain. If range is not specified, it defaults to the unit range [0, 1].

    :param range:

    :rtype: D3Band
    :return:
    """
    if range is None:
      self._js.append("scaleBand()")
    return D3Band(self.toStr())

  def forceSimulation(self, nodes=None):
    return D3ForceSimulation(nodes)

  def forceManyBody(self):
    return D3ForceManyBody()

  def scaleOrdinal(self, colors):
    pass

  def forceX(self):
    pass

  def forceY(self):
    pass

  def drag(self):
    pass

  def toStr(self):
    """
    Javascript representation

    :return: Return the Javascript String
    """
    if self._selector is None:
      raise Exception("Selector not defined, use this() or new() first")

    if len(self._js) == 0:
      return self._selector

    strData = "%(jqId)s.%(items)s" % {'jqId': self._selector, 'items': ".".join(self._js)}
    self._js = [] # empty the stack
    return strData


if __name__ == '__main__':
  columns = ["A", "B"]
  data = [["1", 12], ["2", 30], ["2", 33]]
  rptObj = None

  rptObj.body.dom.d3.append('table').attr("style", "margin-left: 250px"),
  rptObj.body.dom.d3.var('table').append("thead"),
  rptObj.body.dom.d3.var('thead').rappend("tr").selectAll("th").data(columns).enter().rappend("th").text("test"),
  rptObj.body.dom.d3.var('table').append("tbody"),
  rptObj.body.dom.d3.var('tbody').selectAll("tr").data(data).enter().append("tr"),
  rptObj.body.dom.d3.var('tr').selectAll("td").dataFncRows(columns).enter().rappend("td").html("")
