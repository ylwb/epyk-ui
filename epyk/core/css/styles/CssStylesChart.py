"""
CSS Style module for the Chart components
"""


from epyk.core.css.styles import CssStyle


class CssDivChart(CssStyle.Style):
  """
  CSS class for the Chart container
  """
  _attrs = {'margin': '0 0 5px 0', 'outline': 'none'}

  def customize(self):
    self.css({'border': "1px solid %s" % self.rptObj.theme.greys[3]})
    self.hover.css({'border': "1px solid %s" % self.rptObj.theme.colors[1]})


# --------------------------------------------------------------------------------------------------------------
#
#                                   BILLBOARD SECTION
# --------------------------------------------------------------------------------------------------------------
class CssBillboardTitle(CssStyle.Style):
  classname = "bb-title"

  def customize(self):
    self.css({'fill': self.rptObj.theme.greys[-1]}, important=True)


class CssBillboardLegend(CssStyle.Style):
  classname = "bb text"

  def customize(self):
    self.css({'fill': self.rptObj.theme.greys[-1]}, important=True)


class CssBillboardAxis(CssStyle.Style):
  _selectors = {'child': ".bb-axis line, .bb-axis-x line, .bb-axis .domain, .bb-axis-x .domain"}

  def customize(self):
    self.css({'stroke': self.rptObj.theme.greys[-1]})


class CssBillboardXAxis(CssStyle.Style):
  classname = "bb-axis-x text"

  def customize(self):
    self.css({'fill': self.rptObj.theme.greys[-1]}, important=True)


class CssBillboardYAxis(CssStyle.Style):
  classname = "bb-axis-y text"

  def customize(self):
    self.css({'fill': self.rptObj.theme.greys[-1]}, important=True)


# --------------------------------------------------------------------------------------------------------------
#
#                                   C3 SECTION
# --------------------------------------------------------------------------------------------------------------
class CssC3Title(CssStyle.Style):
  classname = "c3-title"

  def customize(self):
    self.css({'fill': self.rptObj.theme.greys[-1]}, important=True)


class CssC3Legend(CssStyle.Style):
  classname = "c3 text"

  def customize(self):
    self.css({'fill': self.rptObj.theme.greys[-1]}, important=True)


class CssC3Axis(CssStyle.Style):
  _selectors = {'child': '.c3-axis line, .c3-axis .domain'}

  def customize(self):
    self.css({'stroke': self.rptObj.theme.greys[-1]})


class CssC3XAxis(CssStyle.Style):
  classname = "c3-axis-x"
  _selectors = {'child': "text"}

  def customize(self):
    self.css({'fill': self.rptObj.theme.greys[-1]}, important=True)


class CssC3YAxis(CssStyle.Style):
  classname = "c3-axis-y"
  _selectors = {'child': "text"}

  def customize(self):
    self.css({'fill': self.rptObj.theme.greys[-1]}, important=True)


# --------------------------------------------------------------------------------------------------------------
#
#                                   NVD3 SECTION
# --------------------------------------------------------------------------------------------------------------
class CssNVD3Axis(CssStyle.Style):
  _selectors = {'child': '.nvd3 .nv-axis g path.domain'}

  def customize(self):
    self.css({'stroke': self.rptObj.theme.greys[-1], 'stroke-opacity': 1})


class CssNVD3AxisLabel(CssStyle.Style):
  classnames = ['nvd3', 'nv-axis']

  def customize(self):
    self.css({'fill': self.rptObj.theme.greys[-1]})


class CssNVD3AxisLegend(CssStyle.Style):
  _selectors = {'child': 'svg text'}

  def customize(self):
    self.css({'fill': self.rptObj.theme.greys[-1]})


class CssNVD3HideGrid(CssStyle.Style):
  classnames = ['nvd3', 'tick']
  _selectors = {'child': 'line'}

  def customize(self):
    self.css({'display': 'none'})


# Bootstrap issue
# https://stackoverflow.com/questions/18894820/jquery-sparklines-and-twitter-bootstrap-3-tooltip-style-overrides
class CssSparklines(CssStyle.Style):
  classname = "jqstooltip"
  attrs = {"ebkit-box-sizing": "content-box", "-moz-box-sizing": "content-box", "box-sizing": "content-box"}
