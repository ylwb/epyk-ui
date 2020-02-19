"""
Module in charge of all the Text components
"""

from epyk.core import html
from epyk.core.html import Defaults


class Texts(object):

  def __init__(self, context):
    self.context = context

  def text(self, text="", color=None, align='left', width=('auto', ""), height=(None, "px"),
           htmlCode=None, tooltip=None, options=None, helper=None, profile=None):
    """
    Add the HTML text component to the page

    Example
    rptObj.ui.text("this is a test")

    Documentation
    https://www.w3schools.com/tags/tag_font.asp

    :param text: The string value to be displayed in the component
    :param color: Optional. The color of the text
    :param align: Optional. The position of the icon in the line (left, right, center)
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param htmlCode: Optional. An identifier for this component (on both Python and Javascript side)
    :param tooltip: Optional. A string with the value of the tooltip
    :param options: Optional. The component options
    :param helper:
    :param profile: Optional. A flag to set the component performance storage

    :return: The text HTML object
    """
    if not isinstance(width, tuple):
      width = (width, 'px')
    text_comp = html.HtmlText.Text(self.context.rptObj, text, color, align, width, height, htmlCode, tooltip,
                                   options or {}, helper, profile)
    self.context.register(text_comp)
    return text_comp

  def label(self, text=None, color=None, align='center', width=(100, "px"), height=('auto', ""), htmlCode=None,
            tooltip='', profile=None, options=None):
    """
    The <label> tag defines a label for a <button>, <input>, <meter>, <output>, <progress>, <select>, or <textarea> element...

    The for attribute of the <label> tag should be equal to the id attribute of the related element to bind them together.

    Example
    rptObj.ui.texts.label("Test")
    rptObj.ui.texts.label("this is a test", color="red")

    Documentation
    https://www.w3schools.com/tags/tag_label.asp

    :param text: Optional. The string value to be displayed in the component
    :param color: Optional. The color of the text
    :param align: Optional. The position of the icon in the line (left, right, center)
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param htmlCode: Optional. An identifier for this component (on both Python and Javascript side)
    :param tooltip: Optional. A string with the value of the tooltip
    :param profile: Optional. A flag to set the component performance storage
    """
    dflt_options = {"markdown": True}
    if options is not None:
      dflt_options.update(options)
    html_label = html.HtmlText.Label(self.context.rptObj, text, color, align, width, height, htmlCode, tooltip,
                                     profile, dflt_options)
    self.context.register(html_label)
    return html_label

  def span(self, text=None, color=None, align='center', width=None, height=None, htmlCode=None,
           tooltip=None, profile=None):
    """
    The <span> tag is used to group inline-elements in a document.

    The <span> tag provides no visual change by itself.

    The <span> tag provides a way to add a hook to a part of a text or a part of a document.

    Example
    rptObj.ui.texts.span("Test")

    Documentation
    https://www.w3schools.com/tags/tag_span.asp

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
      width = (Defaults.TEXTS_SPAN_WIDTH, 'px')
    if height is None:
      height = (Defaults.LINE_HEIGHT, 'px')
    html_label = html.HtmlText.Span(self.context.rptObj, text, color, align, width, height, htmlCode, tooltip, profile)
    self.context.register(html_label)
    return html_label

  def highlights(self, text=None, title="", icon=None, type="danger", color=None, width=(None, "%"),
                 height=(None, "px"), htmlCode=None, helper=None, profile=None):
    """

    Example
    rptObj.ui.texts.highlights("Test content", title="Test", icon="fab fa-angellist")

    Documentation
    https://getbootstrap.com/docs/4.3/components/alerts/

    :param text: Optional. The string value to be displayed in the component
    :param title:
    :param icon:
    :param type: Optional, The type of the warning. Can be (primary, secondary, success, danger, warning, info, light,
                 dark). Default danger
    :param color:
    :param width:
    :param height:
    :param htmlCode:
    :param helper:
    :param profile:
    """
    html_light = html.HtmlText.Highlights(self.context.rptObj, text, title, icon, type, color, width,
                                          height, htmlCode, helper, profile)
    self.context.register(html_light)
    return html_light

  def formula(self, text=None, width=(100, "%"), color=None, helper=None, profile=None):
    """
    Interface to the mathjs Formulas object

    Example
    rptObj.ui.texts.formula("$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$", helper="This is a formula")

    Documentation
    https://www.w3schools.com/tags/tag_font.asp

    :param text: Optional. The string value to be displayed in the component
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param color: Optional. The color of the text
    :param helper:
    :param profile: Optional. A flag to set the component performance storage
    """
    html_formula = html.HtmlTextComp.Formula(self.context.rptObj, text, width, color, helper, profile)
    self.context.register(html_formula)
    return html_formula

  def code(self, text="", color=None, width=(90, '%'), height=(None, 'px'), htmlCode=None, options=None, helper=None, profile=None):
    """
    Python Wrapper to the Bootstrap CODE Tag

    Example
    rptObj.ui.texts.code("This is a code")

    Documentation
    https://v4-alpha.getbootstrap.com/content/code/

    :param text:
    :param color:
    :param width:
    :param height:
    :param htmlCode:
    :param options:
    :param helper:
    :param profile:
    """
    if not isinstance(text, list):
      text = [text]
    dflt_options = {"edit": True}
    if options is not None:
      dflt_options.update(options)
    html_code = html.HtmlText.Code(self.context.rptObj, text, color, width, height, htmlCode, dflt_options,
                                   helper, profile)
    self.context.register(html_code)
    return html_code

  def paragraph(self, text="", color=None, background_color=None, border=False, width=(100, "%"),
                height=(None, 'px'), htmlCode=None, encoding="UTF-8", dataSrc=None, helper=None, profile=None):
    """
    Python Wrapper to the HTML P Tag

    Example
    rptObj.ui.texts.paragraph("This is a paragraph", helper="Paragraph helper")

    Documentation
    https://www.w3schools.com/html/html_styles.asp

    :param text:
    :param color:
    :param background_color:
    :param border:
    :param width:
    :param height:
    :param htmlCode:
    :param encoding:
    :param dataSrc:
    :param profile:
    """
    html_paragraph = html.HtmlText.Paragraph(self.context.rptObj, text, color, background_color, border,
                                                         width, height, htmlCode, encoding, dataSrc, helper, profile)
    self.context.register(html_paragraph)
    return html_paragraph

  def preformat(self, text=None, color=None, width=(90, '%'), height=(None, 'px'), htmlCode=None, dataSrc=None,
                options=None, helper=None, profile=None):
    """

    Example
    rptObj.ui.texts.preformat("This is a pre formatted text")

    Documentation
    https://www.w3schools.com/html/html_styles.asp

    :param text:
    :param color:
    :param width:
    :param height:
    :param htmlCode:
    :param dataSrc:
    :param options:
    :param helper:
    :param profile:
    """
    dflt_options = {"reset": True, 'markdown': True}
    if options is not None:
      dflt_options.update(options)
    html_pre = html.HtmlText.Pre(self.context.rptObj, text, color, width, height, htmlCode, dataSrc, dflt_options, helper, profile)
    self.context.register(html_pre)
    return html_pre

  def blockquote(self, text=None, author=None, color=None, width=(None, '%'), height=(None, 'px'),
                 htmlCode=None, helper=None, profile=None):
    """

    Example
    rptObj.ui.texts.blockquote("This is a code")

    Documentation
    https://v4-alpha.getbootstrap.com/content/typography/

    :param text:
    :param author:
    :param color:
    :param width:
    :param height:
    :param htmlCode:
    :param helper:
    :param profile:
    """
    html_blockquote = html.HtmlText.BlockQuote(self.context.rptObj, text, author, color, width, height, htmlCode, helper, profile)
    self.context.register(html_blockquote)
    return html_blockquote

  def up_down(self, rec=None, color=None, label=None, options=None, helper=None, profile=None):
    """
    Up and down Text component

    Example
    rptObj.ui.texts.up_down({'previous': 240885, 'value': 240985})

    Documentation
    https://fontawesome.com/

    :param rec:
    :param color:
    :param label:
    :param options:
    :param helper:
    :param profile:
    """
    dflt_options = {"decPlaces": 0, "thouSeparator": ',', "decSeparator": '.'}
    if options is not None:
      dflt_options.update(options)
    html_up_down = html.HtmlTextComp.UpDown(self.context.rptObj, rec, color, label, dflt_options, helper, profile)
    self.context.register(html_up_down)
    return html_up_down

  def number(self, number=0, title=None, label=None, icon=None, color=None, tooltip='', htmlCode=None,
             options=None, helper=None, width=(150, 'px'), profile=None):
    """

    Example
    rptObj.ui.texts.number(289839898, label="test", helper="Ok", icon="fas fa-align-center")

    Documentation

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
    dflt_options = {"decPlaces": 0, "thouSeparator": ',', "decSeparator": '.'}
    if options is not None:
      dflt_options.update(options)
    html_number = html.HtmlText.Numeric(self.context.rptObj, number, title, label, icon, color, tooltip, htmlCode,
                                        dflt_options, helper, width, profile)
    self.context.register(html_number)
    return html_number

  def title(self, text=None, level=None, name=None, contents=None, color=None, picture=None, icon=None,
            marginTop=5, htmlCode=None, width=("auto", ""), height=(None, "px"), align=None, options=None, profile=None):
    """

    Example
    rptObj.ui.title("Test")
    rptObj.ui.title("Test", level=2)

    Documentation
    https://www.w3schools.com/tags/tag_hn.asp

    :param text:
    :param level:
    :param name:
    :param contents:
    :param color:
    :param picture:
    :param icon:
    :param marginTop:
    :param htmlCode:
    :param width:
    :param height:
    :param align:
    :param options:
    :param profile:
    """
    dflt_options = {"reset": True, 'markdown': False}
    if options is not None:
      dflt_options.update(options)
    html_title = html.HtmlText.Title(self.context.rptObj, text, level, name, contents, color, picture, icon,
                                     marginTop, htmlCode, width, height, align, dflt_options, profile)
    self.context.register(html_title)
    return html_title

  def fieldset(self, legend="", width=(100, "%"), height=(None, "px"), helper=None, profile=None):
    """

    Example
    rptObj.ui.texts.fieldset("legend")

    Documentation
    https://www.w3schools.com/tags/tag_legend.asp
    https://www.w3schools.com/tags/tag_fieldset.asp

    :param legend:
    :param width:
    :param height:
    :param profile:
    """
    html_fieldset = html.HtmlText.Fieldset(self.context.rptObj, legend, width=width, height=height, helper=helper,
                                           profile=profile)
    self.context.register(html_fieldset)
    return html_fieldset
