"""
Module dedicated to produce Images components
"""

from epyk.core import html


class Images(object):
  def __init__(self, context):
    self.context = context

  def img(self, text=None, path=None, width=(100, "%"), height=(None, "px"), align="center", htmlCode=None,
          profile=None, options=None):
    """

    Example


    Documentation
    https://www.w3schools.com/bootstrap/bootstrap_ref_css_images.asp
    https://www.w3schools.com/cssref/css3_pr_border-radius.asp

    :param text:
    :param path:
    :param width:
    :param height:
    :param align:
    :param htmlCode:
    :param profile:
    :param options:
    """
    html_image = html.HtmlImage.Image(self.context.rptObj, text, path, align, htmlCode, width, height, profile, options or {})
    self.context.register(html_image)
    return html_image

  def animated(self, image=None, text="", title="", url=None, path=None, width=(200, "px"), height=(200, "px"),
               profile=None):
    """

    Example
    rptObj.ui.images.animated("philo.PNG")

    Documentation
    https://tympanus.net/Tutorials/OriginalHoverEffects/

    :param image:
    :param text:
    :param title:
    :param url:
    :param path:
    :param width:
    :param height:
    :param profile:
    """
    html_id = html.HtmlImage.AnimatedImage(self.context.rptObj, image, text, title, url, path, width, height, profile)
    self.context.register(html_id)
    return html_id

  def carrousel(self, images, path=None, width=(100, "%"), height=('auto', ""), profile=None):
    """

    Example
    Defaults.SERVER_PATH = r"XXXXX"
    rptObj.ui.images.carrousel(["Capture.PNG", "philo.PNG"])

    Documentation
    https://www.cssscript.com/basic-pure-css-slideshow-carousel/

    :param images:
    :param path:
    :param width:
    :param height:
    :param profile:
    """
    html_i = html.HtmlImage.ImgCarrousel(self.context.rptObj, images, path, width, height, profile)
    self.context.register(html_i)
    return html_i

  def emoji(self, symbole=None, size=(None, 'px'), top=(20, 'px'), profile=None):
    """

    Example
    rptObj.ui.images.emoji(rptObj.symbols.smileys.DISAPPOINTED_FACE)

    Documentation
    https://github.com/wedgies/jquery-emoji-picker

    :param symbole:
    :param size:
    :param top:
    :param profile:
    """
    size = self.context._size(size)
    html_emoji = html.HtmlImage.Emoji(self.context.rptObj, symbole, size, top, profile)
    self.context.register(html_emoji)
    return html_emoji

  def icon(self, text=None, size=(None, "px"), width=(None, 'px'), height=(None, "px"), tooltip=None, profile=None):
    """

    Example
    rptObj.ui.images.icon("fab fa-angellist")
    
    Documentation
    https://fontawesome.com/icons?m=free

    :param text:
    :param size: Optional, A tuple with a integer for the size and its unit
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param tooltip:
    :param profile:
    """
    size = self.context._size(size)
    html_icon = html.HtmlImage.Icon(self.context.rptObj, text, size=size, width=width, height=height, tooltip=tooltip,
                                    profile=profile)
    self.context.register(html_icon)
    return html_icon

  def badge(self, text=None, label=None, size=(None, 'px'), icon=None, background_color=None, color=None, url=None,
            tooltip=None, profile=None):
    """
    Display a badge component using Bootstrap

    Example
    rptObj.ui.images.badge("Test badge", "Label", icon="fas fa-align-center")
    rptObj.ui.images.badge("This is a badge", background_color="red", color="white")

    Documentation
    https://getbootstrap.com/docs/4.0/components/badge/

    :param text: The content of the badge
    :param label: Optional, The label to display close to the badge
    :param size: Optional, A tuple with a integer for the size and its unit
    :param icon: Optional, A String with the icon to display from font-awesome
    :param background_color: Optional, The background color of the badge
    :param color: Optional, The text color of the badge
    :param url:
    :param tooltip: Optional, The text to display in the tooltip
    :param profile: Optional, A boolean to store the performances for each components
    """
    tmp_size = self.context._size(size)
    if size[0] is None:
      size = (tmp_size[0] - 2, tmp_size[1])
    html_badge = html.HtmlImage.Badge(self.context.rptObj, text, label, icon, size, background_color, color, url, tooltip, profile)
    self.context.register(html_badge)
    return html_badge
