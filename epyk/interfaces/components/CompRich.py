"""
Interface to the rich HTML components
"""

from epyk.core import html


class Rich(object):
  def __init__(self, context):
    self.context = context

  def textbubble(self, recordSet=None, width=(100, "%"), height=(80, 'px'), color=None, size=(25, "px"),
                 background_color=None, helper=None, profile=None):
    """

    Example
    rptObj.ui.rich.textbubble({"value": 23, "title": "Title"}, helper="This is a helper")

    Documentation

    :param recordSet:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param color: Optional. The font color in the component. Default inherit
    :param size: Optional, A tuple with a integer for the size and its unit
    :param background_color:
    :param helper: Optional. A tooltip helper
    :param profile: Optional. A flag to set the component performance storage
    """
    html_bubble = html.HtmlTextComp.TextBubble(self.context.rptObj, recordSet or {}, width, height, color, size,
                                               background_color, helper, profile)
    self.context.register(html_bubble)
    return html_bubble

  def delta(self, rec=None, width=(200, 'px'), height=(80, 'px'), size=None, options=None, helper=None, profile=None):
    """

    Example
    rptObj.ui.rich.delta({'number': 100, 'prevNumber': 60, 'thresold1': 100, 'thresold2': 50}, helper="test")

    Documentation
    https://jqueryui.com/progressbar/
    https://fontawesome.com/icons?d=gallery

    :param rec:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param size: Optional, A tuple with a integer for the size and its unit
    :param helper: Optional. A tooltip helper
    :param profile: Optional. A flag to set the component performance storage

    :rtype: html.HtmlTextComp.Delta
    :return:
    """
    dflt_options = {"decPlaces": 0, "thouSeparator": ',', "decSeparator": '.'}
    if options is not None:
      dflt_options.update(options)
    return self.context.register(html.HtmlTextComp.Delta(self.context.rptObj, rec or {}, width, height, size,
                                                         dflt_options, helper, profile))

  def vignet(self, rec=None, width=(100, '%'), height=(None, 'px'), size=(None, 'px'), color_title=None, options=None,
             helper=None, profile=None):
    """

    Example
    rptObj.ui.rich.vignet({'title': 'Python', 'number': 100, 'text': 'Content', 'color': 'green', 'url':
                           'https://www.python.org/', 'icon': 'fab fa-python', 'tooltip': 'Python Fondation',
                           'urlTitle': 'WebSite'})

    Documentation

    :param rec:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param size: Optional, A tuple with a integer for the size and its unit
    :param color_title:
    :param helper: Optional. A tooltip helper
    :param profile: Optional. A flag to set the component performance storage
    """
    dflt_options = {"decPlaces": 0, "thouSeparator": ',', "decSeparator": '.', 'markdown': True}
    if options is not None:
      dflt_options.update(options)
    size = self.context._size(size)
    vignet = html.HtmlTextComp.Vignet(self.context.rptObj, rec, width, height, size, color_title, dflt_options, helper,
                                      profile)
    self.context.register(vignet)
    return vignet

  def stars(self, val=None, label=None, color=None, align='left', best=5, htmlCode=None, helper=None, profile=None):
    """
    Entry point for the Stars component

    Example
    rptObj.ui.rich.stars(3, label="test", helper="This is a helper")

    stars = rptObj.ui.rich.stars(3, label="test", helper="This is a helper")
    stars.click()

    Documentation
    https://www.w3schools.com/howto/howto_css_star_rating.asp

    :param val:
    :param label: Optional. The text of label to be added to the component
    :param color: Optional. The font color in the component. Default inherit
    :param align:
    :param best: Optional. The max number of stars. Default 5
    :param htmlCode: Optional. An identifier for this component (on both Python and Javascript side)
    :param profile: Optional. A flag to set the component performance storage
    """
    html_star = html.HtmlOthers.Stars(self.context.rptObj, val, label, color, align, best, htmlCode, helper, profile)
    self.context.register(html_star)
    return html_star

  def textborder(self, recordSet=None, width=(None, '%'), height=(None, "px"), size=(None, 'px'), align='center',
                 helper=None, profile=None):
    """

    Example
    rptObj.ui.rich.textborder({"title": "New Python Framework", 'value': "A new Python Web Framework", 'color': 'green',
                             'icon': 'fab fa-python', 'colorTitle': 'darkgreen'})

    Documentation

    :param recordSet:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param size: Optional, A tuple with a integer for the size and its unit
    :param align:
    :param helper: Optional. A tooltip helper
    :param profile: Optional. A flag to set the component performance storage
    """
    size = self.context._size(size)

    return self.context.register(html.HtmlTextComp.TextWithBorder(self.context.rptObj, recordSet, width,
                                                                  height, size, align, helper, profile))

  def blocktext(self, recordSet=None, color=None, size=(None, 'px'), border='auto', width=(300, 'px'), height=(None, 'px'),
                helper=None, profile=None):
    """

    Example
    rptObj.ui.rich.blocktext({"text": 'This is a brand new python framework', "title": 'New Python Web Framework',
                            "button": {"text": 'Get Started', 'url': "/getStarted"}, 'color': 'green'})

    Documentation

    :param recordSet:
    :param color: Optional. The font color in the component. Default inherit
    :param size: Optional. The font size in the component. Default 12px
    :param border:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param helper: Optional. A tooltip helper
    :param profile: Optional. A flag to set the component performance storage
    """
    size = self.context._size(size)
    html_blocktext = html.HtmlTextComp.BlockText(self.context.rptObj, recordSet, color, size, border, width, height, helper, profile)
    self.context.register(html_blocktext)
    return html_blocktext

  def light(self, color=None, height=(20, 'px'), label=None, tooltip=None, helper=None, profile=None):
    """

    Example
    rptObj.ui.rich.light("red", label="label", tooltip="Tooltip", helper="Helper")

    :param color:
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param label: Optional. The text of label to be added to the component
    :param tooltip: Optional. A string with the value of the tooltip
    :param helper: Optional. The filtering properties for this component
    :param profile: Optional. A flag to set the component performance storage
    """
    html_traffic = html.HtmlTextComp.TrafficLight(self.context.rptObj, color, label, height, tooltip, helper, profile)
    self.context.register(html_traffic)
    return html_traffic

  def prism(self, text=None, language='python', size=(None, 'px'), width=(100, "%"), height=(None, "px"),
            isEditable=False, trimSpaces=True, align=None, helper=None, profile=None):
    """

    Example
    rptObj.ui.rich.prism("print('test')")

    Documentation
    https://www.w3schools.com/tags/tag_font.asp

    :param text:
    :param language: Optional, The language format used. Default Python
    :param size: Optional, A tuple with a integer for the size and its unit
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param isEditable:
    :param trimSpaces:
    :param align:
    :param profile: Optional. A flag to set the component performance storage
    """
    size = self.context._size(size)
    html_prism = html.HtmlTextComp.Prism(self.context.rptObj, text, language, size, width,
                                                         height, isEditable, trimSpaces, align, helper, profile)
    self.context.register(html_prism)
    return html_prism

  def info(self, text=None, options=None, profile=None):
    """
    Display a info icon with a tooltip

    Example
    rptObj.ui.info("Test")

    Documentation
    https://fontawesome.com/icons/question-circle?style=solid
    https://api.jqueryui.com/tooltip/

    :param text: The content of the tooltip
    :param profile: Optional, A boolean to store the performances for each components
    """
    html_help = html.HtmlOthers.Help(self.context.rptObj, text, width=(10, "px"), profile=profile, options=options or {})
    self.context.register(html_help)
    return html_help
