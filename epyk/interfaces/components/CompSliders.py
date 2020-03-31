# Check if pandas is available in the current environment
# if it is the case this module can handle DataFrame directly
try:
  import pandas as pd
  has_pandas = True

except:
  has_pandas = False


from epyk.core import html


class Sliders(object):
  """
  Description:
  ------------
  This module is relying on some Jquery IU components

  The slider and progress bar components can be fully described on the corresponding website
    - https://jqueryui.com/progressbar/
    - https://jqueryui.com/slider/

  As this module will return those object, all the properties and changes defined in the documentation can be done.
  """
  def __init__(self, context):
    self.context = context

  def slider(self, number=0, min=0, max=100, width=(100, '%'), height=(20, 'px'), htmlCode=None, attrs=None,
             helper=None, options=None, profile=None):
    """
    Description:
    ------------
    Add a Jquery UI slider object to the page

    Usage:
    ------
    rptObj.ui.slider(40)

    Related Pages:
    --------------
    https://jqueryui.com/slider/

    Attributes:
    ----------
    :param value:
    :param type:
    :param range:
    :param animate:
    :param step:
    :param min:
    :param max:
    :param width:
    :param height:
    :param htmlCode:
    :param globalFilter:
    :param recordSet:
    :param column:
    :param color:
    :param helper:
    :param profile:
    """
    html_slider = html.HtmlEvent.Slider(self.context.rptObj, number, min, max, width, height,  attrs or {}, helper,
                                         options or {}, htmlCode, profile)
    self.context.register(html_slider)
    return html_slider

  def date(self, value, min=None, max=None, width=(100, '%'), height=(20, 'px'), htmlCode=None, attrs=None,
             helper=None, options=None, profile=None):
    """

    :param value:
    :param min:
    :param max:
    :param width:
    :param height:
    :param htmlCode:
    :param attrs:
    :param helper:
    :param options:
    :param profile:
    """
    options = options or {}
    html_slider = html.HtmlEvent.SliderDate(self.context.rptObj, value, min, max, width, height, attrs or {}, helper,
                                            options or {}, htmlCode, profile)
    self.context.register(html_slider)
    return html_slider

  def date_range(self, value1, value2, min=None, max=None, width=(100, '%'), height=(20, 'px'), htmlCode=None, attrs=None,
                 helper=None, options=None, profile=None):
    """

    :param value1:
    :param value2:
    :param min:
    :param max:
    :param width:
    :param height:
    :param htmlCode:
    :param attrs:
    :param helper:
    :param options:
    :param profile:
    """
    options = options or {}
    options['range'] = True
    html_slider = html.HtmlEvent.SliderDates(self.context.rptObj, [value1, value2], min, max, width, height, attrs or {}, helper,
                                             options or {}, htmlCode, profile)
    self.context.register(html_slider)
    return html_slider

  def range(self, values, min=0, max=100, width=(100, '%'), height=(20, 'px'), htmlCode=None, attrs=None,
             helper=None, options=None, profile=None):
    """

    :param values:
    :param min:
    :param max:
    :param width:
    :param height:
    :param htmlCode:
    :param attrs:
    :param helper:
    :param options:
    :param profile:
    """
    options = options or {}
    options['range'] = True
    html_slider = html.HtmlEvent.Range(self.context.rptObj, values, min, max, width, height, attrs or {}, helper,
                                         options or {}, htmlCode, profile)
    self.context.register(html_slider)
    return html_slider


  def progressbar(self, number=0, total=100, width=(100, '%'), height=(20, 'px'), htmlCode=None, attrs=None,
                  helper=None, options=None, profile=None):
    """
    Description:
    ------------
    Add a progress bar component to the page

    Usage:
    ------
    rptObj.ui.sliders.progressbar(300)

    Related Pages:
    --------------
    https://jqueryui.com/progressbar/

    Attributes:
    ----------
    :param number: A number (by default between 0 and 100)
    :param total: A number
    :param width: Optional. Integer for the component width
    :param height: Optional. Integer for the component height
    :param htmlCode:
    :param attrs:
    :param helper:
    :param profile:
    """
    html_pr = html.HtmlEvent.ProgressBar(self.context.rptObj, number, total, width, height,  attrs or {}, helper,
                                         options or {}, htmlCode, profile)
    self.context.register(html_pr)
    return html_pr
