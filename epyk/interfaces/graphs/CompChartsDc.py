"""

"""

from epyk.core.html.graph import GraphDC
from epyk.core.js.objects import JsChartDC


class DC(object):
  def __init__(self, context):
    self.parent = context
    self.chartFamily = "DC"

  def line(self, data=None, seriesNames=None, xAxis=None, otherDims=None, title=None, filters=None, profile=None,
           xAxisOrder=None, options=None, width=(100, "%"), height=(330, "px"), htmlCode=None):
    """

    Documentation
    https://square.github.io/crossfilter/
    https://dc-js.github.io/dc.js/

    :param data:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param title:
    :param profile:
    :param xAxisOrder:
    :param width:
    :param height:
    :param htmlCode:

    :return:

    :rtype: GraphDC.Chart
    """
    chart_obj = JsChartDC.JsLine(self.parent.context.rptObj, data, {'static': {}, 'dynamic': {}})
    return self.parent.context.register(GraphDC.Chart(self.parent.context.rptObj, chart_obj, width, height, title,
                                                      options or {}, htmlCode, filters, profile))

  def pie(self, data=None, seriesNames=None, xAxis=None, otherDims=None, title=None, filters=None, profile=None,
           xAxisOrder=None, options=None, width=(100, "%"), height=(330, "px"), htmlCode=None):
    """

    Documentation
    https://square.github.io/crossfilter/
    https://dc-js.github.io/dc.js/

    :param data:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param title:
    :param profile:
    :param xAxisOrder:
    :param width:
    :param height:
    :param htmlCode:

    :return:

    :rtype: GraphDC.Chart
    """
    chart_obj = JsChartDC.JsPie(self.parent.context.rptObj, data, {'static': {}, 'dynamic': {}})
    return self.parent.context.register(GraphDC.Chart(self.parent.context.rptObj, chart_obj, width, height, title,
                                                      options or {}, htmlCode, filters, profile))

  def bubble(self, data=None, seriesNames=None, xAxis=None, otherDims=None, title=None, filters=None, profile=None,
        xAxisOrder=None, options=None, width=(100, "%"), height=(330, "px"), htmlCode=None):
    """

    Documentation
    https://square.github.io/crossfilter/
    https://dc-js.github.io/dc.js/

    :param data:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param title:
    :param profile:
    :param xAxisOrder:
    :param width:
    :param height:
    :param htmlCode:

    :return:

    :rtype: GraphDC.Chart
    """
    chart_obj = JsChartDC.JsBuble(self.parent.context.rptObj, data, {'static': {}, 'dynamic': {}})
    return self.parent.context.register(GraphDC.Chart(self.parent.context.rptObj, chart_obj, width, height, title,
                                                      options or {}, htmlCode, filters, profile))
