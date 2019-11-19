"""
Wrapper to the different HTML input components
"""

import datetime

from epyk.core.html import Html

#
from epyk.core.js import JsUtils

# The list of CSS classes
from epyk.core.css.groups import CssGrpClsInput


class Output(Html.Html):
  name, category, callFnc = 'Output', 'Inputs', '_output'
  builder_name = False

  def __str__(self):
    return '<output %(strAttr)s>%(val)s</output>' % {'strAttr': self.get_attrs(pyClassNames=self.pyStyle), 'val': self.val}


class Input(Html.Html):
  name, category, callFnc = 'Input', 'Inputs', 'input'
  _grpCls = CssGrpClsInput.CssClassInput

  def __init__(self, report, text, placeholder, size, width, height, htmlCode, filter, options, attrs, profile):
    super(Input, self).__init__(report, text, htmlCode=htmlCode, width=width[0], widthUnit=width[1], height=height[0],
                                heightUnit=height[1], globalFilter=filter, profile=profile, options=options)
    self.set_attrs(attrs={"placeholder": placeholder, "type": "text", "value": text, "spellcheck": False})
    self.set_attrs(attrs=attrs)
    self.css({"font-size": "%s%s" % (size[0], size[1])})

  @property
  def _js__builder__(self):
    return '''htmlObj.value = data; 
      if(typeof options.css !== 'undefined'){for(var k in options.css){htmlObj.style[k] = options.css[k]}}'''

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

    :return:
    """
    self._report.js.addOnLoad(['%s.autocomplete({"source": %s})' % (self.dom.jquery.varId, source)])
    return self

  def enter(self, jsFncs, profile=False):
    """
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

  def __str__(self):
    return '<input %(strAttr)s />' % {'strAttr': self.get_attrs(pyClassNames=self.pyStyle)}


class InputTime(Input):
  name, callFnc = 'Input Time', 'input'
  __reqCss, __reqJs = ['timepicker'], ['timepicker']
  _grpCls = CssGrpClsInput.CssClassTimePicker

  def __init__(self, report, text, placeholder, size, width, height, htmlCode, filter, options, attrs, profile):
    if text is None:
      text = {"time": str(datetime.datetime.now()).split(" ")[1].split(".")[0]}
    elif isinstance(text, str):
      text = {"time": text}
    if 'options' not in text:
      text['options'] = {'timeFormat': 'HH:mm:ss'}
      text['options']["_change"] = []
    super(InputTime, self).__init__(report, text, placeholder, size, width, height, htmlCode, filter, options, attrs, profile)

  @property
  def _js__builder__(self):
    return '''
      if (typeof data == "string"){jQuery(htmlObj).timepicker('setTime', data)
      } else {
        if (data.time == ''){data.time = new Date()};
        if (data.options._change.length > 0) {data.options.change = function(time){
            let data = {event_val: time.getHours() +':'+ time.getMinutes() +':'+ time.getSeconds(), event_code: htmlId}; 
            eval(data.options._change.join(";"))}};
        jQuery(htmlObj).timepicker(data.options); jQuery(htmlObj).timepicker('setTime', data.time)}'''


class InputDate(Input):
  __reqCss, __reqJs = ['jqueryui'], ['jqueryui']
  name, callFnc = 'Input Time', 'input'
  cssCls = ["datepicker"]
  _grpCls = CssGrpClsInput.CssClassDatePicker

  def __init__(self, report, records, placeholder, size, width, height, htmlCode, filter, options, attrs, profile):
    super(InputDate, self).__init__(report, records, placeholder, size, width, height, htmlCode, filter, options, attrs, profile)

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


class InputInteger(Input):
  _grpCls = CssGrpClsInput.CssClassInputInteger
  name, callFnc = 'Input Number', 'input'

  def quantity(self):
    factors, strFcts = {'K': 1000, 'M': 1000000, 'B': 1000000000}, []
    for f, val in factors.items():
      strFcts.append("if(event.key.toUpperCase() == '%s'){$(this).find('input').val($(this).find('input').val() * %s)}" % (f, val))
    self.on('keydown', ";".join(strFcts))
    return self


class InputRange(Input):
  name, callFnc = 'Input Range', 'input'
  _grpCls = CssGrpClsInput.CssClassInputRange

  def __init__(self, report, text, min, max, step, placeholder, size, width, height, htmlCode, filter, options, attrs, profile):
    super(InputRange, self).__init__(report, text, placeholder, size, width, height, htmlCode, filter, options,
                                     attrs, profile)
    self.output = self._report.ui.inputs._output(text)
    self.set_attrs(attrs={"min": min, "max": max, "step": step, "oninput": "%s.value=this.value" % self.output.htmlId})


class Checkbox(Html.Html):
  name, category, callFnc = 'Checkbox', 'Inputs', 'checkbox'
  _grpCls = CssGrpClsInput.CssClassInput

  def __init__(self, report, flag, label, group_name, size, width, height, htmlCode, filter, options, attrs, profile):
    super(Checkbox, self).__init__(report, {"value": flag, 'text': label}, htmlCode=htmlCode, width=width[0],
                                   widthUnit=width[1], height=height[0], heightUnit=height[1], globalFilter=filter,
                                   profile=profile, options=options)
    self.set_attrs(attrs={"type": "checkbox"})
    self.set_attrs(attrs=attrs)
    self.css({"font-size": "%s%s" % (size[0], size[1]), "cursor": 'pointer', 'display': 'inline-block',
              'vertical-align': 'middle', 'margin-left': '2px'})

  @property
  def _js__builder__(self):
    return '''htmlObj.checked = data.value; 
      if(data.text !== null){
        htmlObj.parentNode.insertBefore(document.createTextNode(data.text), htmlObj.nextSibling)};
      if(typeof options.css !== 'undefined'){for(var k in options.css){htmlObj.style[k] = options.css[k]}}'''

  def __str__(self):
    return '<input %(strAttr)s>' % {'strAttr': self.get_attrs(pyClassNames=self.defined)}


class Radio(Html.Html):
  name, category, callFnc = 'Radio', 'Inputs', 'radio'
  _grpCls = CssGrpClsInput.CssClassInput

  def __init__(self, report, flag, label, group_name, size, width, height, htmlCode, filter, options, attrs, profile):
    super(Radio, self).__init__(report, {"value": flag, 'text': label}, htmlCode=htmlCode, width=width[0], widthUnit=width[1],
                                height=height[0], heightUnit=height[1], globalFilter=filter, profile=profile, options=options)
    if group_name is not None:
      self.set_attrs(name="name", value=group_name)
    self.set_attrs(attrs={"type": "radio"})
    self.set_attrs(attrs=attrs)
    self.css({"font-size": "%s%s" % (size[0], size[1]), "cursor": 'pointer', 'display': 'inline-block',
              'vertical-align': 'middle', 'margin-right': '2px'})

  @property
  def _js__builder__(self):
    return '''htmlObj.checked = data.value; 
      if(data.text !== null){
        htmlObj.parentNode.insertBefore(document.createTextNode(data.text), htmlObj.nextSibling)};
      if(typeof options.css !== 'undefined'){for(var k in options.css){htmlObj.style[k] = options.css[k]}}'''

  def __str__(self):
    return '<input %(strAttr)s>' % {'strAttr': self.get_attrs(pyClassNames=self.defined)}


class TextArea(Html.Html):
  name, category, callFnc = 'Text Area', 'Inputs', 'textArea'
  _grpCls = CssGrpClsInput.CssClassTextArea

  def __init__(self, report, text, width, rows, placeholder, size, background_color, htmlCode, options, profile):
    super(TextArea, self).__init__(report, text, htmlCode=htmlCode, width=width[0], widthUnit=width[1], profile=profile)
    self.width, self.rows, self.backgroundColor = width, rows, background_color
    self.css({"font-size": "%s%s" % (report.style.defaults.font.size, report.style.defaults.font.unit),
              "font-family": report.style.defaults.font.family})
    if options.get("selectable", False):
      self.attr['onclick'] = "this.blur();this.select()"
      options["readOnly"] = True
      del options["selectable"]

    options.update({"rows": rows, "placeholder": placeholder or ""})
    self.set_attrs(attrs=options)
    self.css({"font-size": "%s%s" % (size[0], size[1])})

  def jsAppend(self, jsData='data', jsDataKey=None, isPyData=False, jsParse=False, jsStyles=None, jsFnc=None):
    return "%s.append(%s+ '\\r\\n')" % (self.jqId, self._jsData(jsData, jsDataKey, jsParse, isPyData, jsFnc))

  @property
  def _js__builder__(self):
    return 'htmlObj.innerHTML = data'

  def empty(self): return 'document.getElementById("%s").value = ""' % self.htmlId

  def __str__(self):
    return '<textarea %(strAttr)s></textarea>' % {"strAttr": self.get_attrs(pyClassNames=self.defined)}


class Search(Html.Html):
  name, category, callFnc = 'Search', 'Inputs', 'search'
  _grpCls = CssGrpClsInput.CssClassInputSearch

  def __init__(self, report, text, placeholder, color, size, height, htmlCode, tooltip, extensible, profile):
    self.placeholder, self.extensible = placeholder, extensible
    self.size = "%s%s" % (size[0], size[1])
    super(Search, self).__init__(report, text, htmlCode=htmlCode, height=height[0], heightUnit=height[1], profile=profile)
    self.color = self.getColor('colors', -1) if color is None else color
    self.css({"width": "100%", "display": "block", "margin-bottom": '2px'})
    if self.htmlCode is not None:
      self._report.htmlCodes[self.htmlCode] = self
      self.change('') # Add the onchange method to update the breadcrumb
      if self.htmlCode in self._report.http:
        self.vals = self._report.http[self.htmlCode]
    if tooltip != '':
      self.tooltip(tooltip)

  @property
  def val(self): return '$("#%s input").val()' % self.htmlId

  @property
  def jsQueryData(self): return "{event_val: $(this).parent().find('input').val()}"

  def onDocumentLoadFnc(self): self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, "htmlObj.find('input').val(data);", 'Javascript Object builder')

  @property
  def eventId(self): return '$("#%s input")' % self.htmlId

  def click(self, jsFncs):
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    self._report.jsOnLoadEvtsFnc.add('''
      $('#%(htmlId)s_button').on('click', function(event) {
        var data = %(data)s; %(jsFncs)s})''' % {'htmlId': self.htmlId, 'jsFncs': ";".join(jsFncs), 'data': self.jsQueryData})
    return self

  def enter(self, jsFncs):
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
    self.keydown(["if (event.keyCode  == 13) {var data = %(data)s; event.preventDefault(); %(jsFnc)s } " % {"jsFnc": ";".join(jsFncs), 'data': self.jsQueryData}])
    return self

  def __str__(self):
    if not self.extensible:
      self._report.style.cssCls('CssSearch')
      pyCssCls = self._report.style.cssName('CssSearch')
    else:
      self._report.style.cssCls('CssSearchExt')
      pyCssCls = self._report.style.cssName('CssSearchExt')
    return '''
      <div %(attr)s>
          <input class="%(pyCssCls)s" type="text" name="search" placeholder="%(placeholder)s" spellcheck="false">
          <span id="%(htmlId)s_button" class="fas fa-search"></span>
      </div>''' % {"attr": self.get_attrs(pyClassNames=self.__pyStyle), "pyCssCls": pyCssCls, "placeholder": self.placeholder,
                   'htmlId': self.htmlId}


