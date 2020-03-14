"""
DC.js API

http://dc-js.github.io/dc.js/docs/html/
"""

from epyk.core.js import JsUtils
from epyk.core.js.packages import JsPackage


class DC(JsPackage):
  lib_alias = {'css': 'dc', 'js': 'dc'}

  def __init__(self, src=None, varName=None, setVar=True, parent=None):
    self.src = src if src is not None else self.__internal()
    self._selector = "new dc.%s('#%s')" % (self.chartFnc, parent.htmlId)
    self.varName, self.setVar = varName, setVar
    self.src.jsImports.add(self.lib_alias['js'])
    self.src.cssImport.add(self.lib_alias['css'])
    self._js, self._xaxis, self._yaxis, self._u = [[]], None, None, {}

  def x(self):
    return self.fnc("x(d3.scaleLinear().domain([0,20]))")

  def width(self, n):
    """

    :param n:

    :return: Return 'self' to allow the cnains on the Python side
    """
    return self.fnc("width(%s)" % JsUtils.jsConvertData(n, None))

  def height(self, n):
    """

    :param n:
    :return:
    """
    return self.fnc("height(%s)" % JsUtils.jsConvertData(n, None))

  def yAxisLabel(self, text):
    """

    :param text:

    :return:
    """
    return self.fnc("yAxisLabel(%s)" % JsUtils.jsConvertData(text, None))

  def xAxisLabel(self, text):
    """

    :param text:
    :return:
    """
    return self.fnc("xAxisLabel(%s)" % JsUtils.jsConvertData(text, None))

  def render(self):
    """

    :return:
    """
    self._js.append(["render()"])
    return self

  def dimension(self, values):
    return self.fnc("dimension(%s)" % values)
    #return self.fnc("dimension(%s)" % JsUtils.jsConvertData(values, None))

  def group(self, groups):
    return self.fnc("group(%s)" % groups)
    #return self.fnc("group(%s)" % JsUtils.jsConvertData(groups, None))

  def toStr(self):
    """
    Description:
    ------------
    Javascript representation

    :return: Return the Javascript String
    """
    if self._selector is None:
      raise Exception("Selector not defined, use this() or new() first")

    obj_content = []
    for i, js in enumerate(self._js):
      if len(js) == 0:
        continue

      str_fnc = ".".join([d.toStr() if hasattr(d, "toStr") else d for d in js])
      if self.setVar:
        if str_fnc:
          str_fnc = "var %s = %s; %s.%s" % (self.varId, self._selector, self.varId, str_fnc)
        else:
          str_fnc = "var %s = %s" % (self.varId, self._selector)
        self.setVar = False
      else:
        if str_fnc:
          if i in self._u:
            # to avoid raising an error when the variable is not defined
            str_fnc = "if(%s !== undefined){%s.%s}" % (self.varId, self.varId, str_fnc)
          else:
            varId = self._mapVarId(str_fnc, self.varId)
            str_fnc = "%s.%s" % (varId, str_fnc)
        else:
          str_fnc = self.varId
      obj_content.append(str_fnc)
    self._js = [[]] # empty the stack
    return "; ".join(obj_content)


class Line(DC):
  chartFnc = "lineChart"

  def curve(self):
    pass

  def renderArea(self, flag):
    """

    :param flag:
    """
    return self.fnc("renderArea(%s)" % JsUtils.jsConvertData(flag, None))

  def renderDataPoints(self, flag):
    """

    :param flag:
    :return:
    """
    return self.fnc("renderDataPoints(%s)" % JsUtils.jsConvertData(flag, None))

  def clipPadding(self, value):
    """

    :param value:
    :return:
    """
    return self.fnc("clipPadding(%s)" % JsUtils.jsConvertData(value, None))


class Bar(DC):
  chartFnc = "barChart"


class Row(DC):
  chartFnc = "RowChart"

  def x(self):
    pass

  def elasticY(self, flag):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/row-targets.html

    :param flag:
    """
    return self.fnc("elasticY(%s)" % JsUtils.jsConvertData(flag, None))


class Pie(DC):
  chartFnc = "pieChart"

  def slicesCap(self, value):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/pie.html

    :param value:
    """
    return self.fnc("slicesCap(%s)" % JsUtils.jsConvertData(value, None))

  def innerRadius(self, value):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/pie.html

    :param value:
    """
    return self.fnc("innerRadius(%s)" % JsUtils.jsConvertData(value, None))

  def legend(self):
    pass

  def drawPaths(self, flag):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/pie-external-labels.html

    :param flag:
    """
    return self.fnc("drawPaths(%s)" % JsUtils.jsConvertData(flag, None))

  def externalLabels(self, size):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/pie-external-labels.html

    :param size:
    """
    return self.fnc("externalLabels(%s)" % JsUtils.jsConvertData(size, None))

  def externalRadiusPadding(self, size):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/pie-external-labels.html

    :param size:
    """
    return self.fnc("externalRadiusPadding(%s)" % JsUtils.jsConvertData(size, None))


class Series(DC):
  chartFnc = "seriesChart"

  def chart(self):
    pass

  def x(self):
    pass

  def elasticY(self, flag):
    """

    :param flag:
    """
    return self.fnc("elasticY(%s)" % JsUtils.jsConvertData(flag, None))

  def mouseZoomable(self, flag):
    """

    :param flag:
    """
    return self.fnc("mouseZoomable(%s)" % JsUtils.jsConvertData(flag, None))

  def shareTitle(self, flag):
    """

    :param flag:
    """
    return self.fnc("shareTitle(%s)" % JsUtils.jsConvertData(flag, None))


class Scatter(DC):
  chartFnc = "ScatterPlot"

  def x(self):
    pass

  def elasticX(self, flag):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/splom.html

    :param flag:
    """
    return self.fnc("elasticX(%s)" % JsUtils.jsConvertData(flag, None))

  def excludedOpacity(self, value):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/scatter-brushing.html

    :param value:
    """
    return self.fnc("excludedOpacity(%s)" % JsUtils.jsConvertData(value, None))

  def excludedColor(self, color):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/scatter-brushing.html

    :param color:
    """
    return self.fnc("excludedColor(%s)" % JsUtils.jsConvertData(color, None))


class Sunburst(DC):
  chartFnc = "SunburstChart"

  def innerRadius(self, value):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/sunburst-equal-radii.html

    :param value:
    """
    return self.fnc("innerRadius(%s)" % JsUtils.jsConvertData(value, None))

  def ringSizes(self, jsFnc):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/sunburst-equal-radii.html

    :param jsFnc:
    """
    return self.fnc("ringSizes(%s)" % jsFnc)

  def equalRingSizes(self):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/sunburst-equal-radii.html

    :return:
    """
    return self.fnc("ringSizes(%s.equalRingSizes())" % self.varId)


class Composite(DC):
  chartFnc = "compositeChart"

  def x(self):
    pass

  def xUnits(self):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/pareto-chart.html
    """
    pass

  def elasticY(self, flag):
    """

    :param flag:
    """
    return self.fnc("elasticY(%s)" % JsUtils.jsConvertData(flag, None))

  def renderHorizontalGridLines(self, flag):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/composite-bar-line.html

    :param flag:
    """
    return self.fnc("renderHorizontalGridLines(%s)" % JsUtils.jsConvertData(flag, None))

  def compose(self, dc_charts):
    pass


class BoxPlot(DC):
  chartFnc = "boxPlot"

  def elasticY(self, flag):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/boxplot-basic.html

    :param flag:
    """
    return self.fnc("elasticY(%s)" % JsUtils.jsConvertData(flag, None))

  def elasticX(self, flag):
    """

    https://github.com/dc-js/dc.js/blob/master/web-src/examples/boxplot-basic.html

    :param flag:
    """
    return self.fnc("elasticX(%s)" % JsUtils.jsConvertData(flag, None))
