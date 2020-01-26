"""
CSS Style module for the Text components
"""


from epyk.core.css.styles import CssStyle

from epyk.core.css import Defaults as Defaults_css


class CssTextBold(CssStyle.CssCls):
  attrs = {'font-weight': 'bold'}


class CssText(CssStyle.CssCls):
  attrs = {'padding': 0, 'margin': 0}


class CssFormula(CssStyle.CssCls):
  """
  CSS Style for the formulas component
  """
  attrs = {'padding': 0, 'margin': 0}
  focus = {'outline': 0, 'border': 'none', 'box-shadow': 'none'}
  cssId = {'reference': ".math"}


class CssTitle1(CssStyle.CssCls):
  attrs = {'padding': '0 0 5px 0', 'font-size': '24px', 'font-weight': 'bold', 'text-transform': 'uppercase',
           'white-space': 'pre-wrap', 'border-bottom': '1px dashed black', 'border-width': '2px', 'margin-bottom': '5px'}

  def customize(self, style, eventsStyles):
    style.update({"color": self.rptObj.theme.greys[7], "border-color": self.rptObj.theme.greys[9]})


class CssTitle2(CssStyle.CssCls):
  attrs = {'padding': 0, 'font-size': '22px', 'margin-top': '5px', 'font-weight': 'bold', 'text-transform': 'uppercase',
           'white-space': 'pre-wrap'}

  def customize(self, style, eventsStyles):
    style.update({"color": self.rptObj.theme.colors[7]})


class CssTitle3(CssStyle.CssCls):
  attrs = {'padding': 0, 'font-size': '16px', 'margin-top': '5px', 'font-weight': 'bold', 'text-transform': 'uppercase',
           'white-space': 'pre-wrap'}

  def customize(self, style, eventsStyles):
    style.update({"color": self.rptObj.theme.colors[7]})


class CssTitle4(CssStyle.CssCls):
  attrs = {'padding': 0, 'font-size': '14px', 'margin': '5px 0 0 0', 'font-weight': 'bold', 'width': '100%',
           'white-space': 'pre-wrap'}

  def customize(self, style, eventsStyles):
    style.update({"color": self.rptObj.theme.greys[5]})


class CssTitle(CssStyle.CssCls):
  attrs = {'padding': 0, 'font-size': '14px', 'font-family': 'arial', 'margin-bottom': 0, 'white-space': 'pre-wrap',
           'font-weight': 'bold'}


class CssNumberCenter(CssStyle.CssCls):
  reqCssCls = [CssTitle]
  attrs = {'width': '100%', 'text-align': 'center'}


class CssMarkRed(CssStyle.CssCls):
  attrs = {'background': 'none', 'font-size': '12px'}

  def customize(self, style, eventsStyles):
    style.update({"color": self.rptObj.theme.danger[1]})


class CssMarkBlue(CssStyle.CssCls):
  attrs = {'background': 'none', 'font-weight': 'bold', 'font-size': '12px'}

  def customize(self, style, eventsStyles):
    style.update({"color": self.rptObj.theme.colors[7]})


class CssTextWithBorder(CssStyle.CssCls):
  attrs = {'border': '1px solid', 'padding': '5px', 'margin': '10px'}
  cssId = {'child': 'fieldset'}

  def customize(self, style, eventsStyles):
    style.update({"background-color": self.rptObj.theme.greys[0]})


class CssCheckMark(CssStyle.CssCls):
  attrs = {'text-align': 'center', 'display': 'inline-block',
           'font-family': 'FontAwesome', 'height': '18px', 'width': '18px'}

  def customize(self, style, eventsStyles):
    style.update({"background-color": self.rptObj.theme.greys[0], "color": self.rptObj.theme.greys[9]})
    eventsStyles['hover'].update({'color': 'white', 'background-color': self.rptObj.theme.colors[9]})


class CssTextItem(CssStyle.CssCls):
  attrs = {'cursor': 'pointer', 'width': '200px', 'padding': '5px 5px 5px 20px'}

  def customize(self, style, eventsStyles):
    eventsStyles['hover'].update({"color": self.rptObj.theme.greys[-1], "background": self.rptObj.theme.colors[2]})


class CssTextNotSelectable(CssStyle.CssCls):
  attrs = {'-moz-user-select': '-moz-none', "user-select": 'none', '-khtml-user-select': 'none',
           '-webkit-user-select': 'none', '-ms-user-select': 'none'}
