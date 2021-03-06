#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core.html import tables as html_tables
from epyk.interfaces import Arguments


class Pivottable(object):

  def __init__(self, context):
    self.parent = context

  def pivot(self, recordSet=None, rows=None, cols=None, width=(100, '%'), height=(None, 'px'), htmlCode=None,
            helper=None, options=None, profile=False):
    """
    Description:
    -----------
    Create a HTML Pivot table

    Usage::

      Related Pages:

      https://pivottable.js.org/examples/
    https://react-pivottable.js.org/
    https://jsfiddle.net/nicolaskruchten/w86bgq9o/
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    table = html_tables.HtmlTablePivot.PivotTable(self.parent.context.rptObj, recordSet, rows, cols, width, height, htmlCode,
                                                  helper, options, profile)
    return table

  def ui(self, recordSet=None, rows=None, cols=None, width=(100, '%'), height=(None, 'px'), htmlCode=None,
            helper=None, options=None, profile=False):
    """
    Description:
    -----------
    Create a HTML Pivot table

    Usage::

      Related Pages:

      https://pivottable.js.org/examples/
    https://react-pivottable.js.org/
    https://jsfiddle.net/nicolaskruchten/w86bgq9o/
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    table = html_tables.HtmlTablePivot.PivotUITable(self.parent.context.rptObj, recordSet, rows, cols, width, height, htmlCode,
                                                  helper, options, profile)
    return table

  def sub_total(self, recordSet=None, rows=None, cols=None, width=(100, '%'), height=(None, 'px'), htmlCode=None,
                helper=None, options=None, profile=False):
    """
    Description:
    -----------
    Create a HTML Pivot table

    Usage::

      Related Pages:

      https://pivottable.js.org/examples/
    https://react-pivottable.js.org/
    https://jsfiddle.net/nicolaskruchten/w86bgq9o/
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    table = html_tables.HtmlTablePivot.PivotUITable(self.parent.context.rptObj, recordSet, rows, cols, width, height, htmlCode,
                                                  helper, options, profile)
    table.sub_total()
    return table

  def heatmap(self, recordSet=None, rows=None, cols=None, values=None, width=(100, '%'), height=(None, 'px'),
              htmlCode=None, helper=None, options=None, profile=False):
    """
    Description:
    -----------
    Create a HTML Pivot table

    Usage::

    Related Pages:

      https://pivottable.js.org/examples/
    https://react-pivottable.js.org/
    https://jsfiddle.net/nicolaskruchten/w86bgq9o/
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    table = html_tables.HtmlTablePivot.PivotTable(self.parent.context.rptObj, recordSet, rows, cols, width, height, htmlCode,
                                                  helper, options, profile)
    table.renderers.heatmap()
    if values is not None:
      table.aggregators.sumOverSum(values)
    return table

  def c3(self, recordSet=None, rows=None, cols=None, width=(100, '%'), height=(None, 'px'), htmlCode=None,
            helper=None, options=None, profile=False):
    """
    Description:
    -----------
    Create a HTML Pivot table

    Usage::

      Related Pages:

      https://pivottable.js.org/examples/
    https://react-pivottable.js.org/
    https://jsfiddle.net/nicolaskruchten/w86bgq9o/
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    table = html_tables.HtmlTablePivot.PivotUITable(self.parent.context.rptObj, recordSet, rows, cols, width, height, htmlCode,
                                                  helper, options, profile)
    table.renderers.c3.bar()
    return table

  def d3(self, recordSet=None, rows=None, cols=None, width=(100, '%'), height=(None, 'px'), htmlCode=None,
            helper=None, options=None, profile=False):
    """
    Description:
    -----------
    Create a HTML Pivot table

    Usage::

      Related Pages:

      https://pivottable.js.org/examples/
    https://react-pivottable.js.org/
    https://jsfiddle.net/nicolaskruchten/w86bgq9o/
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    table = html_tables.HtmlTablePivot.PivotUITable(self.parent.context.rptObj, recordSet, rows, cols, width, height, htmlCode,
                                                  helper, options, profile)
    table.renderers.treemap()
    return table

  def plotly(self, recordSet=None, rows=None, cols=None, width=(100, '%'), height=(None, 'px'), htmlCode=None,
            helper=None, options=None, profile=False):
    """
    Description:
    -----------
    Create a HTML Pivot table

    Usage::

      Related Pages:

      https://pivottable.js.org/examples/
    https://react-pivottable.js.org/
    https://jsfiddle.net/nicolaskruchten/w86bgq9o/
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    table = html_tables.HtmlTablePivot.PivotUITable(self.parent.context.rptObj, recordSet, rows, cols, width, height, htmlCode,
                                                    helper, options, profile)
    table.renderers.plotly.bar()
    return table
