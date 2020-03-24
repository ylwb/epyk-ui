
from epyk.core.html import geo


class Dc(object):
  def __init__(self, context):
    self.parent = context
    self.chartFamily = "DC"

  def usa(self, record=None, y_columns=None, x_axis=None, title=None, profile=None, options=None, width=(100, "%"),
           height=(330, "px"), htmlCode=None):
    """

    Documentation
    https://jsfiddle.net/djmartin_umich/9VJHe/
    http://bl.ocks.org/KatiRG/cccd23dd7a830da0de5c

    :param record:
    :param y_columns:
    :param x_axis:
    :param title:
    :param profile:
    :param width:
    :param height:
    :param htmlCode:
    """
    geo_chart = geo.GeoDc.ChartGeoChoropleth(self.parent.context.rptObj, width, height, title, options or {}, htmlCode, profile)
    line_id = geo_chart.htmlId
    self.parent.context.rptObj._props.setdefault('js', {}).setdefault('datasets', {})['data_cf_%s' % line_id] = "var %(cId)s_cf = crossfilter(%(data)s); var %(cId)s_dim = %(cId)s_cf.dimension(function(d) {return +d['%(x)s'];})" % {'cId': line_id, 'data': record, 'x': x_axis}
    geo_chart.dom.height(height[0]).dimension("%s_dim" % line_id).group("%(cId)s_dim.group().reduceSum(function(d) {return d['%(y)s'] ;})" % {'cId': line_id, 'y': y_columns})
    self.parent.context.register(geo_chart)
    return geo_chart