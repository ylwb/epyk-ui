# Check if pandas is available in the current environment
# if it is the case this module can handle Dataframe directly
try:
  import pandas as pd
  has_pandas = True

except:
  has_pandas = False

from epyk.core import html
from epyk.core.css import Defaults


class Lists(object):

  def __init__(self, context):
    self.context = context

  def _filter(self, recordSet, column, options=None):
    """
    Description:
    ------------



    Attributes:
    ----------
    :param recordSet:
    :param column:
    :param options: A dictionary with specific filtering options e.g {'allSelected': True, 'operation': 'in'}
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
    Description:
    ------------

    Attributes:
    ----------
    :param recordSet:
    :param column:
    """
    data = None
    is_converted = False
    if has_pandas:
      if isinstance(recordSet, pd.DataFrame):
        data = [{'name': r, 'value': r} for r in recordSet[column].unique().tolist()]
        is_converted = True

    if not is_converted:
      result = {}
      for rec in recordSet:
        result[rec[column]] = {'name': rec[column], 'value': rec[column]}
      data = [result[k] for k in sorted(result.keys())]
    return data

  def select(self, records=None, htmlCode=None, label=None, selected=None, width=(100, "%"), height=(None, "%"), column=None, filter=None, profile=None, multiple=False, options=None):
    """
    Description:
    ------------
    HTML Select component

    Usage::

      rptObj.ui.select(["A", "B", "C"], label="label", selected="C", multiple=True,
                      options={"title": "ttle", 'showTick': True, 'maxOptions': 2})
      s.selected = "B"
      s.change(rptObj.js.console.log(s.dom.val))

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlSelect.Select`

    Related Pages:

			https://silviomoreto.github.io/bootstrap-select/examples/
    https://www.npmjs.com/package/bootstrap-select-v4
    https://www.jqueryscript.net/form/Bootstrap-4-Dropdown-Select-Plugin-jQuery.html

    Attributes:
    ----------
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
    """
    records = records or []
    options = {} if options is None else options

    all_selected = options.get("allSelected", False)
    empty_selected = options.get("empty_selected", True)
    if column is not None:
      if filter is not None:
        if filter == True:
          self._filter(records, column, {'allSelected': all_selected, 'operation': options.get("operation", "in")})
      records = self._recordSet(records, column)
    elif isinstance(records, (list, tuple)) and len(records) > 0 and not isinstance(records[0], dict):
      records = [{'name': rec, 'value': rec} for rec in records]
    if all_selected:
      records = [{'name': 'All', 'value': ''}] + records
    if empty_selected:
      records = [{'name': '', 'value': ''}] + records
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

  def lookup(self, lookupData=None, htmlCode=None, label=None, selected=None, width=(100, "%"), height=(None, "%"), column=None, filter=None, profile=None, multiple=False, options=None):
    """
    Description:
    ------------
    HTML Select component

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlSelect.Lookup`

    Related Pages:

			https://silviomoreto.github.io/bootstrap-select/examples/
    https://www.npmjs.com/package/bootstrap-select-v4
    https://www.jqueryscript.net/form/Bootstrap-4-Dropdown-Select-Plugin-jQuery.html

    Attributes:
    ----------
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
    """
    options = {} if options is None else options
    html_select = html.HtmlSelect.Lookup(self.context.rptObj, lookupData, htmlCode, width, height, filter, profile, multiple, options)
    self.context.register(html_select)
    return html_select

  def item(self, text=None):
    """
    Description:
    ------------

    Usage::

      l = rptObj.ui.lists.list(["A", "B"])

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlList.List`

    Related Pages:

      https://www.w3schools.com/bootstrap/bootstrap_list_groups.asp
    http://astronautweb.co/snippet/font-awesome/
    """
    html_item = html.HtmlList.Li(self.context.rptObj, text)
    self.context.register(html_item)
    return html_item

  def list(self, data=None, color=None, width=('auto', ""), height=(None, 'px'), htmlCode=None, helper=None,
           options=None, profile=None):
    """
    Description:
    ------------

    Usage::

      l = rptObj.ui.lists.list(["A", "B"])

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlList.List`

    Related Pages:

      https://www.w3schools.com/bootstrap/bootstrap_list_groups.asp
    http://astronautweb.co/snippet/font-awesome/
    """
    html_list = html.HtmlList.List(self.context.rptObj, data or [], color, width, height, htmlCode,
                                   helper, options or {}, profile)
    self.context.register(html_list)
    html_list.css({"list-style": 'none'})
    return html_list

  def items(self, records=None, width=(100, "%"), height=(None, "%"), column=None, options=None, htmlCode=None, profile=None, helper=None):
    """
    """

    if column is not None:
      values = set()
      for rec in records:
        values.add(rec[column])
      records = sorted(list(values))

    html_item = html.HtmlList.Items(self.context.rptObj, 'text', records, width, height, options, htmlCode, profile, helper)
    self.context.register(html_item)
    html_item.style.css.padding_left = '15px'
    return html_item

  def numbers(self, data=None, width=('auto', ""), height=(None, 'px'), htmlCode=None, options=None, profile=None, helper=None):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.lists.numbers(["A", "B"])

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlList.List`

    Related Pages:

        https://www.w3schools.com/html/html_lists.asp
    https://www.w3.org/wiki/CSS/Properties/list-style-type
    """
    html_list = html.HtmlList.Items(self.context.rptObj, 'text', data or [], width, height, options or {}, htmlCode, profile, helper)
    self.context.register(html_list)
    html_list.css({"list-style-type": 'decimal'})
    html_list.style.css.padding_left = '15px'
    return html_list

  def alpha(self, data=None, width=('auto', ""), height=(None, 'px'), htmlCode=None, options=None, profile=None, helper=None):
    """
    Description:
    ------------

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlList.List`

    :param data:
    :param color:
    :param width:
    :param height:
    :param htmlCode:
    :param helper:
    :param options:
    :param profile:
    """
    html_list = html.HtmlList.Items(self.context.rptObj, 'text', data or [], width, height, options or {}, htmlCode, profile, helper)
    self.context.register(html_list)
    html_list.css({"list-style-type": 'lower-alpha'})
    html_list.style.css.padding_left = '15px'
    return html_list

  def roman(self, data=None, width=('auto', ""), height=(None, 'px'), htmlCode=None, options=None, profile=None, helper=None):
    """
    Description:
    ------------

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlList.List`

    :param data:
    :param color:
    :param width:
    :param height:
    :param htmlCode:
    :param helper:
    :param options:
    :param profile:
    :return:
    """
    html_list = html.HtmlList.Items(self.context.rptObj, 'text', data or [], width, height, options or {}, htmlCode, profile, helper)
    self.context.register(html_list)
    html_list.css({"list-style-type": 'lower-roman'})
    html_list.style.css.padding_left = '15px'
    return html_list

  def points(self, data=None, width=('auto', ""), height=(None, 'px'), htmlCode=None, options=None, profile=None, helper=None):
    """
    Description:
    ------------

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlList.List`

    Related Pages:

			https://www.w3schools.com/html/html_lists.asp

    Attributes:
    ----------
    :param data:
    :param color:
    :param width:
    :param height:
    :param htmlCode:
    :param helper:
    :param options:
    :param profile:
    """
    html_list = html.HtmlList.Items(self.context.rptObj, 'text', data or [], width, height, options or {}, htmlCode, profile, helper)
    self.context.register(html_list)
    html_list.css({"list-style-type": 'circle'})
    html_list.style.css.padding_left = '15px'
    return html_list

  def disc(self, data=None, width=('auto', ""), height=(None, 'px'), htmlCode=None, helper=None, options=None, profile=None):
    """
    Description:
    ------------

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlList.List`

    Related Pages:

			https://www.w3schools.com/cssref/pr_list-style-type.asp

    Attributes:
    ----------
    :param data:
    :param color:
    :param width:
    :param height:
    :param htmlCode:
    :param helper:
    :param options:
    :param profile:
    """
    html_list = html.HtmlList.Items(self.context.rptObj, 'text', data or [], width, height, options or {}, htmlCode, profile, helper)
    self.context.register(html_list)
    html_list.css({"list-style-type": 'disc'})
    html_list.style.css.padding_left = '15px'
    return html_list

  def squares(self, data=None, width=('auto', ""), height=(None, 'px'), htmlCode=None, helper=None, options=None, profile=None):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.lists.squares(["A", "B"])

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlList.List`

    Related Pages:

        https://www.w3schools.com/cssref/pr_list-style-type.asp

    Attributes:
    ----------
    :param data:
    :param color:
    :param width:
    :param height:
    :param htmlCode:
    :param helper:
    :param options:
    :param profile:
    """
    html_list = html.HtmlList.Items(self.context.rptObj, 'text', data or [], width, height, options or {}, htmlCode, profile, helper)
    self.context.register(html_list)
    html_list.css({"list-style-type": 'square'})
    html_list.style.css.padding_left = '15px'
    return html_list

  def groups(self, data=None, categories=None, color=None, width=('auto', ""), height=(None, 'px'), htmlCode=None, helper=None, profile=None):
    """
    Description:
    ------------

    Usage::

      l = rptObj.ui.lists.groups(["AWW", "B"])
      l.add_list(["D", "E"], category="Test")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlList.Groups`

    Related Pages:

    http://designbump.com/create-a-vertical-accordion-menu-using-css3-tutorial/
    http://thecodeplayer.com/walkthrough/vertical-accordion-menu-using-jquery-css3

    Attributes:
    ----------
    :param data:
    :param categories:
    :param color:
    :param width:
    :param height:
    :param htmlCode:
    :param helper:
    :param profile:
    """
    data = data or []
    categories = categories or [""]
    if len(data) > 0:
      if isinstance(data[0], list):
        categories = [""] * len(data)
      else:
        # This object is expecting a list of lists
        data = [data]
    html_obj = html.HtmlList.Groups(self.context.rptObj, data, categories, color, width, height, htmlCode, helper, profile)
    self.context.register(html_obj)
    return html_obj

  def tree(self, data=None, color=None, width=('auto', ""), height=(None, 'px'), htmlCode=None, helper=None, options=None, profile=None):
    """
    Description:
    ------------

    Usage::

      data = [{"label": 'test', 'items': [{"label": 'child 1', 'color': 'red'}]}]
      rptObj.ui.lists.tree(data)

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlTrees.Tree`

    ----------
    :param data:
    :param width:
    :param height:
    :param htmlCode:
    :param profile:
    """
    html_tree = html.HtmlTrees.Tree(self.context.rptObj, data or [], color, width, height, htmlCode, helper, options, profile)
    self.context.register(html_tree)
    return html_tree

  def dropdown(self, recordSet=None, text="", width=('auto', ""), height=(32, 'px'), htmlCode=None, helper=None, options=None, profile=None):
    """
    Description:
    ------------

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlTrees.DropDown`

    Related Pages:

      http://getbootstrap.com/docs/4.0/components/dropdowns/
      https://www.w3schools.com/bootstrap/tryit.asp?filename=trybs_ref_js_dropdown_multilevel_css&stacked=h
      https://codepen.io/svnt/pen/beEgre

    Attributes:
    ----------
    :param recordSet:
    :param width:
    :param height:
    :param htmlCode:
    :param profile:
    """
    dftl_options = {"width": 70}
    dftl_options.update(options or {})
    html_d = html.HtmlTrees.DropDown(self.context.rptObj, recordSet, text, width, height, htmlCode, helper,
                                     dftl_options, profile)
    self.context.register(html_d)
    return html_d

  def checks(self, data=None, width=('auto', ""), height=(None, 'px'), column=None, htmlCode=None, helper=None, options=None, profile=None):
    """
    Description:
    ------------

    Usage::

      data = [{"label": "python", "value": False}, {"label": "Java", "value": 5}]
      checks = rptObj.ui.lists.checklist(data)

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlList.Checks`

    Related Pages:

    Attributes:
    ----------
    :param data:
    :param width:
    :param height:
    :param column:
    :param htmlCode:
    :param helper:
    :param profile:
    """
    if column is not None:
      values = set()
      for rec in data:
        values.add(rec[column])
      data = sorted(list(values))

    dft_options = {"checked": False}
    if options is not None:
      dft_options.update(options)

    html_list = html.HtmlList.Items(self.context.rptObj, 'check', data or [], width, height, dft_options, htmlCode, profile, helper)
    self.context.register(html_list)
    html_list.css({"list-style": 'none'})
    return html_list

  def badges(self, data=None, width=('auto', ""), height=(None, 'px'), htmlCode=None, helper=None, options=None, profile=None):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.lists.badges([{'label': 'Python', 'value': 12}, {'label': 'R', 'value': 3}])

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlList.Badges`

    Related Pages:

      https://www.w3schools.com/bootstrap/bootstrap_list_groups.asp
      https://v4-alpha.getbootstrap.com/components/list-group/

    Attributes:
    ----------
    :param data:
    :param width:
    :param height:
    :param options:
    :param profile:
    """
    html_list = html.HtmlList.Items(self.context.rptObj, 'badge', data or [], width, height, options or {}, htmlCode, profile, helper)
    self.context.register(html_list)
    html_list.css({"list-style": 'none'})
    return html_list

  def icons(self, data=None, width=('auto', ""), height=(None, 'px'), htmlCode=None, helper=None, options=None, profile=None):
    """
    Description:
    ------------

    Usage::

      rptObj.ui.lists.badges([{'label': 'Python', 'value': 12}, {'label': 'R', 'value': 3}])

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlList.Badges`

    Related Pages:

      https://www.w3schools.com/bootstrap/bootstrap_list_groups.asp
      https://v4-alpha.getbootstrap.com/components/list-group/

    Attributes:
    ----------
    :param data:
    :param width:
    :param height:
    :param options:
    :param profile:
    """
    html_list = html.HtmlList.Items(self.context.rptObj, 'icon', data or [], width, height, options or {}, htmlCode,profile, helper)
    self.context.register(html_list)
    html_list.css({"list-style": 'none'})
    return html_list

  def radios(self, data=None, group_name='group', width=('auto', ""), height=(None, "px"), column=None, htmlCode=None, helper=None, options=None, profile=None):
    """
    Description:
    ------------

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlContainer.Div`
      - :class:`epyk.core.html.HtmlInput.Radio`

    Attributes:
    ----------
    :param data:
    :param group_name:
    :param width:
    :param height:
    :param htmlCode:
    :param helper:
    :param options:
    :param profile:
    """
    if column is not None:
      values = set()
      for rec in data:
        values.add(rec[column])
      data = sorted(list(values))

    html_list = html.HtmlList.Items(self.context.rptObj, 'radio', data or [], width, height, options or {}, htmlCode, profile, helper)
    html_list._jsStyles['group'] = group_name
    self.context.register(html_list)
    html_list.css({"list-style": 'none'})
    return html_list

  def brackets(self, recordSet=None, width=('auto', ""), height=(550, 'px'), options=None, profile=None):
    return self.context.register(html.HtmlList.ListTournaments(self.context.rptObj, recordSet, width, height, options or {}, profile))

  def chips(self, items=None, category='group', placeholder="", width=(100, "%"), height=(60, "px"), htmlCode=None, helper=None, options=None, profile=None):
    """
    Description:
    ------------
    Add a chip (filter) html component

    Usage::

      chips = rptObj.ui.panels.chips()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlEvent.Filters`

    Related Pages:

			https://www.w3schools.com/howto/howto_css_contact_chips.asp

    Attributes:
    ----------
    :param items: List. Selected items
    :param category: String. The group of the items.
    :param placeholder: String. The input field placeholder
    :param width:
    :param height:
    :param htmlCode:
    :param helper:
    :param profile:
    """
    dflt_options = {"item_css": {"padding": '5px', 'border': '1px solid %s' % self.context.rptObj.theme.success[0], 'border-radius': '5px', 'margin': '2px',
                                 "width": 'auto', 'display': 'inline', 'background': 'white'},
                    'category': category, 'visible': True,
                    'value_css': {'font-size': Defaults.font(3), 'font-weight': 'bold', 'vertical-align': 'bottom'},
                    'category_css': {'display': 'inline', 'margin-right': '2px', 'vertical-align': 'top', 'font-size': Defaults.font(-3)},
                    'icon_css': {'color': self.context.rptObj.theme.success[1], 'margin-left': '5px', 'cursor': 'pointer'}}
    if category == 'group':
      dflt_options['visible'] = False
    if options is not None:
      dflt_options.update(options)
    html_f = html.HtmlEvent.Filters(self.context.rptObj, items or [], width, height, htmlCode, helper, dflt_options, profile)
    html_f.input.attr['placeholder'] = placeholder
    self.context.register(html_f)
    return html_f
