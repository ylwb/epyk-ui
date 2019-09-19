"""

"""

from epyk.core.html import Html


class Sparklines(Html.Html):
  __reqJs = ['jquery-sparklines']
  name, category, callFnc = 'sparkline', 'Charts', 'sparkline'
  __pyStyle = ["CssSparklines"]

  def __init__(self, report, data, chart_type, options):
    super(Sparklines, self).__init__(report, data)
    self._jsStyles = {"type": chart_type}
    if options is not None:
      self._jsStyles.update(options)

  def options(self, attrs):
    """
    Add any option to the sparkline object

    Example
    chartObj.options({"lineColor": 'yellow'})

    Documentation
    https://omnipotent.net/jquery.sparkline/#s-docs

    :param attrs: A python dictionary

    :return: The sparkline object
    """
    self._jsStyles.update(attrs)
    return self

  def onDocumentLoadFnc(self):
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, 'htmlObj.sparkline(data, jsStyles)')

  def __str__(self):
    return "<span %s></span>" % self.strAttr(pyClassNames=["CssSparklines"])