
from epyk.interfaces.geo import CompGeoPlotly


class Geo(object):
  def __init__(self, context):
    self.context = context

  @property
  def plotly_map(self):
    """
    Interface for the Plotly library

    Documentation

    :return: A Python Plolty object
    """
    return CompGeoPlotly.Plotly(self)

  @property
  def plotly_choropleth(self):
    """

    :return:
    """
    return CompGeoPlotly.PlotlyChoropleth(self)

  @property
  def plotly_scatter(self):
    """

    https://plot.ly/javascript/scatter-plots-on-maps/

    :return:
    """
    return CompGeoPlotly.PlotlyScatter(self)

  @property
  def plotly_bubble(self):
    """

    https://plot.ly/javascript/bubble-maps/

    :return:
    """
    return CompGeoPlotly.PlotlyBubble(self)