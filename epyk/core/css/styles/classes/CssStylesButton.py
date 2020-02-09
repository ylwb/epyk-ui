"""
CSS Style module for the Button components
"""

from epyk.core.css.styles.classes import CssStyle


class CssBorderRadius(CssStyle.Style):
  _attrs = {'border-radius': '5px'}


class CssButtonBasic(CssStyle.Style):
  # Static properties for this class
  _attrs = {'font-weight': 'bold', 'padding': '1px 10px', 'margin': '2px 0 2px 0', 'text-decoration': 'none',
            'border-radius': '5px', 'white-space': 'nowrap', 'display': 'inline-block',
            '-webkit-appearance': 'none', '-moz-appearance': 'none'}
  _hover = {'text-decoration': 'none', 'cursor': 'pointer'}
  _focus = {'outline': 0}
  _disabled = {'cursor': 'none'}

  def customize(self):
    self.css({'border': '1px solid %s' % self.rptObj.theme.colors[-1], 'color': self.rptObj.theme.greys[-1],
              'background-color': self.rptObj.theme.greys[0]})
    self.hover.css({'background-color': self.rptObj.theme.colors[-1], 'color': self.rptObj.theme.colors[0]})
    self.disabled.css({'background-color': self.rptObj.theme.colors[-1], 'color': self.rptObj.theme.colors[6],
                       'font-style': 'italic'})


class CssButtonReset(CssStyle.Style):
  # Static properties for this class
  _attrs = {'font-weight': 'bold', 'padding': '5px 10px 5px 10px', 'margin-top': '5px', 'text-decoration': 'none',
            'border-radius': '5px', 'display': 'inline-block', 'text-transform': 'uppercase'}
  _hover = {'text-decoration': 'none', 'cursor': 'pointer'}

  def customize(self):
    self.css({'border': '1px solid %s' % self.rptObj.theme.danger[1], 'color': self.rptObj.theme.danger[1],
              'background-color': self.rptObj.theme.greys[0]})
    self.hover.css({'background-color': self.rptObj.theme.danger[1], 'color': self.rptObj.theme.greys[0]})


class CssButtonSuccess(CssStyle.Style):
  # Static properties for this class
  _attrs = {'font-weight': 'bold', 'padding': '10px 10px 10px 10px', 'margin': '10px 0px 10px 5px',
            'text-decoration': 'none', 'border-radius': '5px', 'display': 'inline-block', 'text-transform': 'uppercase'}
  _hover = {'text-decoration': 'none', 'cursor': 'pointer'}

  def customize(self):
    self.css({'color': self.rptObj.theme.colors[9], 'background-color': self.rptObj.theme.greys[0],
              'border': '1px solid %s' % self.rptObj.theme.colors[9]})
    self.hover.css({'color': self.rptObj.theme.greys[0], 'background-color': self.rptObj.theme.colors[9]})