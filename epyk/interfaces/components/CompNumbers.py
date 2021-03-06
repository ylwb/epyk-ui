#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core import html
from epyk.core.html import graph

from epyk.core.html import Defaults as defaults_html
from epyk.core.css import Defaults as defaults_css
from epyk.interfaces import Arguments


class Numbers(object):

  def __init__(self, context):
    self.context = context

  def digits(self, text=None, color=None, align='center', width=None, height=None, htmlCode=None,
           tooltip=None, options=None, profile=None):
    """
    Description:
    ------------
    The <span> tag is used to group inline-elements in a document.

    The <span> tag provides no visual change by itself.

    The <span> tag provides a way to add a hook to a part of a text or a part of a document.

    Usage::

      rptObj.ui.texts.span("Test")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlText.Position`

    Related Pages:

      https://www.w3schools.com/tags/tag_span.asp

    Templates:

      https://github.com/epykure/epyk-templates/blob/master/locals/components/numbers.py

    Attributes:
    ----------
    :param text: Optional. The string value to be displayed in the component
    :param color: Optional. The color of the text
    :param align: Optional. The position of the icon in the line (left, right, center)
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param htmlCode: Optional. An identifier for this component (on both Python and Javascript side)
    :param tooltip: Optional. A string with the value of the tooltip
    :param profile: Optional. A flag to set the component performance storage
    """
    if width is None:
      width = (defaults_html.TEXTS_SPAN_WIDTH, 'px')
    if height is None:
      height = (defaults_html.LINE_HEIGHT, 'px')
    html_label = html.HtmlText.Position(self.context.rptObj, text, color, align, width, height, htmlCode, tooltip, options, profile)
    html_label.position(3, {"font-size": defaults_css.font(5), "font-weight": "bold"})
    html_label.position(4, {"font-size": defaults_css.font(5), "font-weight": "bold"})
    html_label.digits(True)
    return html_label

  def number(self, number=0, title=None, label=None, icon=None, color=None, tooltip='', htmlCode=None,
             options=None, helper=None, width=(150, 'px'), profile=None):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.texts.number(289839898, label="test", helper="Ok", icon="fas fa-align-center")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlText.Numeric`

    Attributes:
    ----------
    :param number: Optional. The value to be displayed to the component. Default now
    :param title:
    :param label: Optional. The text of label to be added to the component
    :param icon: Optional. A string with the value of the icon to display from font-awesome
    :param color:
    :param tooltip:
    :param htmlCode:
    :param options:
    :param helper:
    :param profile:
    """
    dflt_options = {"digits": 0, "thousand_sep": ',', "decimal_sep": '.'}
    if options is not None:
      dflt_options.update(options)
    html_number = html.HtmlText.Numeric(self.context.rptObj, number, title, label, icon, color, tooltip, htmlCode,
                                        dflt_options, helper, width, profile)
    return html_number

  def percent(self, number=0, title=None, label=None, icon=None, color=None, tooltip='', htmlCode=None,
             options=None, helper=None, width=(150, 'px'), profile=None):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.texts.percent(289839898, label="test", helper="Ok", icon="fas fa-align-center")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlText.Numeric`

    Attributes:
    ----------
    :param number: Optional. The value to be displayed to the component. Default now
    :param title:
    :param label: Optional. The text of label to be added to the component
    :param icon: Optional. A string with the value of the icon to display from font-awesome
    :param color:
    :param tooltip:
    :param htmlCode:
    :param options:
    :param helper:
    :param profile:
    """
    html_number = self.number(number, title, label, icon, color, tooltip, htmlCode, options, helper, width, profile)
    html_number.money("%", format="%v%s")
    return html_number

  def pound(self, number=0, title=None, label=None, icon=None, color=None, tooltip='', htmlCode=None,
             options=None, helper=None, width=(150, 'px'), profile=None):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.texts.pound(289839898, label="test", helper="Ok", icon="fas fa-align-center")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlText.Numeric`

    Attributes:
    ----------
    :param number: Optional. The value to be displayed to the component. Default now
    :param title:
    :param label: Optional. The text of label to be added to the component
    :param icon: Optional. A string with the value of the icon to display from font-awesome
    :param color:
    :param tooltip:
    :param htmlCode:
    :param options:
    :param helper:
    :param profile:
    """
    html_number = self.number(number, title, label, icon, color, tooltip, htmlCode, options, helper, width, profile)
    html_number.money("£")
    return html_number

  def euro(self, number=0, title=None, label=None, icon=None, color=None, tooltip='', htmlCode=None,
             options=None, helper=None, width=(150, 'px'), profile=None):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.texts.euro(289839898, label="test", helper="Ok", icon="fas fa-align-center")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlText.Numeric`

    Attributes:
    ----------
    :param number: Optional. The value to be displayed to the component. Default now
    :param title:
    :param label: Optional. The text of label to be added to the component
    :param icon: Optional. A string with the value of the icon to display from font-awesome
    :param color:
    :param tooltip:
    :param htmlCode:
    :param options:
    :param helper:
    :param profile:
    """
    html_number = self.number(number, title, label, icon, color, tooltip, htmlCode, options, helper, width, profile)
    html_number.money("€", format="%v %s")
    return html_number

  def dollar(self, number=0, title=None, label=None, icon=None, color=None, tooltip='', htmlCode=None,
             options=None, helper=None, width=(150, 'px'), profile=None):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.texts.dollar(289839898, label="test", helper="Ok", icon="fas fa-align-center")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlText.Numeric`

    Attributes:
    ----------
    :param number: Optional. The value to be displayed to the component. Default now
    :param title:
    :param label: Optional. The text of label to be added to the component
    :param icon: Optional. A string with the value of the icon to display from font-awesome
    :param color:
    :param tooltip:
    :param htmlCode:
    :param options:
    :param helper:
    :param profile:
    """
    html_number = self.number(number, title, label, icon, color, tooltip, htmlCode, options, helper, width, profile)
    html_number.money("$", format="%v %s")
    return html_number

  def money(self, symbol, number=0, title=None, label=None, icon=None, color=None, tooltip='', htmlCode=None,
             options=None, helper=None, width=(150, 'px'), profile=None):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.texts.money(289839898, label="test", helper="Ok", icon="fas fa-align-center")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlText.Numeric`

    Attributes:
    ----------
    :param number: Optional. The value to be displayed to the component. Default now
    :param title:
    :param label: Optional. The text of label to be added to the component
    :param icon: Optional. A string with the value of the icon to display from font-awesome
    :param color:
    :param tooltip:
    :param htmlCode:
    :param options:
    :param helper:
    :param profile:
    """
    html_number = self.number(number, title, label, icon, color, tooltip, htmlCode, options, helper, width, profile)
    html_number.money(symbol, format="%v %s")
    return html_number

  def plotly(self, value, profile=None, options=None, width=(100, "%"), height=(330, "px"),
             htmlCode=None):
    """
    Description:
    ------------

    Underlying HTML Objects:

      - :class:`epyk.core.graph.GraphPlotly.Indicator`

    Attributes:
    ----------
    :param value:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    ind = graph.GraphPlotly.Indicator(self.context.rptObj, width, height, options or {}, htmlCode, profile)
    ind.add_trace({'value': value}, mode="number")
    return ind

  def plotly_with_delta(self, value, profile=None, options=None, width=(100, "%"),
                        height=(330, "px"), htmlCode=None):
    """
    Description:
    ------------

    Underlying HTML Objects:

      - :class:`epyk.core.graph.GraphPlotly.Indicator`

    Attributes:
    ----------
    :param value:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    ind = graph.GraphPlotly.Indicator(self.context.rptObj, width, height, options or {}, htmlCode, profile)
    ind.add_trace({'value': value}, mode="number+delta")
    return ind

  def move(self, current, previous, color=None, label=None, options=None, helper=None, profile=None):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.rich.delta({'number': 100, 'prevNumber': 60, 'thresold1': 100, 'thresold2': 50}, helper="test")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlTextComp.Delta`

    Attributes:
    ----------
    :param current:
    :param previous:
    :param color:
    :param label:
    :param options:
    :param helper:
    :param profile:
    """
    dflt_options = {"digits": 0, 'thousand_sep': ",", 'decimal_sep': ".",
                    'red': self.context.rptObj.theme.danger[1], 'green': self.context.rptObj.theme.success[1],
                    'orange': self.context.rptObj.theme.warning[1]}
    if options is not None:
      dflt_options.update(options)
    html_up_down = html.HtmlTextComp.UpDown(self.context.rptObj, {"value": current, 'previous': previous}, color, label, dflt_options, helper, profile)
    return html_up_down
