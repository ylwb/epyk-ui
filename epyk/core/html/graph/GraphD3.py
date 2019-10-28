"""

"""

# https://bl.ocks.org/ctufts/f38ef0187f98c537d791d24fda4a6ef9
import json

from epyk.core.js import Imports
from epyk.core.html import Html
from epyk.core.html.graph import GraphFabric

# The list of CSS classes
from epyk.core.css.groups import CssGrpCls


class Chart(Html.Html):
  """

  """
  name, category, callFnc = 'D3', 'Charts', 'plotChartD3'
  _grpCls = CssGrpCls.CssGrpClassBase
  __reqJs = ['d3']
  references = {
    'Website': 'https://d3js.org/',
    'Website2': 'https://d3plus.org/examples/',
  }

  def __init__(self, aresObj, chartType, data, width, widthUnit, height, heightUnit, title, chartOptions, toolsbar,
               htmlCode, globalFilter, filterSensitive, dataSrc, profile):
    if chartOptions is None:
      chartOptions = {}
    if GraphFabric.CHARTS_FACTORY is None:
      GraphFabric.CHARTS_FACTORY = GraphFabric.loadFactory()  # atomic function to store all the different table mapping
    self.title, self.toolsbar, self.seriesProperties, self.height = title, toolsbar, {'static': {}, 'dynamic': {}}, height
    super(Chart, self).__init__(aresObj, [], code=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, dataSrc=dataSrc)
    self.__chart = GraphFabric.CHARTS_FACTORY[self.name][chartType](aresObj, data, self.seriesProperties)
    self.__chart.data.attach(self)
    self.__chart.data._schema['out']['params'] = tuple(list(self.__chart.data._schema['out']['params']) + [self.htmlId])
    # self.__chart.data.post(('extend-dataset', self.seriesProperties, 'datasets'))
    self.__chart['chart_colors'] = json.dumps(aresObj.getColor('charts'))
    self.setSeriesColor(aresObj.getColor('charts'))
    self.css({'position': 'relative'})
    self.__chart.addAttr('position', chartOptions.get('legend', {'position': 'right'}).get('position', 'right'), ['legend'], category='options')
    self.__chart.addAttr('bottom', 20, ['layout', 'padding'], category='options')
    self.aresObj.jsGlobal.fnc('%s(%s)' % (self.__chart.jsCls, ', '.join(self.__chart.jsClsParams)), self.__chart.jsClassDefinition)
    self.colName, self.filterSensitive = list(self.__chart.data._schema['keys'])[0], filterSensitive
    if title:
      self.__chart.addAttr('text', title, ['title'], category='options')
      self.__chart.addAttr('display', True, ['title'], category='options')
    if globalFilter:
      if self._code is None:
        raise Exception("ERROR: ChartJs - %s -  Please add an htmlCode to name your filter" % chartType)

      if globalFilter is True:
        self.filter(data._jqId, self.colName)
      else:
        self.filter(**globalFilter)

  @property
  def chartId(self):
    """
    Return the Javascript variable of the chart
    """
    return "chart_%s" % self.htmlId

  @property
  def jqDiv(self):
    return "d3.select('#%s')" % self.htmlId

  @property
  def jqId(self):
    return "%s.select('svg')" % self.jqDiv

  def onDocumentLoadFnc(self): pass

  def onDocumentReady(self):
    self.ctx = []  # Just to ensure that the Structure of the chart component will not be changed in the python layer
    GraphFabric.Chart.resolveDict(dict([(key, val) for key, val in self.__chart.items() if val]), self.ctx)
    self.aresObj.jsOnLoadFnc.add('''window['%(htmlId)s_def'] = {%(chartDef)s}; %(jsChart)s
          ''' % {'htmlId': self.htmlId, 'chartDef': ", ".join(self.ctx), 'jsChart': self.jsGenerate(None)})

  def setSeriesColor(self, colors, seriesId=None, borderColors=None):
    pass

  def addAttr(self, key, val=None, tree=None, category=None, isPyData=True):
    pass

  def delAttr(self, keys, tree=None, category=None):
    pass

  def jsResize(self):
    self.addGlobalFnc('D3Resize(htmlId)', ''' 
      var container = d3.select(d3.select('#' + htmlId).node());
      var width = parseInt(container.style("width"));
      var height = parseInt(container.style("height"));
      var aspect = width / height;
    
      var svg = d3.select('#' + htmlId).select('svg').attr("viewBox", "0 0 " + width + " " + height)
        .attr("perserveAspectRatio", "xMinYMid").call(resize);  
      d3.select(window).on("resize." + container.attr("id"), resize);
    
      function resize() {
        var targetWidth = parseInt(container.style("width"));
        svg.attr("width", targetWidth);
        svg.attr("height", Math.round(targetWidth / aspect))
      }''')

  def jsRemove(self):
    return "d3.select('#%s').selectAll('svg').remove()" % self.htmlId

  def jsGenerate(self, jsData='data', jsDataKey=None, isPyData=False, jsId=None):
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return '''
       window['%(htmlId)s_def'].data = %(dc)s;
       if(window['%(htmlId)s_chart'] !== undefined){window['%(htmlId)s_chart'].destroy();};
       window['%(htmlId)s_chart'] = new %(jsCls)s('%(htmlId)s', window['%(htmlId)s_def']); %(time)s;
       ''' % {'htmlId': self.htmlId, 'time': GraphFabric.Chart.jsLastUpdate(self.htmlId), 'dc': self.__chart.data.setId(jsData).getJs(filterSensitive=self.filterSensitive), 'jsCls': self.__chart.jsCls}

  def filter(self, jsId, colName, allSelected=True, filterGrp=None, operation="=", itemType="string"):
    raise NotImplemented()

  def click(self, jsFncs):
    pass

  def __str__(self):
    strChart = '<div style="height:%spx" id="%s"></div>' % (self.height-30, self.htmlId)
    return GraphFabric.Chart.html(self, self.strAttr(withId=False, pyClassNames=self.defined), strChart)

  def setSeriesColor(self, colors, seriesId=None, borderColors=None):
    """
    :category:
    :rubric: JS
    :example:
    :dsc:

    """
    self.__chart._colors(colors, seriesId, borderColors)
    return self





class Config(Html.Html):
  name, category, callFnc = 'D3Bespoke', 'Charts', 'chartD3Bespoke'
  __reqJs = ['d3']
  __pyStyle = ['CssDivNoBorder']
  staticUrlMap = {
    'd3-lasso.min.js': 'https://bl.ocks.org/skokenes/raw/a85800be6d89c76c1ca98493ae777572/ec2ac78d8c18d3f85ef6cf7cdb77013096d42da3',
    'cloud.js': 'https://bl.ocks.org/jyucsiro/raw/767539a876836e920e38bc80d2031ba7'
  }

  def __init__(self, aresObj, script, data, width, widthUnit, height, heightUnit, title, chartOptions, toolsbar,
               htmlCode, globalFilter, filterSensitive, dataSrc, profile, url, d3Version):
    self.height = height
    super(Config, self).__init__(aresObj, [], code=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, dataSrc=dataSrc, profile=profile)
    # Override the version of D3
    if d3Version is not None:
      d3Version = '4.13.0' if d3Version == "4" else d3Version
      for mod in Imports.JS_IMPORTS['d3']['modules']:
        mod['version'] = d3Version
    # Load a external script using D3
    if script is not None:
      if url is None:
        # Try to get the script location from the catalog
        url = self.staticUrlMap.get(script)
      Imports.JS_IMPORTS[script] = {'req': [{'alias': 'd3'}], 'modules': [{'reqAlias': 'bootstrap', 'script': script, 'version': '', 'path': '', 'cdnjs': url}]}
      self.aresObj.jsImports.add(script)

  @property
  def jqId(self): return "d3.select('#%s')" % self.htmlId

  @property
  def dataId(self): return "data_%s" % self.htmlId

  def onDocumentLoadFnc(self): pass

  def dataText(self, dataText, dataType="json"):
    if dataType == 'json':
      data = json.loads(dataText)
      self.aresObj.jsOnLoadFnc.add("var %s = %s" % (self.dataId, json.dumps(data)))
    elif dataType == 'csv':
      rows, records = dataText.strip().split("\n"), []
      header = rows[0].strip().split(",")
      for row in rows[1:]:
        records.append(dict(zip(header, row.strip().split(","))))
      self.aresObj.jsOnLoadFnc.add("var %s = %s" % (self.dataId, json.dumps(records)))
    else:
      self.aresObj.jsOnLoadFnc.add("var %s = %s" % (self.dataId, json.dumps(dataText)))
    return self

  def cssText(self, cssText):
    self.aresObj.addCssText(cssText)
    return self

  def jsText(self, jsText):
    self.aresObj.jsOnLoadFnc.add(jsText)
    return self

  def jsGenerate(self, jsData='data', jsDataKey=None, isPyData=False, jsId=None):
    return ""

  def onDocumentReady(self): pass

  def __str__(self):
    strChart = '<svg style="height:%spx" id="%s"></svg>' % (self.height-30, self.htmlId)
    return GraphFabric.Chart.html(self, self.strAttr(withId=False, pyClassNames=self.pyStyle), strChart)




