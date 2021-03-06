
from epyk.core.css import Defaults_css
from epyk.core.css.styles.attributes import Attrs


class NavBar(Attrs):
  def __init__(self, htmlObj):
    super(NavBar, self).__init__(htmlObj)
    self.font_size = Defaults_css.font(8)
    self.display = 'block'
    self.margin = 0
    self.vertical_align = 'top'
    self.left = 0
    self.box_sizing = "border-box"
    self.padding = "0 5px 0 2px"
    self.position = "fixed"
    self.background_color = htmlObj._report.theme.greys[0]
    self.border_bottom = "1px solid %s" % htmlObj._report.theme.greys[4]
    self.top = 0
    self.z_index = 310


class Footer(Attrs):
  def __init__(self, htmlObj):
    super(Footer, self).__init__(htmlObj)
    self.display = 'block'
    self.margin = 0
    self.vertical_align = 'bottom'
    self.left = 0
    self.padding = "0 2px 0 2px"
    self.position = "fixed"
    self.bottom = 0
    self.z_index = 10
