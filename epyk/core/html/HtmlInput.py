
import datetime
import json

from epyk.core.html import Html
from epyk.core.html import Defaults
from epyk.core.html.options import OptInputs

#
from epyk.core.js import JsUtils
from epyk.core.js.packages import JsTimepicker
from epyk.core.js.packages import JsQueryUi
from epyk.core.js.html import JsHtmlField
from epyk.core.js.html import JsHtmlJqueryUI

# The list of CSS classes
from epyk.core.css.styles import GrpClsInput


class Output(Html.Html):
  name, category, callFnc = 'Output', 'Inputs', '_output'

  def __str__(self):
    return '<output %(strAttr)s>%(val)s</output>' % {'strAttr': self.get_attrs(pyClassNames=self.pyStyle), 'val': self.val}


class Input(Html.Html):
  name, category, callFnc = 'Input', 'Inputs', 'input'

  def __init__(self, report, text, placeholder, width, height, htmlCode, filter, options, attrs, profile):
    super(Input, self).__init__(report, text, htmlCode=htmlCode, css_attrs={"width": width, "height": height},
                                globalFilter=filter, profile=profile, options=options)
    value = text['value'] if isinstance(text, dict) else text
    self.set_attrs(attrs={"placeholder": placeholder, "type": "text", "value": value, "spellcheck": False})
    self.set_attrs(attrs=attrs)
    self.__options = OptInputs.OptionsInput(self, options)

  @property
  def options(self):
    """
    Property to set all the input component properties

    :rtype: OptSelect.OptionsSelect
    """
    return self.__options

  @property
  def style(self):
    """
    Description:
    ------------
    Property to the CSS Style of the component

    :rtype: GrpClsInput.ClassInput
    """
    if self._styleObj is None:
      self._styleObj = GrpClsInput.ClassInput(self)
    return self._styleObj

  @property
  def _js__builder__(self):
    return '''
      if(typeof options.css !== 'undefined'){for(var k in options.css){htmlObj.style[k] = options.css[k]}}
      
      if(typeof options.formatMoney !== 'undefined'){ htmlObj.value = accounting.formatMoney(data, 
        options.formatMoney.symbol, options.formatMoney.digit, 
        options.formatMoney.thousand, options.formatMoney.decimal)}
      else if(typeof options.formatNumber !== 'undefined'){ htmlObj.value = accounting.formatNumber(data,
        options.formatNumber.digit, options.formatNumber.thousand)}
      else if(typeof options.toFixed !== 'undefined'){ htmlObj.value = accounting.toFixed(data, options.toFixed) }
      else { htmlObj.value = data; }
      '''

  def focus(self, jsFncs=None, profile=False, options=None):
    """
    Action on focus

    :param jsFncs: List or String with the Javascript events
    :param profile: Boolean to add the Javascript fragment to profile
    :param options: Python dictionary with special options (shortcuts) for the component
    """
    if options is not None:
      if jsFncs is None:
        jsFncs = []
      elif not isinstance(jsFncs, list):
        jsFncs = [jsFncs]
      if options.get("reset", False):
        jsFncs.append(self.dom.empty())
    return self.on("focus", jsFncs, profile)

  def autocomplete(self, source):
    """

    :param source:

    :return: Self to allow the chaining
    """
    self._report.js.addOnLoad(['%s.autocomplete({"source": %s})' % (self.dom.jquery.varId, source)])
    return self

  def validation(self, pattern, required=True):
    """
    Add validation rules on the input component

    Example
    input.validation(pattern="[0-9]{5}")

    :param pattern: String.
    :return: Self to allow the chaining
    """
    self.attr["pattern"] = pattern
    if required:
      self.attr["required"] = None
    #self.style.add_classes.input.
    self.style.addCls(["CssInputInValid", "CssInputValid"])
    return self

  def enter(self, jsFncs, profile=False):
    """
    Description:
    ------------
    Add an javascript action when the key enter is pressed on the keyboard

    Example
    htmlObj.input(placeholder="Put your tag").enter("alert()")

    :param jsFncs:
    :param profile:

    :return: The python object itself
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    self.on("keydown", "if(event.keyCode == 13){event.preventDefault(); %s}" % JsUtils.jsConvertFncs(jsFncs, toStr=True), profile)
    return self

  def readonly(self, flag=True):
    """

    :param flag:
    :return:
    """
    if flag:
      self.attr["readonly"] = "readonly"
    else:
      if "readonly" in self.attr:
        del self.attr["readonly"]
    return self

  def __str__(self):
    if 'css' in self._jsStyles:
      self.css(self._jsStyles['css'])
    return '<input %(strAttr)s />' % {'strAttr': self.get_attrs(pyClassNames=self.style.get_classes())}


class InputTime(Input):
  name, callFnc = 'Input Time', 'input'
  __reqCss, __reqJs = ['timepicker'], ['timepicker']

  def __init__(self, report, text, placeholder, width, height, htmlCode, filter, options, attrs, profile):
    if text is None:
      text = str(datetime.datetime.now()).split(" ")[1].split(".")[0]
    super(InputTime, self).__init__(report, text, placeholder, width, height, htmlCode, filter, options, attrs, profile)
    self.__options = OptInputs.OptionsTimePicker(self, options)

  @property
  def options(self):
    """
    Description:
    ------------
    Property to set all the input timepicker component properties

    Related Pages:
    --------------
    https://timepicker.co/options/

    :rtype: OptInputs.OptionsTimePicker
    """
    return self.__options

  @property
  def style(self):
    """
    Description:
    ------------
    Property to the CSS Style of the component

    :rtype: GrpClsInput.ClassInputTime
    """
    if self._styleObj is None:
      self._styleObj = GrpClsInput.ClassInputTime(self)
    return self._styleObj

  @property
  def dom(self):
    """
    Description:
    ------------
    The Javascript Dom object

    :rtype: JsHtmlJqueryUI.JsHtmlTimePicker
    """
    if self._dom is None:
      self._dom = JsHtmlJqueryUI.JsHtmlTimePicker(self, report=self._report)
    return self._dom

  @property
  def js(self):
    """
    Description:
    -----------

    Attributes:
    ----------
    :return: A Javascript Dom object

    :rtype: JsTimepicker.Timepicker
    """
    if self._js is None:
      self._js = JsTimepicker.Timepicker(self, report=self._report)
    return self._js

  @property
  def _js__builder__(self):
    """
    else {
        if (data.value == ''){data.time = new Date()} else{data.time = data.value};
        if (data.options._change.length > 0) {data.options.change = function(time){
            let data = {event_val: time.getHours() +':'+ time.getMinutes() +':'+ time.getSeconds(), event_code: htmlId};
            eval(data.options._change.join(";"))}};
        jQuery(htmlObj).timepicker(data.options); jQuery(htmlObj).timepicker('setTime', data.time)}

    :return:
    """
    return '''
      if (typeof data == "string"){jQuery(htmlObj).timepicker('setTime', data)} 
      jQuery(htmlObj).timepicker(options); '''

  def change(self, jsFnc):
    """
    Description:
    -----------
    Event triggerd when the value of the input field changes. A Date object containing the selected time is passed as the first argument of the callback.
    Note: the variable time is a function parameter received in the Javascript side

    Related Pages:
    --------------
    https://timepicker.co/options/

    :param jsFnc:
    """
    if not isinstance(jsFnc, list):
      jsFnc = [jsFnc]
    self._jsStyles["change"] = "function(time){ %s }" % JsUtils.jsConvertFncs(jsFnc, toStr=True)
    return self

  def __str__(self):
    self._report._props.setdefault('js', {}).setdefault("builders", []).append(self.refresh())
    return '<input %(strAttr)s />' % {'strAttr': self.get_attrs(pyClassNames=self.style.get_classes())}


class InputDate(Input):
  __reqCss, __reqJs = ['jqueryui'], ['jqueryui']
  name, callFnc = 'Input Time', 'input'

  def __init__(self, report, records, placeholder, width, height, htmlCode, filter, options, attrs, profile):
    super(InputDate, self).__init__(report, records, placeholder, width, height, htmlCode, filter, options, attrs, profile)
    self.__options = OptInputs.OptionsDatePicker(self, options)

  @property
  def options(self):
    """
    Description:
    ------------
    Property to set all the input Datepicker component properties

    Related Pages:
    --------------
    https://timepicker.co/options/

    :rtype: OptInputs.OptionsDatePicker
    """
    return self.__options

  @property
  def js(self):
    """
    Description:
    -----------

    Attributes:
    ----------
    :return: A Javascript Dom object

    :rtype: JsQueryUi.Datepicker
    """
    if self._js is None:
      self._js = JsQueryUi.Datepicker(self, report=self._report)
    return self._js

  @property
  def style(self):
    """
    Description:
    ------------
    Property to the CSS Style of the component

    :rtype: GrpClsInput.ClassInput
    """
    if self._styleObj is None:
      self._styleObj = GrpClsInput.ClassInputDate(self)
    return self._styleObj

  @property
  def dom(self):
    """
    Description:
    ------------
    The Javascript Dom object

    :rtype: JsHtmlJqueryUI.JsHtmlDatePicker
    """
    if self._dom is None:
      self._dom = JsHtmlJqueryUI.JsHtmlDatePicker(self, report=self._report)
    return self._dom

  @property
  def _js__builder__(self):
    return '''
      if ((typeof data.options.selectedDts !== "undefined") && (data.options.selectedDts.length > 0)){
        var selectedDt = {};
        data.options.selectedDts.forEach(function(dt){var jsDt = new Date(dt); selectedDt[jsDt.toISOString().split('T')[0]] = jsDt}) ;
        if (data.options.excludeDts === true){ 
          function renderCalendarCallbackExc(intDate) {var utc = intDate.getTime() - intDate.getTimezoneOffset()*60000; var newDate = new Date(utc); var Highlight = selectedDt[newDate.toISOString().split('T')[0]]; if(Highlight){return [false, '', '']} else {return [true, '', '']}}; 
          data.options.beforeShowDay = renderCalendarCallbackExc;
        } else{ 
          function renderCalendarCallback(intDate) {var utc = intDate.getTime() - intDate.getTimezoneOffset()*60000; var newDate = new Date(utc); var Highlight = selectedDt[newDate.toISOString().split('T')[0]]; if(Highlight){return [true, "%s", '']} else {return [false, '', '']}};
          data.options.beforeShowDay = renderCalendarCallback;};
        delete data.options.selectedDts};
      jQuery(htmlObj).datepicker(data.options).datepicker('setDate', data.value)'''

  def __str__(self):
    # Javascript builder is mandatory for this object
    self._report._props.setdefault('js', {}).setdefault("builders", []).append(self.refresh())
    return '<input %(strAttr)s />' % {'strAttr': self.get_attrs(pyClassNames=self.style.get_classes())}


class InputInteger(Input):
  # _grpCls = CssGrpClsInput.CssClassInputInteger
  name, callFnc = 'Input Number', 'input'

  def quantity(self):
    factors, strFcts = {'K': 1000, 'M': 1000000, 'B': 1000000000}, []
    for f, val in factors.items():
      strFcts.append("if(event.key.toUpperCase() == '%s'){$(this).find('input').val($(this).find('input').val() * %s)}" % (f, val))
    self.on('keydown', ";".join(strFcts))
    return self


class InputRange(Input):
  name, callFnc = 'Input Range', 'input'

  def __init__(self, report, text, min, max, step, placeholder, width, height, htmlCode, filter, options, attrs, profile):
    super(InputRange, self).__init__(report, text, placeholder, width, height, htmlCode, filter, options, attrs, profile)
    self.__options = OptInputs.OptionsInputRange(self, options)
    #
    self.input = report.ui.inputs.input(text, width=(None, "px"), placeholder=placeholder).css({"vertical-align": 'middle'})
    self.input.inReport = False
    self.append_child(self.input)
    #
    self.input.set_attrs(attrs={"type": "range", "min": min, "max": max, "step": step})
    if self.options.output:
      self.output = self._report.ui.inputs._output(text).css({
        "width": '15px', "text-align": 'center', "margin-left": '2px', 'color': self._report.theme.success[1]})
      self.output.inReport = False
      self.append_child(self.output)
      self.input.set_attrs(attrs={"oninput": "%s.value=this.value" % self.output.htmlId})
    self.css({"display": 'inline-block', "vertical-align": 'middle', "line-height": '%spx' % Defaults.LINE_HEIGHT})

  @property
  def options(self):
    """
    Property to set input range properties

    :rtype: OptSelect.OptionsInputRange
    """
    return self.__options

  @property
  def style(self):
    """
    Description:
    ------------
    Property to the CSS Style of the component

    :rtype: GrpClsInput.ClassInputRange
    """
    if self._styleObj is None:
      self._styleObj = GrpClsInput.ClassInputRange(self)
    return self._styleObj#

  def __str__(self):
    if hasattr(self, 'output'):
      self.output.css({"display": 'inline-block'})
    return '<div %(strAttr)s></div>' % {'strAttr': self.get_attrs(pyClassNames=self.style.get_classes())}


class Field(Html.Html):
  def __init__(self, report, input, label, placeholder, icon, width, height, htmlCode, helper, profile):
    super(Field, self).__init__(report, "", code=htmlCode, css_attrs={"width": width, "height": height}, profile=profile)
    # Add the component predefined elements
    self.add_label(label)
    self.add_helper(helper, css={"line-height": '%spx' % Defaults.LINE_HEIGHT})
    # add the input item
    self.input = input
    self.append_child(self.input)
    self.add_icon(icon, position="after", css={"margin-left": '5px', 'color': self._report.theme.success[1]})
    self.css({"margin-top": '2px'})

  @property
  def dom(self):
    """
    Javascript Functions

    Return all the Javascript functions defined for an HTML Component.
    Those functions will use plain javascript by default.

    :return: A Javascript Dom object

    :rtype: JsHtmlField.JsHtmlFields
    """
    if self._dom is None:
      self._dom = JsHtmlField.JsHtmlFields(self, report=self._report)
    return self._dom

  def __str__(self):
    str_div = "".join([v.html() if hasattr(v, 'html') else v for v in self.val])
    return "<div %s>%s%s</div>" % (self.get_attrs(pyClassNames=self.style.get_classes()), str_div, self.helper)


class FieldInput(Field):

  def __init__(self, report, value, label, placeholder, icon, width, height, htmlCode, helper, profile):
    input = report.ui.inputs.input(value, width=(None, "%"), placeholder=placeholder)
    super(FieldInput, self).__init__(report, input, label, placeholder, icon, width, height, htmlCode, helper, profile)


class FieldRange(Field):

  def __init__(self, report, value, min, max, step, label, placeholder, icon, width, height, htmlCode, helper, options, profile):
    input = report.ui.inputs.d_range(value, min=min, max=max, step=step, width=(None, "%"), placeholder=placeholder, options=options)
    super(FieldRange, self).__init__(report, input, label, placeholder, icon, width, height, htmlCode, helper, profile)


class FieldCheckBox(Field):
  def __init__(self, report, value, label, icon, width, height, htmlCode, helper, profile):
    input = report.ui.inputs.checkbox(value, width=(None, "%"))
    super(FieldCheckBox, self).__init__(report, input, label, "", icon, width, height, htmlCode, helper, profile)


class FieldInteger(Field):

  def __init__(self, report, value, label, placeholder, icon, width, height, htmlCode, helper, profile):
    input = report.ui.inputs.d_int(value, width=(None, "%"), placeholder=placeholder)
    super(FieldInteger, self).__init__(report, input, label, placeholder, icon, width, height, htmlCode, helper, profile)


class FieldPassword(Field):
  def __init__(self, report, value, label, placeholder, icon, width, height, htmlCode, helper, profile):
    input = report.ui.inputs.password(value, width=(None, "%"), placeholder=placeholder)
    super(FieldPassword, self).__init__(report, input, label, placeholder, icon, width, height, htmlCode, helper, profile)


class FieldTextArea(Field):
  def __init__(self, report, value, label, placeholder, icon, width, height, htmlCode, helper, profile):
    input = report.ui.inputs.textarea(value, width=(100, "%"), placeholder=placeholder)
    super(FieldTextArea, self).__init__(report, input, label, placeholder, icon, width, height, htmlCode, helper, profile)


class FieldSelect(Field):
  def __init__(self, report, value, label, icon, width, height, htmlCode, helper, profile):
    input = report.ui.select(value, width=(100, "%"))
    super(FieldSelect, self).__init__(report, input, label, "", icon, width, height, htmlCode, helper, profile)


class Checkbox(Html.Html):
  name, category, callFnc = 'Checkbox', 'Inputs', 'checkbox'
  # _grpCls = CssGrpClsInput.CssClassInput

  def __init__(self, report, flag, label, group_name, width, height, htmlCode, filter, options, attrs, profile):
    super(Checkbox, self).__init__(report, {"value": flag, 'text': label}, htmlCode=htmlCode,
                                   css_attrs={"width": width, "height": height}, globalFilter=filter,
                                   profile=profile, options=options)
    self.set_attrs(attrs={"type": "checkbox"})
    self.set_attrs(attrs=attrs)
    self.css({"cursor": 'pointer', 'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '2px'})

  @property
  def _js__builder__(self):
    return '''htmlObj.checked = data.value; 
      if(data.text !== null){
        htmlObj.parentNode.insertBefore(document.createTextNode(data.text), htmlObj.nextSibling)};
      if(typeof options.css !== 'undefined'){for(var k in options.css){htmlObj.style[k] = options.css[k]}}'''

  def __str__(self):
    return '<input %(strAttr)s>' % {'strAttr': self.get_attrs(pyClassNames=self.style.get_classes())}


class Radio(Html.Html):
  name, category, callFnc = 'Radio', 'Inputs', 'radio'

  def __init__(self, report, flag, label, group_name, icon, width, height, htmlCode, helper, profile):
    super(Radio, self).__init__(report, {"value": flag, 'text': label}, htmlCode=htmlCode,
                                         css_attrs={"width": width, 'height': height}, profile=profile)
    self.add_input("", position="before", css={"width": 'none', "vertical-align": 'middle'})
    self.add_label(label, position="after", css={"display": 'inline-block', "width": "None", 'float': 'none'})
    self.input.inReport = False
    if flag:
      self.input.set_attrs({"checked": json.dumps(flag)})
    self.input.style.clear()
    if group_name is not None:
      self.input.set_attrs(name="name", value=group_name)
    self.input.set_attrs(attrs={"type": "radio"})
    self.input.css({"cursor": 'pointer', 'display': 'inline-block', 'vertical-align': 'middle', 'min-width': 'none'})
    self.css({'vertical-align': 'middle', 'text-align': "left"})
    self.add_icon(icon, position="after", css={"margin-left": '5px', 'color': self._report.theme.success[1]})

  @property
  def _js__builder__(self):
    return '''htmlObj.checked = data.value; 
      if(data.text !== null){
        htmlObj.parentNode.insertBefore(document.createTextNode(data.text), htmlObj.nextSibling)};
      if(typeof options.css !== 'undefined'){for(var k in options.css){htmlObj.style[k] = options.css[k]}}'''

  def __str__(self):
    return '<div %(strAttr)s></div>' % {'strAttr': self.get_attrs(pyClassNames=self.style.get_classes())}


class TextArea(Html.Html):
  name, category, callFnc = 'Text Area', 'Inputs', 'textArea'
  # _grpCls = CssGrpClsInput.CssClassTextArea

  def __init__(self, report, text, width, rows, placeholder, background_color, htmlCode, options, profile):
    super(TextArea, self).__init__(report, text, htmlCode=htmlCode, css_attrs={"width": width}, profile=profile)
    self.width, self.rows, self.backgroundColor = width, rows, background_color
    if not options.get("selectable", True):
      self.attr['onclick'] = "this.blur();this.select()"
      options["readOnly"] = True
      del options["selectable"]

    options.update({"rows": rows, "placeholder": placeholder or ""})
    self.set_attrs(attrs=options)

  def jsAppend(self, jsData='data', jsDataKey=None, isPyData=False, jsParse=False, jsStyles=None, jsFnc=None):
    return "%s.append(%s+ '\\r\\n')" % (self.jqId, self._jsData(jsData, jsDataKey, jsParse, isPyData, jsFnc))

  @property
  def _js__builder__(self):
    return 'htmlObj.innerHTML = data'

  def empty(self): return 'document.getElementById("%s").value = ""' % self.htmlId

  def __str__(self):
    return '<textarea %(strAttr)s></textarea>' % {"strAttr": self.get_attrs(pyClassNames=self.style.get_classes())}


class Search(Html.Html):
  name, category, callFnc = 'Search', 'Inputs', 'search'
  # _grpCls = GrpCls.CssGrpClassBase

  def __init__(self, report, text, placeholder, color, height, htmlCode, tooltip, extensible, profile):
    super(Search, self).__init__(report, "", htmlCode=htmlCode, css_attrs={"height": height}, profile=profile)
    self.color = self._report.theme.colors[-1] if color is None else color
    self.css({"display": "inline-block", "margin-bottom": '2px'})
    #
    if not extensible:
      self.attr["class"].add('CssSearch')
      self.css({"width": "100%"})
    else:
      self._report.style.cssCls('CssSearchExt')
    self.add_input(text).input.set_attrs({"placeholder": placeholder, "spellcheck": False})
    self.input.css({"text-align": 'left', 'padding-left': '%spx' % Defaults.LINE_HEIGHT})
    self.add_icon("fas fa-search").icon.attr['id'] = "%s_button" % self.htmlId
    self.icon.css({"margin": '6px 0 6px 5px', 'display': 'block', 'cursor': 'pointer', 'position': 'absolute'})
    if tooltip != '':
      self.tooltip(tooltip)

  @property
  def dom(self):
    if self._dom is None:
      self._dom = JsHtmlField.JsHtmlFields(self, report=self._report)
    return self._dom

  @property
  def _js__builder__(self):
    return '''htmlObj.find('input').val(data)'''

  def click(self, jsFncs, profile=False):
    return self.icon.click(jsFncs, profile)

  def enter(self, jsFncs, profile=False):
    """
    Add an javascript action when the key enter is pressed on the keyboard

    Example
    htmlObj.enter(" alert() ")

    :param jsFncs:
    :return: The python object itself
    """
    self.click(jsFncs)
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    return self.on("keydown", ["if (event.keyCode  == 13) {event.preventDefault(); %(jsFnc)s } " % {"jsFnc": JsUtils.jsConvertFncs(jsFncs, toStr=True)}], profile=profile)

  def __str__(self):
    return '<div %(attr)s></div>' % {"attr": self.get_attrs(pyClassNames=self.style.get_classes())}
