
import sys

from epyk.core.html import graph


class Billboard(object):
  def __init__(self, context):
    self.parent = context
    self.chartFamily = "Billboard"

  def line(self, record, y_columns=None, x_axis=None, profile=None, width=(100, "%"), height=(330, "px"), options=None, htmlCode=None):
    agg_data = {}
    for rec in record:
      for y in y_columns:
        if y in rec:
          agg_data.setdefault(y, {})[rec[x_axis]] = agg_data.get(y, {}).get(rec[x_axis],  0) + float(rec[y])
    labels, data = set(), []
    for c in y_columns:
      series = []
      for x, y in agg_data[c].items():
        labels.add(x)
        series.append(y)
      data.append(series)

    line_chart = graph.GraphBillboard.ChartLine(self.parent.context.rptObj, width, height, htmlCode, options, profile)
    line_chart.labels(sorted(list(labels)))
    for i, y in enumerate(y_columns):
      line_chart.add_dataset(y, data[i])
    self.parent.context.register(line_chart)
    return line_chart

  def bar(self, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, title='',
           globalFilter=None, filterSensitive=True, profile=None, dataSrc=None, xAxisOrder=None, chartOptions=None,
           width=100, widthUnit="%", height=330, heightUnit="px", htmlCode=None):
    """

    :param aresDf:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param dataFncs:
    :param title:
    :param globalFilter:
    :param filterSensitive:
    :param profile:
    :param dataSrc:
    :param xAxisOrder:
    :param chartOptions:
    :param width:
    :param widthUnit:
    :param height:
    :param heightUnit:
    :param htmlCode:
    :return:
    :rtype: graph.GraphBillboard.Chart
    """
    return self.parent.context.chart(chartType=sys._getframe().f_code.co_name, aresDf=aresDf, seriesNames=seriesNames,
                                     xAxis=xAxis, otherDims=otherDims, dataFncs=dataFncs, title=title, chartFamily=self.chartFamily,
                                     globalFilter=globalFilter, filterSensitive=filterSensitive, profile=profile, dataSrc=dataSrc,
                                     xAxisOrder=xAxisOrder, chartOptions=chartOptions, width=width, widthUnit=widthUnit,
                                     height=height, heightUnit=heightUnit, htmlCode=htmlCode)

  def hbar(self, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, title='',
           globalFilter=None, filterSensitive=True, profile=None, dataSrc=None, xAxisOrder=None, chartOptions=None,
           width=100, widthUnit="%", height=330, heightUnit="px", htmlCode=None):
    """

    :param aresDf:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param dataFncs:
    :param title:
    :param globalFilter:
    :param filterSensitive:
    :param profile:
    :param dataSrc:
    :param xAxisOrder:
    :param chartOptions:
    :param width:
    :param widthUnit:
    :param height:
    :param heightUnit:
    :param htmlCode:
    :return:
    :rtype: graph.GraphBillboard.Chart
    """
    return self.parent.context.chart(chartType=sys._getframe().f_code.co_name, aresDf=aresDf, seriesNames=seriesNames,
                                     xAxis=xAxis, otherDims=otherDims, dataFncs=dataFncs, title=title, chartFamily=self.chartFamily,
                                     globalFilter=globalFilter, filterSensitive=filterSensitive, profile=profile, dataSrc=dataSrc,
                                     xAxisOrder=xAxisOrder, chartOptions=chartOptions, width=width, widthUnit=widthUnit,
                                     height=height, heightUnit=heightUnit, htmlCode=htmlCode)

  def scatter(self, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, title='',
           globalFilter=None, filterSensitive=True, profile=None, dataSrc=None, xAxisOrder=None, chartOptions=None,
           width=100, widthUnit="%", height=330, heightUnit="px", htmlCode=None):
    """

    :param aresDf:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param dataFncs:
    :param title:
    :param globalFilter:
    :param filterSensitive:
    :param profile:
    :param dataSrc:
    :param xAxisOrder:
    :param chartOptions:
    :param width:
    :param widthUnit:
    :param height:
    :param heightUnit:
    :param htmlCode:
    :return:
    :rtype: graph.GraphBillboard.Chart
    """
    return self.parent.context.chart(chartType=sys._getframe().f_code.co_name, aresDf=aresDf, seriesNames=seriesNames,
                                     xAxis=xAxis, otherDims=otherDims, dataFncs=dataFncs, title=title, chartFamily=self.chartFamily,
                                     globalFilter=globalFilter, filterSensitive=filterSensitive, profile=profile, dataSrc=dataSrc,
                                     xAxisOrder=xAxisOrder, chartOptions=chartOptions, width=width, widthUnit=widthUnit,
                                     height=height, heightUnit=heightUnit, htmlCode=htmlCode)

  def spline(self, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, title='',
           globalFilter=None, filterSensitive=True, profile=None, dataSrc=None, xAxisOrder=None, chartOptions=None,
           width=100, widthUnit="%", height=330, heightUnit="px", htmlCode=None):
    """

    :param aresDf:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param dataFncs:
    :param title:
    :param globalFilter:
    :param filterSensitive:
    :param profile:
    :param dataSrc:
    :param xAxisOrder:
    :param chartOptions:
    :param width:
    :param widthUnit:
    :param height:
    :param heightUnit:
    :param htmlCode:
    :return:
    :rtype: graph.GraphBillboard.Chart
    """
    return self.parent.context.chart(chartType=sys._getframe().f_code.co_name, aresDf=aresDf, seriesNames=seriesNames,
                                     xAxis=xAxis, otherDims=otherDims, dataFncs=dataFncs, title=title, chartFamily=self.chartFamily,
                                     globalFilter=globalFilter, filterSensitive=filterSensitive, profile=profile, dataSrc=dataSrc,
                                     xAxisOrder=xAxisOrder, chartOptions=chartOptions, width=width, widthUnit=widthUnit,
                                     height=height, heightUnit=heightUnit, htmlCode=htmlCode)

  def step(self, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, title='',
           globalFilter=None, filterSensitive=True, profile=None, dataSrc=None, xAxisOrder=None, chartOptions=None,
           width=100, widthUnit="%", height=330, heightUnit="px", htmlCode=None):
    """

    :param aresDf:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param dataFncs:
    :param title:
    :param globalFilter:
    :param filterSensitive:
    :param profile:
    :param dataSrc:
    :param xAxisOrder:
    :param chartOptions:
    :param width:
    :param widthUnit:
    :param height:
    :param heightUnit:
    :param htmlCode:
    :return:
    :rtype: graph.GraphBillboard.Chart
    """
    return self.parent.context.chart(chartType=sys._getframe().f_code.co_name, aresDf=aresDf, seriesNames=seriesNames,
                                     xAxis=xAxis, otherDims=otherDims, dataFncs=dataFncs, title=title, chartFamily=self.chartFamily,
                                     globalFilter=globalFilter, filterSensitive=filterSensitive, profile=profile, dataSrc=dataSrc,
                                     xAxisOrder=xAxisOrder, chartOptions=chartOptions, width=width, widthUnit=widthUnit,
                                     height=height, heightUnit=heightUnit, htmlCode=htmlCode)

  def area(self, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, title='',
           globalFilter=None, filterSensitive=True, profile=None, dataSrc=None, xAxisOrder=None, chartOptions=None,
           width=100, widthUnit="%", height=330, heightUnit="px", htmlCode=None):
    """

    :param aresDf:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param dataFncs:
    :param title:
    :param globalFilter:
    :param filterSensitive:
    :param profile:
    :param dataSrc:
    :param xAxisOrder:
    :param chartOptions:
    :param width:
    :param widthUnit:
    :param height:
    :param heightUnit:
    :param htmlCode:
    :return:
    :rtype: graph.GraphBillboard.Chart
    """
    return self.parent.context.chart(chartType=sys._getframe().f_code.co_name, aresDf=aresDf, seriesNames=seriesNames,
                                     xAxis=xAxis, otherDims=otherDims, dataFncs=dataFncs, title=title, chartFamily=self.chartFamily,
                                     globalFilter=globalFilter, filterSensitive=filterSensitive, profile=profile, dataSrc=dataSrc,
                                     xAxisOrder=xAxisOrder, chartOptions=chartOptions, width=width, widthUnit=widthUnit,
                                     height=height, heightUnit=heightUnit, htmlCode=htmlCode)

  def pie(self, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, title='',
           globalFilter=None, filterSensitive=True, profile=None, dataSrc=None, xAxisOrder=None, chartOptions=None,
           width=100, widthUnit="%", height=330, heightUnit="px", htmlCode=None):
    """

    :param aresDf:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param dataFncs:
    :param title:
    :param globalFilter:
    :param filterSensitive:
    :param profile:
    :param dataSrc:
    :param xAxisOrder:
    :param chartOptions:
    :param width:
    :param widthUnit:
    :param height:
    :param heightUnit:
    :param htmlCode:
    :return:
    :rtype: graph.GraphBillboard.Chart
    """
    return self.parent.context.chart(chartType=sys._getframe().f_code.co_name, aresDf=aresDf, seriesNames=seriesNames,
                                     xAxis=xAxis, otherDims=otherDims, dataFncs=dataFncs, title=title, chartFamily=self.chartFamily,
                                     globalFilter=globalFilter, filterSensitive=filterSensitive, profile=profile, dataSrc=dataSrc,
                                     xAxisOrder=xAxisOrder, chartOptions=chartOptions, width=width, widthUnit=widthUnit,
                                     height=height, heightUnit=heightUnit, htmlCode=htmlCode)

  def donut(self, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, title='',
           globalFilter=None, filterSensitive=True, profile=None, dataSrc=None, xAxisOrder=None, chartOptions=None,
           width=100, widthUnit="%", height=330, heightUnit="px", htmlCode=None):
    """

    :param aresDf:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param dataFncs:
    :param title:
    :param globalFilter:
    :param filterSensitive:
    :param profile:
    :param dataSrc:
    :param xAxisOrder:
    :param chartOptions:
    :param width:
    :param widthUnit:
    :param height:
    :param heightUnit:
    :param htmlCode:
    :return:
    :rtype: graph.GraphBillboard.Chart
    """
    return self.parent.context.chart(chartType=sys._getframe().f_code.co_name, aresDf=aresDf, seriesNames=seriesNames,
                                     xAxis=xAxis, otherDims=otherDims, dataFncs=dataFncs, title=title, chartFamily=self.chartFamily,
                                     globalFilter=globalFilter, filterSensitive=filterSensitive, profile=profile, dataSrc=dataSrc,
                                     xAxisOrder=xAxisOrder, chartOptions=chartOptions, width=width, widthUnit=widthUnit,
                                     height=height, heightUnit=heightUnit, htmlCode=htmlCode)

  def gauge(self, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, title='',
           globalFilter=None, filterSensitive=True, profile=None, dataSrc=None, xAxisOrder=None, chartOptions=None,
           width=100, widthUnit="%", height=330, heightUnit="px", htmlCode=None):
    """

    :param aresDf:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param dataFncs:
    :param title:
    :param globalFilter:
    :param filterSensitive:
    :param profile:
    :param dataSrc:
    :param xAxisOrder:
    :param chartOptions:
    :param width:
    :param widthUnit:
    :param height:
    :param heightUnit:
    :param htmlCode:
    :return:
    :rtype: graph.GraphBillboard.Chart
    """
    return self.parent.context.chart(chartType=sys._getframe().f_code.co_name, aresDf=aresDf, seriesNames=seriesNames,
                                     xAxis=xAxis, otherDims=otherDims, dataFncs=dataFncs, title=title, chartFamily=self.chartFamily,
                                     globalFilter=globalFilter, filterSensitive=filterSensitive, profile=profile, dataSrc=dataSrc,
                                     xAxisOrder=xAxisOrder, chartOptions=chartOptions, width=width, widthUnit=widthUnit,
                                     height=height, heightUnit=heightUnit, htmlCode=htmlCode)

  def radar(self, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, title='',
           globalFilter=None, filterSensitive=True, profile=None, dataSrc=None, xAxisOrder=None, chartOptions=None,
           width=100, widthUnit="%", height=330, heightUnit="px", htmlCode=None):
    """

    :param aresDf:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param dataFncs:
    :param title:
    :param globalFilter:
    :param filterSensitive:
    :param profile:
    :param dataSrc:
    :param xAxisOrder:
    :param chartOptions:
    :param width:
    :param widthUnit:
    :param height:
    :param heightUnit:
    :param htmlCode:
    :return:
    :rtype: graph.GraphBillboard.Chart
    """
    return self.parent.context.chart(chartType=sys._getframe().f_code.co_name, aresDf=aresDf, seriesNames=seriesNames,
                                     xAxis=xAxis, otherDims=otherDims, dataFncs=dataFncs, title=title, chartFamily=self.chartFamily,
                                     globalFilter=globalFilter, filterSensitive=filterSensitive, profile=profile, dataSrc=dataSrc,
                                     xAxisOrder=xAxisOrder, chartOptions=chartOptions, width=width, widthUnit=widthUnit,
                                     height=height, heightUnit=heightUnit, htmlCode=htmlCode)

  def bubble(self, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, title='',
           globalFilter=None, filterSensitive=True, profile=None, dataSrc=None, xAxisOrder=None, chartOptions=None,
           width=100, widthUnit="%", height=330, heightUnit="px", htmlCode=None):
    """

    Online chart Documentation: https://naver.github.io/billboard.js/demo/#Chart.BubbleChart

    :param aresDf:
    :param seriesNames:
    :param xAxis:
    :param otherDims:
    :param dataFncs:
    :param title:
    :param globalFilter:
    :param filterSensitive:
    :param profile:
    :param dataSrc:
    :param xAxisOrder:
    :param chartOptions:
    :param width:
    :param widthUnit:
    :param height:
    :param heightUnit:
    :param htmlCode:
    :return:
    :rtype: graph.GraphBillboard.Chart
    """
    return self.parent.context.chart(chartType=sys._getframe().f_code.co_name, aresDf=aresDf, seriesNames=seriesNames,
                                     xAxis=xAxis, otherDims=otherDims, dataFncs=dataFncs, title=title, chartFamily=self.chartFamily,
                                     globalFilter=globalFilter, filterSensitive=filterSensitive, profile=profile, dataSrc=dataSrc,
                                     xAxisOrder=xAxisOrder, chartOptions=chartOptions, width=width, widthUnit=widthUnit,
                                     height=height, heightUnit=heightUnit, htmlCode=htmlCode)
