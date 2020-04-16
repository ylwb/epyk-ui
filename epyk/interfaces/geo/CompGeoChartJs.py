
from epyk.core.html import geo


class ChartJs(object):
  def __init__(self, context):
    self.parent = context
    self.chartFamily = "ChartJs"

  def usa(self, record=None, y_columns=None, x_axis=None, title=None, profile=None, options=None, width=(100, "%"),
           height=(330, "px"), htmlCode=None):
    """

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoChartJs.Choropleth`

    :param record:
    :param y_columns:
    :param x_axis:
    :param title:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    :return:
    """
    geo_chart = geo.GeoChartJs.Choropleth(self.parent.context.rptObj, width, height, htmlCode, options or {}, profile)
    self.parent.context.register(geo_chart)
    return geo_chart

  def world_map(self, record=None, y_columns=None, x_axis=None, title=None, profile=None, options=None, width=(100, "%"),
           height=(330, "px"), htmlCode=None):
    """
    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoChartJs.Choropleth`

    :param record:
    :param y_columns:
    :param x_axis:
    :param title:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    :return:
    """
    geo_chart = geo.GeoChartJs.Choropleth(self.parent.context.rptObj, width, height, htmlCode, options or {}, profile)
    self.parent.context.register(geo_chart)
    return geo_chart
