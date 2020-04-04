
import re
import json

from epyk.core.html import Html
from epyk.core.html.options import OptButton

from epyk.core.js.html import JsHtml
from epyk.core.js import JsUtils
from epyk.core.js.statements import JsIf
from epyk.core.js.objects import JsComponents

# The list of CSS classes
from epyk.core.css.styles import GrpClsButton
from epyk.core.css import Defaults_css


class Button(Html.Html):
  name, category, callFnc = 'Button', 'buttons', 'button'

  def __init__(self, report, text, icon, width, height, htmlCode, tooltip, profile, options):
    super(Button, self).__init__(report, text, code=htmlCode, profile=profile,
                                 css_attrs={"width": width, "height": height})
    if options is None:
      options = {}
    self.add_icon(icon)
    if icon is not None and not text:
      self.icon.style.css.margin_right = None
    self.__options = OptButton.OptionsButton(self, options)
    if tooltip is not None:
      self.tooltip(tooltip)
    self.set_attrs(name="data-count", value=0)

  @property
  def options(self):
    """
    Description:
    -----------
    Property to set all the possible object for a button

    :rtype: OptButton.OptionsButton
    """
    return self.__options

  @property
  def dom(self):
    """
    Description:
    -----------
    HTML Dom object

    :rtype: JsHtml.JsHtmlButton
    """
    if self._dom is None:
      self._dom = JsHtml.JsHtmlButton(self, report=self._report)
    return self._dom

  @property
  def _js__builder__(self):
    return "htmlObj.innerHTML = data"

  @property
  def style(self):
    """
    Description:
    -----------
    Property to the CSS Style of the component

    Usage:
    ------
    self.style.css.margin = "5px"

    :rtype: GrpClsButton.ClassButton
    """
    if self._styleObj is None:
      self._styleObj = GrpClsButton.ClassButton(self)
    return self._styleObj

  def disable(self, background_color=None, color=None):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param background_color: String.
    :param color: String.

    :return: The htmlObj to allow the chaining
    """
    css_pmts = {"cursor": "not-allowed"}
    if background_color is not None:
      css_pmts["background"] = background_color
    if color is not None:
      css_pmts["color"] = color
    self.css(css_pmts)
    self.attr['disabled'] = True
    return self

  def press(self, jsPressFncs=None, jsReleaseFncs=None, profile=False):
    """
    Description:
    -----------
    Special click event to keep in memory the state of the component

    Usage:
    ------

    Attributes:
    ----------
    :param jsPressFncs:
    :param jsReleaseFncs:
    :param profile:
    """
    str_fnc = ""
    if jsPressFncs is not None:
      if not isinstance(jsPressFncs, list):
        jsPressFncs = [jsPressFncs]
      if self.options.group is not None and not self.options.multiple:
        jsPressFncs.append(self.dom.release(by_name=True))
      jsPressFncs.append(self.dom.lock(not_allowed=jsReleaseFncs is None))
      str_fnc = "if(%s == 'pointer'){%s}" % (self.dom.css('cursor'), JsUtils.jsConvertFncs(jsPressFncs, toStr=True))
    if jsReleaseFncs is not None:
      if jsPressFncs is None:
        raise Exception("Press Event must be defined")

      if not isinstance(jsReleaseFncs, list):
        jsReleaseFncs = [jsReleaseFncs]
      jsReleaseFncs.append(self.dom.release())
      str_fnc = "%s else{%s}" % (str_fnc, JsUtils.jsConvertFncs(jsReleaseFncs, toStr=True))
    return self.on("click", str_fnc, profile)

  def color(self, color):
    """
    Description:
    -----------
    Change the color of the button background when the mouse is hover

    Usage:
    ------
    rptObj.ui.buttons.remove("remove").color("blue")

    Attributes:
    ----------
    :param color: String. the color of the component (text and borders)
    """
    self.style.css.border = "1px solid %s" % color
    self.set_attrs(name="onmouseover", value="this.style.backgroundColor='%s';this.style.color='white'" % color)
    self.set_attrs(name="onmouseout", value="this.style.backgroundColor=\'white\';this.style.color=\'%s\';" % color)
    return self

  def __str__(self):
    return '<button %s>%s</button>' % (self.get_attrs(pyClassNames=self.style.get_classes()), self.val)

  @staticmethod
  def matchMarkDown(val):
    return val.startswith("[button ")

  @classmethod
  def jsMarkDown(self, vals):
    return '[button url=""](%s)' % vals

  @classmethod
  def to_markdown(cls, val, regExpResult, rptObj):
    res = re.search('\[button url="(.*)"\]\((.*)\)', val)
    if res is not None:
      if rptObj is not None:
        getattr(rptObj, 'button')(res.group(2)).goTo(res.group(1))
      return ["rptObj.ui.%s.button('%s').goTo('%s')" % (cls.category, res.group(2), res.group(1))]

  # No export to this component as no interactivity is expected
  def to_word(self, document): pass
  def to_xls(self, workbook, worksheet, cursor): pass
  def to_ppt(self, workbook, worksheet, cursor): pass


class Checkbox(Html.Html):
  name, category, callFnc = 'Check Box', 'Buttons', 'checkbox'
  __reqCss, __reqJs = ['font-awesome', 'bootstrap'], ['font-awesome', 'bootstrap', 'jquery']

  def __init__(self, rptObj, records, title, color, width, height, align, htmlCode, filters, tooltip, icon, options, profile):
    if rptObj.http.get(htmlCode) is not None:
      selectedVals = set(rptObj.http[htmlCode].split(","))
      for rec in records:
        if rec["value"] in selectedVals:
          rec["checked"] = True
    super(Checkbox, self).__init__(rptObj, records, htmlCode=htmlCode, css_attrs={"width": width, "height": height},
                                   globalFilter=filters, profile=profile)
    # Add the component title
    self.add_title(title, options={'content_table': False})
    self.css({'text-align': align, 'color': 'inherit' if color is None else color, 'padding': '5px'})
    self._jsStyles = {"tooltip": tooltip, "icon": icon} # fas fa-circle fas fa-check
    self.selectAll = options.get("all_selected", False)

  def tooltip(self, value, location='top'):
    self._jsStyles['tooltip'] = value
    return self

  def jsDisable(self, jsData='data', jsDataKey=None, isPyData=False, jsParse=False, jsFnc=None, reset=True):
    jsData = self._jsData(jsData, jsDataKey, jsParse, isPyData, jsFnc)
    return '''
        const ldata = %(jsData)s;
        %(jqId)s.find('span').each(function(){
          var pItem = $(this).next(); 
          if(%(reset)s == true) {pItem.removeClass("%(disableCls)s")};
          if(($(this).find("i").attr("class") !== undefined) && (%(reset)s == true) && ($(this).find("i").attr("class").includes('fas fa-times'))){$(this).html('<div style="width:16px;display:inline-block">&nbsp;</div>') };
          if (ldata.indexOf(pItem.text()) > -1){
            var bcIndex = %(breadCrumVar)s['params']['%(htmlCode)s'].indexOf(pItem.text());
            if(bcIndex > -1) {delete %(breadCrumVar)s['params']['%(htmlCode)s'].splice(bcIndex, 1)};
            $(this).html('<i class="fas fa-times %(disableCls)s"></i>'); pItem.addClass("%(disableCls)s")}
        })''' % {'jsData': jsData, 'jqId': self.jqId, 'disableCls': self._report.style.cssName("CssLabelContainerDisabled"),
                 'breadCrumVar': self._report.jsGlobal.breadCrumVar, 'htmlCode': self.htmlId, 'reset': json.dumps(reset)}

  def jsAdd(self, jsData='data', jsDataKey=None, isPyData=False, jsParse=False, jsFnc=None, isUnique=False):
    """

    :example: c.jsAdd([{"value": 'A', "name": 'Test'}], isPyData=True, isUnique=True)
    """
    jsData = self._jsData(jsData, jsDataKey, jsParse, isPyData, jsFnc)
    return '''
      var existingCols = {};
      if (%(unique)s){%(jqId)s.find('span').each(function(){
        var pItem = $(this); 
        existingCols[pItem.data('content')] = true})};
      %(jsData)s.forEach(function(rec){
        if ((!%(unique)s) || (%(unique)s && (!(rec.value in existingCols))) ){
          var style = {'margin': 0, 'color': rec.color, 'display': 'block', 'position': 'relative', 'cursor': 'pointer'};
          var strCss = []; for (key in style) { strCss.push( key + ":" + style[key])};
          checkData = '&nbsp;';
          if (rec.checked){var checkData = '<i class="'+ %(jsStyles)s.icon + '" style="margin:2px"></i>'};
          var spanContent = '<span data-content="'+ rec.value + '" style="width:16px;display:inline-block;float:left;margin:0">'+ checkData +'</span><p style="margin:0" title="'+ rec.dsc + '">' + rec.name + '</p>';
          %(jqId)s.append($('<label style="' + strCss.join(";") + '">'+ spanContent +'</label>'))}
      })''' % {'jsData': jsData, 'jsStyles': json.dumps(self._jsStyles), 'jqId': self.jqId, 'unique': json.dumps(isUnique)}

  def jsRemove(self, jsData='data', jsDataKey=None, isPyData=False, jsParse=False, jsFnc=None):
    """

    :example: c.jsRemove([1, "A"], isPyData=True)
    """
    jsData = self._jsData(jsData, jsDataKey, jsParse, isPyData, jsFnc)
    return '''
      const ldata = %(jsData)s;
      if (ldata === true) {%(jqId)s.empty(); %(breadCrumVar)s['params']['%(htmlCode)s'] = []}
      else {
        %(jqId)s.find('span').each(function(){
          var pItem = $(this).next(); var bcIndex = %(breadCrumVar)s['params']['%(htmlCode)s'].indexOf(pItem.text());
          if(bcIndex > -1) {delete %(breadCrumVar)s['params']['%(htmlCode)s'].splice(bcIndex, 1)};
          if (ldata.indexOf($(this).data('content')) > -1){$(this).parent().remove()}
        })}''' % {'jsData': jsData, 'jqId': self.jqId, 'breadCrumVar': self._report.jsGlobal.breadCrumVar, 'htmlCode': self.htmlId}

  def jsItemState(self, jsData='data', jsDataKey=None, isPyData=False, jsParse=False, jsFnc=None):
    """

    :example: c.jsItemState(jsData=True, isPyData=True)
    :example: c.jsItemState(jsData=False, isPyData=True)
    """
    jsData = self._jsData(jsData, jsDataKey, jsParse, isPyData, jsFnc)
    return '''
      var ldata = %(jsData)s;
      %(jqId)s.find('span').each(function(){
        var itemCode = $(this).data('content');
        if(typeof ldata === "boolean"){
          if (ldata === true && $(this).find("i").attr("class") === undefined){$(this).trigger("click")}
          if (!ldata && $(this).find("i").attr("class") !== undefined){$(this).trigger("click")}}
        else if (ldata.indexOf(itemCode) > -1){if ($(this).find("i").attr("class") === undefined){$(this).trigger("click")}}
      }) ''' % {'jsData': jsData, 'jqId': self.jqId}

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, ''' htmlObj.empty() ;
      %(breadCrumVar)s['params'][htmlObj.attr('id')] = [];
      data.forEach(function(rec){
        if (rec.color == undefined) {rec.color = 'inherit'}
        var style = {'margin': 0, 'color': rec.color, 'display': 'block', 'position': 'relative', 'cursor': 'pointer'};
        if (rec.style != undefined) { for (key in rec.style) { style[key] = rec.style[key] }} ;
        if (rec.dsc == undefined) { rec.dsc = ''}
        if (rec.name == undefined) { rec.name = rec.value}
        var strCss = []; for (key in style) { strCss.push( key + ":" + style[key])};
        if (rec.checked == true) { 
          %(breadCrumVar)s['params'][htmlObj.attr('id')].push(rec.value );
          var spanContent = '<span data-content="' + rec.value + '" style="display:inline-block;float:left;margin:0"><i class="'+ jsStyles.icon + '" style="margin:2px"></i></span><p style="margin:0;padding:0" title="'+ rec.dsc + '">' + rec.name + '</p>'; }
        else {var spanContent = '<span data-content="'+ rec.value + '" style="width:16px;display:inline-block;float:left;margin:0">&nbsp;</span><p style="margin:0" title="'+ rec.dsc + '">' + rec.name + '</p>';}     
        htmlObj.append($('<label style="' + strCss.join(";") + '">'+ spanContent +'</label>'))}); htmlObj.find("p").tooltip(); 
        if (jsStyles.tooltip != ""){ 
          var tip = $('<i class="fas fa-info-circle" style="right:0" title="'+ jsStyles.tooltip +'"></i>') ;
          tip.tooltip(); htmlObj.append($("<div style='width:100%%;text-align:right'></div>").append(tip) )}
      ''' % {'breadCrumVar': self._report.jsGlobal.breadCrumVar}, 'Javascript Object builder')

  def jsEvents(self):
    if hasattr(self, 'jsFncFrag'):
      for eventKey, fnc in self.jsFncFrag.items():
        if self.htmlCode is not None:
          fnc.insert(0, self.jsAddUrlParam(self.htmlCode, self.val, isPyData=False))
        self._report.jsOnLoadEvtsFnc.add('''
          $( document ).on('%(eventKey)s', '#%(htmlId)s label', function(event) {
            if(($(this).find("i").attr("class") !== undefined) && ($(this).find("i").attr("class").includes('fas fa-times'))) {return {}};
            var useAsync = false; var isChecked = false; var htmlContent = $(this).find('span').find('i').length; 
            if (htmlContent == 0) {$(this).find('span').html('<i class="%(icon)s" style="padding:2px"></i>'); isChecked = true} else {$(this).find('span').html('<div style="width:16px;display:inline-block">&nbsp;</div>')}
            var data = %(data)s ; var returnVal = undefined;
            %(jsInfo)s; %(jsFnc)s; 
            if (!useAsync) {
              var body_loading_count = parseInt($('#body_loading span').text()); $('#body_loading span').html(body_loading_count - 1);
              if ($('#body_loading span').html() == '0') {$('#body_loading').remove()} }
            if (returnVal != undefined) {return returnVal}
          })''' % {'htmlId': self.htmlId, 'eventKey': eventKey, 'data': self.jsQueryData,
                   'jsFnc': ";".join([f for f in fnc if f is not None]), 'icon': self._jsStyles['icon'],
                   'jsInfo': self._report.jsInfo('process(es) running', 'body_loading')})

  def __str__(self):
    if self.selectAll:
      self.addGlobalFnc("CheckBoxSelectAll(event, srcObj, htmlId)", '''
        $(srcObj).find('div').toggleClass("fa-check");
        var ldata = $(srcObj).find('div').hasClass("fa-check");
        $('#'+ htmlId).find('span').each(function(){
          var itemCode = $(this).data('content');
          if(typeof ldata === "boolean"){
            if (ldata === true && $(this).find("i").attr("class") === undefined){$(this).trigger("click")}
            if (!ldata && $(this).find("i").attr("class") !== undefined){$(this).trigger("click")}}
          else if (ldata.indexOf(itemCode) > -1){if ($(this).find("i").attr("class") === undefined){$(this).trigger("click")}}
        })''')
      selectTag = '''
        <div onclick='event.stopPropagation();CheckBoxSelectAll(event, this, "%(htmlId)s");' style='vertical-align:middle;white-space:nowrap;margin-bottom:5px;cursor:pointer;padding:0'>
          <div style='box-sizing:border-box;margin:0;padding:0;border:1px solid %(color)s;font-size:10px;width:11px;height:11px;display:inline-block;color:%(color)s' class="fas">&nbsp;</div>
          <label style='cursor:inherit;margin:0;padding:0;font-style:italic;color:%(color)s;white-space:nowrap'>Select All</label>
        </div>''' % {"color": self._report.theme.colors[5], 'htmlId': self.htmlId}

    return '<div %(strAttr)s><div name="checks"></div></div>' % {'strAttr': self.get_attrs(pyClassNames=self.style.get_classes())}

  def to_word(self, document):
    from docx.shared import RGBColor

    selections = self._report.http.get(self.htmlCode).split(',')
    for rec in self.vals:
      p = document.add_paragraph(style='ListBullet')
      runner = p.add_run(rec['value'])
      if rec['value'] in selections:
        runner.font.color.rgb = RGBColor(0x42, 0x24, 0xE9)

  def to_xls(self, workbook, worksheet, cursor):
    selections = self._report.http.get(self.htmlCode).split(',')
    cellTitle = self.title if self.title != '' else 'Checkbox:'
    cell_format = workbook.add_format({'bold': True})
    worksheet.write(cursor['row'], 0, cellTitle, cell_format)
    cursor['row'] += 1
    for rec in self.vals:
      cell_format = workbook.add_format({})
      if rec['value'] in selections:
        cell_format = workbook.add_format({'bold': True, 'font_color': self._report.theme.colors[5]})
      worksheet.write(cursor['row'], 0, rec['value'], cell_format)
      cursor['row'] += 1
    cursor['row'] += 1

  @staticmethod
  def matchMarkDown(val):
    return re.match("\+\+\+(.*)", val) or re.match("\-\-\-(.*)", val)

  @classmethod
  def convertMarkDown(cls, val, regExpResult, report):
    param = True if val.startswith("+") else False
    if report is not None:
      getattr(report, cls.callFnc)(param, regExpResult.group(1))
    return ["report.%s(%s, %s)" % (cls.callFnc, param, regExpResult.group(1))]

  @classmethod
  def jsMarkDown(self, vals):
    if vals:
      return "+++" % self.label

    return "---%s" % self.label


class CheckButton(Html.Html):
  name, category, callFnc = 'Check Button', 'Button', 'check'

  def __init__(self, report, flag, tooltip, width, height, icon, label, htmlCode, options, profile):
    super(CheckButton, self).__init__(report, 'Y' if flag else 'N', htmlCode=htmlCode,
                                      css_attrs={"width": width, "height": height}, profile=profile)
    self.input = report.ui.images.icon("fas fa-check" if flag else "fas fa-times").css({"width": "12px"})
    if flag:
      self.input.style.css.color = self._report.theme.success[1]
    else:
      self.input.style.css.color = self._report.theme.danger[1]
    self.input.style.middle()
    self.input.inReport = False
    self.isDisable = options.get("disable", False)
    self.add_label(label, {"width": "none", "float": "none"}, position="after")
    self.add_icon(icon, {"float": 'none'}, position="after")
    self.css({'display': 'inline-block', 'margin-right': '10px'})
    if tooltip is not None:
      self.tooltip(tooltip)

  @property
  def _js__builder__(self):
    return ''' htmlObj.empty();
      if (data === true || data == 'Y'){
        htmlObj.append('<i class="fas fa-check" style="color:%(green)s;margin-bottom:2px;margin-left:2px"></i>');
        htmlObj.parent().data('isChecked', true)} 
      else {
        htmlObj.append('<i class="fas fa-times" style="font-size:14px;margin-top:2px;margin-left:5px;color:%(red)s"></i>');
        htmlObj.parent().data('isChecked', false)
      }''' % {'green': self._report.theme.success[1], 'red': self._report.theme.danger[1]}

  @property
  def style(self):
    """
    Description:
    ------------
    Property to the CSS Style of the component

    :rtype: GrpClsButton.ClassButtonCheckBox
    """
    if self._styleObj is None:
      self._styleObj = GrpClsButton.ClassButtonCheckBox(self)
    return self._styleObj

  def click(self, jsFncsTrue, jsFncFalse=None, withColors=True, profile=False):
    """
    Description:
    ------------
    Click even on the checkbox item

    Usage:
    ------
    ch = rptObj.ui.buttons.check(label="Label")
    ch.click(rptObj.js.alert("true"), rptObj.js.alert("false"))

    Attributes:
    ----------
    :param jsFncsTrue: Js function or a list of JsFunction to be triggered when checked
    :param jsFncFalse: Optional. Js function or a list of JsFunction to be triggered when unchecked

    :return: The htmlObl to allow the chaining
    """
    if self.label is not None and hasattr(self.label, 'style'):
      self.label.style.css.cursor = 'pointer'
    self.style.css.cursor = "pointer"
    if not isinstance(jsFncsTrue, list):
      jsFncsTrue = [jsFncsTrue]
    if jsFncFalse is None:
      jsFncFalse = []
    elif not isinstance(jsFncFalse, list):
      jsFncFalse = [jsFncFalse]
    if withColors:
      jsFncsTrue.append(self.input.dom.css({"color": self._report.theme.success[1]}).r)
      jsFncFalse.append(self.input.dom.css({"color": self._report.theme.danger[1]}).r)
    jsFncs = [
      self.input.dom.switchClass("fa-check", "fa-times"),
      JsIf.JsIf(self.input.dom.hasClass("fa-check"), jsFncsTrue).else_(
        jsFncFalse)]
    return super(CheckButton, self).click(jsFncs, profile)

  def __str__(self):
    return '''<div %s>%s</div>''' % (self.get_attrs(pyClassNames=self.style.get_classes()), self.input.html())


class IconEdit(Html.Html):
  name, category, callFnc = 'Icon', 'Icons', 'iconEdit'
  cssCls = ["fa-layers", "fa-fw"]

  def __init__(self, report, position, icon, text, tooltip, width, height, htmlCode, profile):
    super(IconEdit, self).__init__(report, '', code=htmlCode, profile=profile,
                                   css_attrs={"width": width, 'height': height, 'float': 'left' if position is None else position})
    if tooltip is not None:
      self.tooltip(tooltip)
    # Add the internal components icons and helper
    self.add_span(text, css={"float": 'right'})
    self.add_icon(icon, {"color": self._report.theme.success[1], "margin": "2px", 'font-size': Defaults_css.font()})
    self.css({"margin": "5px 0", 'cursor': 'pointer'})

  def __str__(self):
    return "<span %s></span>" % (self.get_attrs(pyClassNames=self.style.get_classes()))


class Buttons(Html.Html):

  def __init__(self, report, data, color, width, height, htmlCode, helper, options, profile):
    super(Buttons, self).__init__(report, data, code=htmlCode, css_attrs={"width": width, "height": height, 'color': color},
                                  profile=profile)
    self.row = []
    for b in data:
      bt = report.ui.button(b, options={"group": "group_%s" % self.htmlId}).css({"margin-right": '5px'})
      bt.css(options.get("button_css", {}))
      bt.inReport = False
      self.row.append(bt)

  def __getitem__(self, i):
    """
    Description:
    ------------
    Get a button in this component

    Attributes:
    ----------
    :param i: Integer. The button index
    :rtype: Button
    """
    return self.row[i]

  def __str__(self):
    str_div = "".join([v.html() if hasattr(v, 'html') else v for v in self.row])
    return '<div %s>%s</div>' % (self.get_attrs(pyClassNames=self.style.get_classes()), str_div)


class ButtonMenuItem(object):

  def __init__(self, report, selector, parent):
    self._report, self._selector = report, selector
    self._src, self._js, self._events = parent, None, []

  @property
  def js(self):
    """
    Description:
    -----------
    Javascript module of the items in the menu

    Attributes:
    ----------
    :return: A Javascript Dom object

    :rtype: JsQueryUi.Autocomplete
    """
    if self._js is None:
      self._js = JsComponents.Menu(self._src, varName=self._selector, report=self._report)
    return self._js

  def on(self, event, jsFncs, profile=False):
    """
    Description:
    -----------
    Javascript generic events of the items in the menu

    Attributes:
    ----------
    :param event: String. The JavaScript event
    :param jsFncs: List: The Javascript fragments
    :param profile: Boolean.
    """
    self._events.append("%s.addEventListener('%s', function (event) { %s })" % (self._selector, event, JsUtils.jsConvertFncs(jsFncs, toStr=True)))
    return self._src

  def click(self, jsFncs):
    """
    Description:
    -----------
    Javascript click events of the items in the menu

    :param jsFncs: List: The Javascript fragments
    """
    self._events.append("%s.addEventListener('click', function (event) { %s })" % (self._selector, JsUtils.jsConvertFncs(jsFncs, toStr=True)))
    return self._src


class ButtonMenu(Html.Html):
  name, category, callFnc = 'ButtonMenu', 'buttons', 'menu'

  def __init__(self, report, record, text, icon, width, height, htmlCode, tooltip, profile, options):
    super(ButtonMenu, self).__init__(report, record, code=htmlCode, profile=profile, css_attrs={"width": width, "height": height})
    self.button = report.ui.button(text, icon, width, height, htmlCode, tooltip, profile, options)
    self.__items = {}
    self.button.inReport = False
    self.set_attrs(name="data-count", value=0)
    self.style.css.position = "relative"
    self.style.css.display = "inline-block"
    self.container = report.ui.div()
    self.container.inReport = False
    self.container.attr['class'].add("dropdown-content")
    self.container.style.css.display = "none"
    self.container.style.css.position = "absolute"
    self.container.style.css.z_index = 5
    self._jsStyles = {"padding": '5px', 'cursor': 'pointer', 'display': 'block'}

  def __getitem__(self, i):
    if i not in self.__items:
      self.__items[i] = ButtonMenuItem(self._report, "document.getElementById('%s').querySelectorAll('a')[%s]" % (self.htmlId, i), self)
    return self.__items[i]

  @property
  def _js__builder__(self):
    return '''
      var panel = htmlObj.querySelector("div");
      data.forEach(function(rec){
        var href = document.createElement("a"); href.innerHTML = rec;
        Object.keys(options).forEach(function(key){href.style[key] = options[key]});
        panel.appendChild(href)})'''

  @property
  def style(self):
    """
    Description:
    -----------
    Property to the CSS Style of the component

    Usage:
    ------
    self.style.css.margin = "5px"

    :rtype: GrpClsButton.ClassButton
    """
    if self._styleObj is None:
      self._styleObj = GrpClsButton.ClassButtonMenu(self)
    return self._styleObj

  def __str__(self):
    self._report._props.setdefault('js', {}).setdefault("builders", []).append(self.refresh())
    events = []
    for comp in self.__items.values():
      events.extend(comp._events)
    self.onReady(events)
    return '<div %s>%s%s</div>' % (self.get_attrs(pyClassNames=self.style.get_classes()), self.button.html(), self.container.html())
