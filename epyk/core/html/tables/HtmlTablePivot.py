"""
Module in charge of the PivotTable library

Related Pages:

		https://pivottable.js.org/examples/
"""

import json

from epyk.core.html import Html
from epyk.core.js import JsUtils
from epyk.core.js.objects import JsPivotFncs
from epyk.core.html.options import OptTable
from epyk.core.js.packages import JsQuery

# The list of CSS classes
from epyk.core.css.styles import GrpClsTable

extensions = {
  'sub-total': {'jsImports': ['pivot-sub-total']},
  'c3': {'jsImports': ['pivot-c3']},
}


class PivotTable(Html.Html):
  __reqJs, __reqCss = ["pivot"], ["pivot"]
  name = 'Pivot Table'
  js_fncs_opts = ('renderer', 'aggregator', 'onRefresh', 'filter', 'dataClass', 'onRefresh')

  # _grpCls = CssGrpClsTable.CssStylesPivot

  def __init__(self, report, recordSet, rows, cols, width, height, htmlCode, helper, options, profile):
    super(PivotTable, self).__init__(report, recordSet, code=htmlCode, profile=profile, css_attrs={"width": width, "height": height})
    # Add the extra HTML components
    self.add_helper(helper)
    self.__options = OptTable.OptionsPivot(self, options)
    # to add all the columns in the table if nothing defined
    self._jsStyles.update({'cols': cols or [], 'rows': rows or []})
    self.style.css.display = 'block'

  @property
  def style(self):
    if self._styleObj is None:
      self._styleObj = GrpClsTable.Pivot(self)
    return self._styleObj

  @property
  def options(self):
    """
    Description:
    ------------
    Pivot Table options

    :rtype: OptTable.OptionsPivot
    """
    return self.__options

  @property
  def aggregators(self):
    return PivotAggregator(self, self._jsStyles)

  @property
  def renderers(self):
    return PivotRenderer(self, self._jsStyles)

  @property
  def _js__builder__(self):
    return '''
      if (options.showUI){%(jqId)s.pivotUI(data, options)}
      else {%(jqId)s.pivot(data, options)}
      ''' % {"jqId": JsQuery.decorate_var("htmlObj", convert_var=False)}

  # def build(self, data=None, options=None, profile=False):
  #   jsAggFncs = "{%s}" % ", ".join(["'%s': function(attributeArray) {return function(data, rowKey, colKey) {return %s}}" % (name, aggFncs.toJs(self.aggOptions)) for name, aggFncs in self.__aggFncs.items()])
  #   preFnc, endFnc = "", ""
  #   return """ %(preFnc)s;
  #     var tpl = $.pivotUtilities.aggregatorTemplates; window['options_%(htmlId)s'] = %(options)s; %(addinOptions)s;
  #     window['options_%(htmlId)s'].aggregators = %(agg)s;
  #     window['options_%(htmlId)s'].onRefresh = function (config) {
  #         %(jqId)s.find('.pvtVal').each(function( index, items ) {
  #           if (parseFloat(items.innerText.replace(',', '.')) < 0){ $(items).css('color', 'red')}});
  #         %(jqId)s.find('.pvtTotal').each(function( index, items ) {
  #           if (parseFloat(items.innerText.replace(',', '.')) < 0){ $(items).css('color', 'red')}});
  #         %(jqId)s.find('.pvtGrandTotal').each(function( index, items ) {
  #           if (parseFloat(items.innerText.replace(',', '.')) < 0){ $(items).css('color', 'red')}});
  #     };
  #     %(jqId)s.pivotUI([], window['options_%(htmlId)s'])
  #     """ % {'jqId': self.jqId, 'options': json.dumps(self.__pivot), 'agg': jsAggFncs, 'htmlId': self.htmlId, 'addinOptions': ";".join(self.addinOptions), "preFnc": preFnc}

  def __str__(self):
    self._report._props.setdefault('js', {}).setdefault("builders", []).append(self.refresh())
    return '<div %(strAttr)s></div>%(helper)s' % {'strAttr': self.get_attrs(pyClassNames=self.style.get_classes()), "helper": self.helper}


class PivotUITable(PivotTable):
  __reqJs, __reqCss = ["pivot"], ["pivot"]

  def __init__(self, report, recordSet, rows, cols, width, height, htmlCode, helper, options, profile):
    super(PivotUITable, self).__init__(report, recordSet, rows, cols, width, height, htmlCode, helper, options, profile)
    self.__options = OptTable.OptionsPivotUI(self, options)
    # to add all the columns in the table if nothing defined
    self._jsStyles.update({'cols': cols or [], 'rows': rows or []})

  @property
  def options(self):
    """
    Description:
    ------------
    Pivot Table options

    :rtype: OptTable.OptionsPivotUI
    """
    return self.__options

  @property
  def _js__builder__(self):
    return '''
        %(jqId)s.pivotUI(data, options)
        ''' % {"jqId": JsQuery.decorate_var("htmlObj", convert_var=False)}


class PivotAggregator(object):

  def __init__(self, report, options):
    self.report, self.options = report, options

  def sumOverSum(self, cola):
    """
    Description:
    ------------

    :param cola:
    """
    cola = JsUtils.jsConvertData(cola, None)
    self.options['aggregator'] = '$.pivotUtilities.aggregators["Sum over Sum"](%s)' % cola
    self.options['aggregatorName'] = "sumOverSum"

  def count(self):
    """
    Description:
    ------------

    """
    self.options['aggregator'] = '$.pivotUtilities.aggregators["Count"]()'
    self.options['aggregatorName'] = "count"

  def sum(self, col1):
    """
    Description:
    ------------

    """
    col1 = JsUtils.jsConvertData(col1, None)
    self.options['aggregator'] = '$.pivotUtilities.aggregators["Sum"]([%s])' % col1
    self.options['aggregatorName'] = "sum"

  def max(self, col1):
    """
    Description:
    ------------

    """
    self.singleFactorFormulas(col1, "= Math.max(this.tmpVal, col1)")
    self.options['aggregatorName'] = "Max"

  def min(self, col1):
    """
    Description:
    ------------

    """
    self.singleFactorFormulas(col1, "= Math.min(this.tmpVal, col1)")
    self.options['aggregatorName'] = "Min"

  def absSum(self, col1):
    """
    Description:
    ------------

    """
    self.singleFactorFormulas(col1, "+= Math.abs(col1)")
    self.options['aggregatorName'] = "sum (abs)"

  def singleFactorFormulas(self, col1, formula):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param col1:
    :param formula:
    """
    col1 = JsUtils.jsConvertData(col1, None)
    self.options['aggregator'] = '''
      function(keyAgg) { 
        return function(data, rowKey, colKey) {
          return {
            tmpVal: 0, numInputs: 1,
            push: function(record){
              const col1 = record[keyAgg]; this.tmpVal %s; return this.tmpVal},
            value: function() { return this.tmpVal; },
            format: function(x) { return x; },
          }}}(%s)''' % (formula, col1)
    self.options['aggregatorName'] = "diff Abs Agg"

  def twoFactorFormulas(self, col1, col2, formula):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param col1:
    :param col2:
    :param formula:
    """
    col1 = JsUtils.jsConvertData(col1, None)
    col2 = JsUtils.jsConvertData(col2, None)
    self.options['aggregator'] = '''
      function(keyAgg, key2Agg) { 
        return function(data, rowKey, colKey) {
          return {
            tmpVal: 0, numInputs: 2,
            push: function(record){
              const col1 = record[keyAgg]; const col2 = record[key2Agg]; this.tmpVal %s; return this.tmpVal},
            value: function() { return this.tmpVal; },
            format: function(x) { return x; },
          };
        };
      }(%s, %s)''' % (formula, col1, col2)
    self.options['aggregatorName'] = "diff Abs Agg"

  def diffAbsolute(self, col1, col2, formula="+= col1 - col2"):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param col1:
    :param col2:
    :param formula:
    """
    self.twoFactorFormulas(col1, col2, formula)
    self.options['aggregatorName'] = "diff Abs Agg"

  def custom(self, name, js_def):
    """

    https://github.com/nicolaskruchten/pivottable/wiki/Aggregators

    Attributes:
    ----------
    :param name:
    :param js_def:
    """
    self.options['aggregator'] = js_def
    self.options['aggregatorName'] = name


class PivotRenderer(object):

  def __init__(self, report, options):
    self.report, self.options = report, options

  def table(self):
    self.options['renderer'] = '$.pivotUtilities.renderers["table"]'

  def bar(self):
    self.options['renderer'] = '$.pivotUtilities.renderers["Table Barchart"]'

  def heatmap(self):
    self.options['renderer'] = '$.pivotUtilities.renderers["Heatmap"]'

  def custom(self, name, js_def):
    """

    https://github.com/nicolaskruchten/pivottable/wiki/Renderers

    :param name:
    :param js_def:
    """
    pass