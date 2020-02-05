"""
CSS Style module for the Search components
"""


from epyk.core.css.styles import CssStyle


class CssSearchExt(CssStyle.Style):
  _attrs = {'box-sizing': 'border-box', 'border-radius': '4px', 'font-size': '12px',
            'background-repeat': 'no-repeat', 'padding': '5px 20px 5px 40px',
            '-webkit-transition': 'width 0.4s ease-in-out', 'transition': 'width 0.4s ease-in-out'}
  _focus = {'width': '100%', 'outline': 0}

  def customize(self):
    self.css({"background-color": self.rptObj.theme.greys[0]})
    self.hover.css({'color': self.rptObj.theme.greys[-1]})


class CssSearch(CssStyle.Style):
  """

  """
  _attrs = {'width': '100%', 'display': 'inline-block', 'border': 'none', 'font-size': '12px',
            'background-repeat': 'no-repeat', 'padding': '5px 20px 5px 40px'}
  _focus = {'outline': 0}

  def customize(self):
    self.css({"background-color": self.rptObj.theme.greys[0],
              "border-bottom": '1px solid %s' % self.rptObj.theme.greys[3], 'color': self.rptObj.theme.greys[-1]})
    self.hover.css({'color': self.rptObj.theme.greys[-1], 'border-bottom-color': self.rptObj.theme.success[1]})


class CssSearchButton(CssStyle.Style):
  _attrs = {'margin-top': '10px', 'margin-left': '10px', 'display': 'block', 'cursor': 'pointer', 'position': 'absolute'}
  _selectors = {'child': 'i'}

  def customize(self):
    self.css({"color": self.rptObj.theme.greys[5]})
