"""

"""

from epyk.core.css.catalogs import Catalog

from epyk.core.css.styles import CssStylesDrop
from epyk.core.css.styles import CssStylesDiv
from epyk.core.css.styles import CssStylesDivEvents


class CatalogDropAreas(Catalog.CatalogGroup):
  def basic(self):
    """  """
    return self._set_class(CssStylesDrop.CssDropFile)

  def bubble(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivBubble)

  def bubble_comment(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivCommBubble)

  def left(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivLeft)

  def right(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivRight)

  def pointer(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivCursor)

  def banner(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivBanner)

  def sub_banner(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivSubBanner)

  def sub_label(self):
    """ """
    return self._set_class(CssStylesDiv.CssDivLabelPoint)

  def no_border(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivNoBorder)

  def border(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivWithBorder)

  def border_shadow(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivShadow)

  def border_dot(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivBoxWithDotBorder)

  def border_bottom(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivBottomBorder)

  def console(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivConsole)

  def margin(self):
    """  """
    return self._set_class(CssStylesDiv.CsssDivBoxMargin)

  def content_center(self):
    """  """
    return self._set_class(CssStylesDiv.CssDivBoxCenter)

  def color_hover(self):
    """ Change the color when the mouse is on the component """
    return self._set_class(CssStylesDivEvents.CssDivOnHover)

  def background_hover(self):
    """ Change the background color when the mouse is on the component """
    return self._set_class(CssStylesDivEvents.CssDivOnHoverBackgroundLight)

  def width_hover(self):
    """ Change the background color when the mouse is on the component """
    return self._set_class(CssStylesDivEvents.CssDivOnHoverWidth)
