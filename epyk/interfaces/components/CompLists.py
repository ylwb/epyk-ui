"""

"""

# Check if pandas is available in the current environment
# if it is the case this module can handle Dataframe directly
try:
  import pandas as pd
  has_pandas = True

except:
  has_pandas = False

from epyk.core import html


class Lists(object):
  """

  """

  def __init__(self, context):
    self.context = context

  def _filter(self, recordSet, column, options=None):
    """

    :param recordSet:
    :param column:
    :param options: A dictionary with specific filtering options e.g {'allSelected': True, 'operation': 'in'}
    :return:
    """
    dataId = id(recordSet)
    dataCode = "df_code_%s" % dataId
    globalFilter = {'jsId': dataCode, 'colName': column}
    globalFilter.update({options})
    if not dataCode in self.context.rptObj.jsSources:
      self.context.rptObj.jsSources[dataCode] = {'dataId': dataId, 'containers': [], 'data': recordSet}
      self.context.rptObj.jsSources[dataCode]['containers'].append(self)
    return globalFilter

  def _recordSet(self, recordSet, column):
    """

    :param recordSet:
    :param column:
    :return:
    """
    data = None
    is_converted = False
    if has_pandas:
      if isinstance(recordSet, pd.DataFrame):
        data = [{'name': r, 'value': r} for r in recordSet[column].unique().tolist()]
        is_converted = True

    if not is_converted:
      result = set([])
      for rec in recordSet:
        result.add({'name': rec[column], 'value': rec[column]})
      data = list(result)
    return data

  def select(self, records, htmlCode=None, label=None, selected=None, width=(100, "%"), height=(None, "%"),
             column=None, filter=None, profile=None, multiple=False, options=None):
    """
    HTML Select component

    Example
    rptObj.ui.select(["A", "B", "C"], label="label", selected="C", multiple=True,
                      options={"title": "ttle", 'showTick': True, 'maxOptions': 2})
    s.selected = "B"
    s.change(rptObj.js.console.log(s.dom.val))

    Documentation
    https://silviomoreto.github.io/bootstrap-select/examples/
    https://www.npmjs.com/package/bootstrap-select-v4
    https://www.jqueryscript.net/form/Bootstrap-4-Dropdown-Select-Plugin-jQuery.html

    :param records: The input data. Can be a list or a dataFrame
    :param htmlCode: Optional. The component identifier code (for bot
    :param label: Optional. The HTML label attached to the component
    :param selected: The selected values
    :param width: Optional. Integer for the component width
    :param height: Optional. Integer for the component height
    :param column:
    :param filter:
    :param profile: Optional. A flag to set the component performance storage
    :param multiple: Boolean. To set if the component can handle multiple selections
    :param options: The select options as defined https://developer.snapappointments.com/bootstrap-select/options/
    :rtype: html.HtmlSelect.Select
    :return:
    """
    options = {} if options is None else options
    all_selected = options.get("allSelected", False)
    if column is not None:
      if filter is not None:
        if filter == True:
          self._filter(records, column, {'allSelected': all_selected, 'operation': options.get("operation", "in")})
      records = self._recordSet(records, column)
    elif isinstance(records, (list, tuple)) and len(records) > 0 and not isinstance(records[0], dict):
      records = [{'name': rec, 'value': rec} for rec in records]
    if all_selected:
      records = [{'name': 'All', 'value': ''}] + records
    if multiple:
      if not isinstance(multiple, dict):
        multiple = {"max": 2}
      if selected is not None:
        for rec in records:
          if rec["value"] in selected:
            rec["selected"] = True
      return self.context.register(
        html.HtmlSelect.Select(self.context.rptObj, records, htmlCode, width, height, filter, profile, multiple, options))

    if selected is not None:
      for rec in records:
        if rec["value"] == selected:
          rec["selected"] = True
    html_select = html.HtmlSelect.Select(self.context.rptObj, records, htmlCode, width, height, filter, profile, multiple, options)
    self.context.register(html_select)
    return html_select

  def list(self, data=None, size=(None, "px"), color=None, width=(100, "%"), height=(None, 'px'),
           htmlCode=None, helper=None, options=None, profile=None):
    """
    Example
    l = rptObj.ui.lists.list(["A", "B"])

    Documentation
    https://www.w3schools.com/bootstrap/bootstrap_list_groups.asp
    http://astronautweb.co/snippet/font-awesome/
    """
    size = self.context._size(size)
    html_list = html.HtmlList.List(self.context.rptObj, data or [], size, color, width, height, htmlCode,
                                   helper, options, profile)
    self.context.register(html_list)
    html_list.css({"list-style": 'none'})
    return html_list

  def numbers(self, data=None, size=(None, "px"), color=None, width=(100, "%"), height=(None, 'px'),
                  htmlCode=None, helper=None, options=None, profile=None):
    """
    Example
    rptObj.ui.lists.numbers(["A", "B"])

    Documentation
    https://www.w3schools.com/html/html_lists.asp
    https://www.w3.org/wiki/CSS/Properties/list-style-type
    """
    size = self.context._size(size)
    html_list = html.HtmlList.List(self.context.rptObj, data or [], size, color, width, height, htmlCode,
                                   helper, options, profile)
    self.context.register(html_list)
    html_list.css({"list-style-type": 'decimal'})
    return html_list

  def alpha(self, data=None, size=(None, "px"), color=None, width=(100, "%"), height=(None, 'px'),
                  htmlCode=None, helper=None, options=None, profile=None):

    size = self.context._size(size)
    html_list = html.HtmlList.List(self.context.rptObj, data or [], size, color, width, height, htmlCode,
                                   helper, options, profile)
    self.context.register(html_list)
    html_list.css({"list-style-type": 'lower-alpha'})
    return html_list

  def roman(self, data=None, size=(None, "px"), color=None, width=(100, "%"), height=(None, 'px'),
                  htmlCode=None, helper=None, options=None, profile=None):

    size = self.context._size(size)
    html_list = html.HtmlList.List(self.context.rptObj, data or [], size, color, width, height, htmlCode,
                                   helper, options, profile)
    self.context.register(html_list)
    html_list.css({"list-style-type": 'lower-roman'})
    return html_list

  def points(self, data=None, size=(None, "px"), color=None, width=(100, "%"), height=(None, 'px'),
             htmlCode=None, helper=None, options=None, profile=None):
    """

    Documentation
    https://www.w3schools.com/html/html_lists.asp
    """
    size = self.context._size(size)
    html_list = html.HtmlList.List(self.context.rptObj, data or [], size, color, width, height, htmlCode,
                                   helper, options, profile)
    self.context.register(html_list)
    html_list.css({"list-style-type": 'circle'})
    return html_list

  def disc(self, data=None, size=(None, "px"), color=None, width=(100, "%"), height=(None, 'px'),
             htmlCode=None, helper=None, options=None, profile=None):
    """

    Documentation
    https://www.w3schools.com/cssref/pr_list-style-type.asp
    """
    size = self.context._size(size)
    html_list = html.HtmlList.List(self.context.rptObj, data or [], size, color, width, height, htmlCode,
                                   helper, options, profile)
    self.context.register(html_list)
    html_list.css({"list-style-type": 'disc'})
    return html_list

  def squares(self, data=None, size=(None, "px"), color=None, width=(100, "%"), height=(None, 'px'),
             htmlCode=None, helper=None, options=None, profile=None):
    """

    Documentation
    https://www.w3schools.com/cssref/pr_list-style-type.asp
    """
    size = self.context._size(size)
    html_list = html.HtmlList.List(self.context.rptObj, data or [], size, color, width, height, htmlCode,
                                   helper, options, profile)
    self.context.register(html_list)
    html_list.css({"list-style-type": 'square'})
    return html_list

  def groups(self, data=None, categories=None, size=(None, "px"), color=None, width=(100, "%"), height=(None, 'px'),
             htmlCode=None, helper=None, profile=None):
    """

    Example
    l = rptObj.ui.lists.groups(["AWW", "B"])
    l.add_list(["D", "E"], category="Test")

    Documentation
    http://designbump.com/create-a-vertical-accordion-menu-using-css3-tutorial/
    http://thecodeplayer.com/walkthrough/vertical-accordion-menu-using-jquery-css3
    """
    size = self.context._size(size)
    data = data or []
    categories = categories or [""]
    if len(data) > 0:
      if isinstance(data[0], list):
        categories = [""] * len(data)
      else:
        # This object is expecting a list of lists
        data = [data]
    html_obj = html.HtmlList.Groups(self.context.rptObj, data, categories, size, color, width, height, htmlCode,
                                    helper, profile)
    self.context.register(html_obj)
    return html_obj

  def checklist(self, data=None, size=(None, "px"), color=None, width=(100, "%"), height=(None, 'px'),
                htmlCode=None, helper=None, profile=None):
    """

    Example
    data = [{"label": "python", "value": False}, {"label": "Java", "value": 5}]
    checks = rptObj.ui.lists.checklist(data)

    :param data:
    :param size:
    :param color:
    :param width:
    :param height:
    :param htmlCode:
    :param helper:
    :param profile:
    """
    html_obj = html.HtmlList.Checks(self.context.rptObj, data or [], size, color, width, height, htmlCode,
                                       helper, profile)
    self.context.register(html_obj)
    return html_obj

  def tree(self, data=None, size=(None, "px"), color=None, width=(100, "%"), height=(None, 'px'),
           htmlCode=None, helper=None, profile=None):
    """

    Example
    data = [{"label": 'test', 'items': [{"label": 'child 1', 'color': 'red'}]}]
    rptObj.ui.lists.tree(data)

    :param data:
    :param width:
    :param height:
    :param htmlCode:
    :param profile:
    """
    html_tree = html.HtmlTrees.Tree(self.context.rptObj, data or [], size, color, width, height, htmlCode, helper, profile)
    self.context.register(html_tree)
    return html_tree

  def dropdown(self, recordSet=None, size=(None, "px"), color=None, width=(100, "%"), height=(32, 'px'), htmlCode=None,
               helper=None, profile=None):
    """

    Documentation
    http://getbootstrap.com/docs/4.0/components/dropdowns/
    https://www.w3schools.com/bootstrap/tryit.asp?filename=trybs_ref_js_dropdown_multilevel_css&stacked=h
    https://codepen.io/svnt/pen/beEgre

    :param recordSet:
    :param size:
    :param width:
    :param height:
    :param htmlCode:
    :param profile:
    :return:
    """
    size = self.context._size(size)
    html_d = html.HtmlTrees.DropDown(self.context.rptObj, recordSet, size, color, width, height, htmlCode, helper, profile)
    self.context.register(html_d)
    return html_d

  def badges(self, data=None, size=(None, "px"), color=None, width=(100, "%"), height=(None, 'px'),
             htmlCode=None, helper=None, profile=None):
    """

    Example
    rptObj.ui.lists.badges([{'label': 'Python', 'value': 12}, {'label': 'R', 'value': 3}])

    Documentation
    https://www.w3schools.com/bootstrap/bootstrap_list_groups.asp
    https://v4-alpha.getbootstrap.com/components/list-group/

    :param data:
    :param size:
    :param color:
    :param width:
    :param height:
    :param profile:
    """
    size = self.context._size(size)
    html_obj = html.HtmlList.Badges(self.context.rptObj, data or [], size, color, width, height, htmlCode,
                                       helper, profile)

    self.context.register(html_obj)
    return html_obj

  def buttons(self, data=None, size=(None, "px"), color=None, width=(100, "%"), height=(None, 'px'),
              htmlCode=None, helper=None, profile=None):
    """

    Example
    rptObj.ui.lists.badges([{'label': 'Python', 'value': 12}, {'label': 'R', 'value': 3}])

    Documentation
    https://www.w3schools.com/bootstrap/bootstrap_list_groups.asp
    https://v4-alpha.getbootstrap.com/components/list-group/

    :param data:
    :param size:
    :param color:
    :param width:
    :param height:
    :param profile:
    """
    size = self.context._size(size)
    html_obj = html.HtmlList.Buttons(self.context.rptObj, data or [], size, color, width, height, htmlCode, helper, profile)

    self.context.register(html_obj)
    return html_obj

  def brackets(self, recordSet=None, width=(100, "%"), height=(550, 'px'), options=None, profile=None):
    return self.context.register(html.HtmlList.ListTournaments(self.context.rptObj, recordSet, width, height, options, profile))
