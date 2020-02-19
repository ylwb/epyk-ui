from epyk.core.html import Html

from epyk.core.js.html import JsHtmlSelect
from epyk.core.js import JsUtils


class Radio(Html.Html):
  name, category, callFnc = 'Radio Buttons', 'Buttons', 'radio'

  def __init__(self, report, vals, htmlCode, label, width, height, radioVisible, event,
               withRemoveButton, align, filters, tooltip, radioType, helper, profile):
    items = []
    for v in vals:
      r = report.ui.inputs.radio(v.get('checked', False), v['value'])
      r.inReport = False
      items.append(r)
    super(Radio, self).__init__(report, items, htmlCode=htmlCode, css_attrs={"width": width, "height": height}, globalFilter=filters, profile=profile)
    for v in self.val:
      v.set_attrs(name="name", value="radio_%s" % self.htmlId)

  def __getitem__(self, i):
    return self._vals[i]

  def __add__(self, val):
    r = self._report.ui.inputs.radio(False, val, group_name="radio_%s" % self.htmlId)
    r.inReport = False
    self._vals.append(r)
    return self

  def set_disable(self, text):
    """

    :param text:
    :return:
    """
    for v in self.val:
      if v.val["text"] == text:
        self._report._props.setdefault('js', {}).setdefault("builders", []).append(v.dom.attr("disabled", 'true').r)
    return self

  def set_checked(self, text):
    """

    :param text:
    :return:
    """
    for v in self.val:
      if v.val["text"] == text:
        v.val["value"] = True
    return self

  def __str__(self):
    row = self._report.ui.layouts.div(self.val)
    row.css({"width": 'none'})
    row.inReport = False
    return "<div %s>%s</div>%s" % (self.get_attrs(pyClassNames=self.style.get_classes()), row.html(), self.helper)


class Switch(Html.Html):
  __reqCss, __reqJs = ['bootstrap'], ['bootstrap', 'jquery']
  name, category, callFnc = 'Switch Buttons', 'Buttons', 'switch'

  def __init__(self, report, records, label, color, width, height, htmlCode, profile):
    self.width, self.jsChange = width[0], ''
    super(Switch, self).__init__(report, records, htmlCode=htmlCode, profile=profile,
                                 css_attrs={"width": width, "height": height, 'color': color})
    self.add_label(label) # add for
    # self.label.style.add_classes.radio.switch_label()
    self.style.add_classes.radio.switch_checked()
    self._clicks = {'on': [], 'off': []}
    #
    self.checkbox = report.ui.inputs.checkbox("", width=(None, "%"))
    self.checkbox.style.add_classes.radio.switch_checkbox()
    self.checkbox.inReport = False
    #
    self.switch_label = report.ui.texts.label(report.entities.non_breaking_space, width=(50, "px"))
    self.switch_label.style.clear()
    self.switch_label.style.add_classes.radio.switch_label()
    self.switch_label.inReport = False
    self.switch_label.style.css.line_height = "18px"

    self.switch_text = report.ui.tags.p(self.val['on'])
    self.switch_text.css({"display": "inline-block", "margin-left": "3px", "font-weight": "bold"})
    self.switch_text.tooltip(self.val.get('text', ''))
    self.switch_text.inReport = False

    # self.css({"display": 'inline-block'})
    self.switch = self.dom.querySelector("label")
    # data should be stored for this object
    self._report._props.setdefault('js', {}).setdefault("builders", []).append("var %s_data = %s" % (self.htmlCode, records))

  @property
  def dom(self):
    """
    HTML Dom object

    :rtype: JsHtmlSelect.JsHtmlSwitch
    """
    if self._dom is None:
      self._dom = JsHtmlSelect.JsHtmlSwitch(self, report=self._report)
    return self._dom

  @property
  def _js__builder__(self):
    return '''
      if (data.off == data.checked){htmlObj.querySelector("input").checked = false; htmlObj.querySelector("p").innerHTML = data.off}
      else {htmlObj.querySelector("input").checked = true; htmlObj.querySelector("p").innerHTML = data.on}'''

  def click(self, onFncs=None, offFncs=None):
    """
    Description:
    ------------
    Set the click property for the Switch

    Usage:
    ------
    sw = rptObj.ui.buttons.switch({'on': "true", 'off': 'false'})
    sw.click([
      rptObj.js.console.log(sw.content)
    ])

    Attributes:
    ----------
    :param onFncs: List. The list of JavaScript functions
    :param offFncs: List. The list of JavaScript functions
    """
    if onFncs is not None:
      if not isinstance(onFncs, list):
        onFncs = [onFncs]
      self._clicks['on'].extend(onFncs)
    if offFncs is not None:
      if not isinstance(offFncs, list):
        offFncs = [offFncs]
      self._clicks['off'].extend(offFncs)

  def __str__(self):
    self._report._props.setdefault('js', {}).setdefault("builders", []).append(
      self.switch.onclick('''
        var input_check = this.parentNode.querySelector('input');
        if(input_check.checked){%(clickOn)s; this.parentNode.querySelector('p').innerHTML = %(htmlCode)s_data.on; input_check.checked = false}
        else {%(clickOff)s; input_check.checked = true; this.parentNode.querySelector('p').innerHTML = %(htmlCode)s_data.off}
        ''' % {'clickOn': JsUtils.jsConvertFncs(self._clicks["on"], toStr=True), "htmlCode": self.htmlCode,
               'clickOff': JsUtils.jsConvertFncs(self._clicks["off"], toStr=True)}).toStr())
    return '''
      <div %s>%s %s %s</div>''' % (self.get_attrs(pyClassNames=self.style.get_classes()),
                                   self.checkbox.html(), self.switch_label.html(), self.switch_text.html())
