"""
Module in charge of the Basic CSS events
"""

from epyk.core.css.styles.classes import CssStyle


class CssDivOnHover(CssStyle.Style):
  """
  Change the color when the mouse is on the component
  """
  _hover = {"cursor": 'pointer'}

  def customize(self):
    self.hover.css({"color": self.rptObj.theme.colors[1]}, important=True)


class CssDivOnHoverBackgroundLight(CssStyle.Style):
  """
  Change the background color when the mouse is on the component
  """
  _attrs = {"background-color": "inherit"}
  _hover = {"cursor": 'pointer'}

  def customize(self):
    self.hover.css({"background-color": self.rptObj.theme.greys[2], "font-weight": 'bold'})
    self.hover.css('color', self.rptObj.theme.greys[-1], important=True)


class CssDivOnHoverWidth(CssStyle.Style):
  """
  Change the background color when the mouse is on the component
  """
  _attrs = {"align": 'right', "background-color": "inherit"}
  _hover = {"cursor": 'pointer', 'width': '150px'}

  def customize(self):
    self.hover.css({"background-color": self.rptObj.theme.greys[2], "font-weight": 'bold'})
    self.hover.css('color', self.rptObj.theme.greys[-1], important=True)