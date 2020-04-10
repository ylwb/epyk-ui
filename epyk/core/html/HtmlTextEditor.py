
import datetime

from epyk.core.js import JsUtils
from epyk.core.js.html import JsHtmlEditor
from epyk.core.js.packages import JsCodeMirror
from epyk.core.html import Html

from epyk.core.html.options import OptCodeMirror
from epyk.core.html.options import OptText


class Console(Html.Html):
  name, category = 'Console', 'Rich'

  def __init__(self, report, data, width, height, htmlCode, helper, options, profile):
    super(Console, self).__init__(report, data, code=htmlCode, css_attrs={"width": width, "height": height}, profile=profile)
    self.css({"overflow": 'auto', 'box-sizing': 'border-box'})
    self.__options = OptText.OptionsConsole(self, options)

  @property
  def dom(self):
    """
    Description:
    ------------
    Javascript Functions

    Return all the Javascript functions defined for an HTML Component.
    Those functions will use plain javascript by default.

    :return: A Javascript Dom object

    :rtype: JsHtmlEditor.Console
    """
    if self._dom is None:
      self._dom = JsHtmlEditor.Console(self, report=self._report)
    return self._dom

  @property
  def options(self):
    """
    Description:
    ------------
    Property to set all the possible object for a button

    :rtype: OptText.OptionsConsole
    """
    return self.__options

  @property
  def _js__builder__(self):
    return ''' 
      if(options.showdown){var converter = new showdown.Converter(options.showdown);
        let frag = document.createRange().createContextualFragment(converter.makeHtml(data)); 
        frag.firstChild.style.display = 'inline-block';frag.firstChild.style.margin = 0 ;  
        data = frag.firstChild.outerHTML} 
      htmlObj.innerHTML = data +'<br/>' '''

  def __str__(self):
    self._report._props.setdefault('js', {}).setdefault("builders", []).append(self.refresh())
    return "<div %s></div>%s" % (self.get_attrs(pyClassNames=self.style.get_classes()), self.helper)


class Editor(Html.Html):
  name, category, callFnc = 'Code Editor', 'Text', 'editor'
  __reqCss, __reqJs = ['codemirror', 'font-awesome'], ['codemirror', 'font-awesome']

  def __init__(self, report, vals, language, width, height, htmlCode, options, profile):
    super(Editor, self).__init__(report, vals, code=htmlCode, css_attrs={"width": width, "height": height,
            'box-sizing': 'border-box', 'margin': '5px 0'}, profile=profile)
    self.textarea = self._report.ui.texts.code(vals, height=height, language=language, options=options)
    self.textarea.inReport = False
    self.actions = []

  @property
  def dom(self):
    """
    Description:
    ------------
    Javascript Functions

    Return all the Javascript functions defined for an HTML Component.
    Those functions will use plain javascript by default.

    :return: A Javascript Dom object

    :rtype: JsHtmlEditor.Editor
    """
    if self._dom is None:
      self._dom = JsHtmlEditor.Editor(self, report=self._report)
    return self._dom

  def action(self, icon, jsFncs, tooltip=None):
    """
    Description:
    ------------
    Add a bespoke action to the action panel

    Attributes:
    ----------
    :param icon: String. The font awesome icon
    :param jsFncs: Array. The Javascript functions
    :param tooltip: String. Text to be displayed when mouse is hover

    :return:
    """
    icon_button = self._report.ui.icon(icon, tooltip=tooltip).css({"margin-right": '5px'}).click(jsFncs)
    self.actions.append((icon, icon_button))
    icon_button.inReport = False
    return self

  def toggle(self, jsFncs, icons=("fas fa-eye", "far fa-eye-slash"), tooltip=None):
    """
    Description:
    ------------
    Add an event action to the console object.

    Attributes:
    ----------
    :param icon: String. The font awesome icon
    :param jsFncs: Array. The Javascript functions
    :param tooltip: String. Text to be displayed when mouse is hover

    :return:
    """
    icon_button = self._report.ui.icon(icons[0], tooltip=tooltip).css({"margin-right": '5px'})
    jsFncs.append(self.textarea.dom.toggle())
    jsFncs.append(icon_button.dom.switchClass(icons[0], icons[1]).r)
    icon_button.click(jsFncs)
    icon_button.inReport = False
    self.actions.append((icons[0], icon_button))
    return self

  def copy(self, jsFncs, icon="far fa-clipboard", tooltip=None):
    """
    Description:
    ------------
    Copy the content of the editor component to the clipboard.

    Attributes:
    ----------
    :param icon: String. The font awesome icon
    :param jsFncs: Array. The Javascript functions
    :param tooltip: String. Text to be displayed when mouse is hover
    """
    jsFncs.append(self.textarea.dom.select())
    jsFncs.append('document.execCommand("copy")')
    return self.action(icon, jsFncs, tooltip)

  def run(self, jsFncs, icon="fas fa-play", tooltip=None):
    """
    Description:
    ------------
    Emtpy run button.
    This function will just add the icon on the actions panel.

    Attributes:
    ----------
    :param icon: String. The font awesome icon
    :param jsFncs: Array. The Javascript functions
    :param tooltip: String. Text to be displayed when mouse is hover
    """
    return self.action(icon, jsFncs, tooltip)

  def save(self, jsFncs, icon="fas fa-save", tooltip=None):
    """
    Description:
    ------------
    Emtpy save button.
    This function will just add the icon on the actions panel.

    Attributes:
    ----------
    :param icon: String. The font awesome icon
    :param jsFncs: Array. The Javascript functions
    :param tooltip: String. Text to be displayed when mouse is hover
    """
    return self.action(icon, jsFncs, tooltip)

  def clear(self, jsFncs, icon="fas fa-times-circle", tooltip=None):
    """
    Description:
    ------------
    Add an event action to the console object.

    Attributes:
    ----------
    :param icon: String. The font awesome icon
    :param jsFncs: Array. The Javascript functions
    :param tooltip: String. Text to be displayed when mouse is hover
    """
    jsFncs.append(self.textarea.dom.clear())
    return self.action(icon, jsFncs, tooltip)

  def __str__(self):
    actions = "".join([b.html() for _, b in self.actions])
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return '''
        <div %(attr)s>%(actions)s
          <span style="display:inline-block;float:right;margin-right:5px;font-style:italic">%(timestamp)s</span>
        </div> 
        %(textarea)s''' % {'attr': self.get_attrs(pyClassNames=self.style.get_classes()), 'timestamp': timestamp,
                           "textarea": self.textarea.html(), 'htmlId': self.htmlId, 'actions': actions}


class Cell(Html.Html):
  name, category, callFnc = 'Python Cell Runner', 'Text', 'pytestcell'
  __reqCss, __reqJs = ['codemirror'], ['codemirror']

  def __init__(self, report, vals, language, width, height, htmlCode, options, profile):
    super(Cell, self).__init__(report, vals, code=htmlCode, css_attrs={"width": width, "height": height}, profile=profile)
    self.textarea = self._report.ui.texts.code(vals, height=height, language=language, options=options)
    self.textarea.inReport = False
    self.textarea.style.add_classes.input.textarea()
    self._jsRun, self._jsSave = '', ''
    self.css({'padding': '10px', "min-height": "30px", 'box-sizing': 'border-box', 'display': 'inline-block'})
    self.actions = []

  def action(self, icon, jsFncs, tooltip=None):
    """
    Description:
    ------------
    Add a bespoke action to the action panel

    Attributes:
    ----------
    :param icon: String. The font awesome icon
    :param jsFncs: Array. The Javascript functions
    :param tooltip: String. Text to be displayed when mouse is hover

    :return:
    """
    icon_button = self._report.ui.icon(icon, tooltip=tooltip).css({"margin-right": '5px'}).click(jsFncs)
    self.actions.append((icon, icon_button))
    icon_button.inReport = False

  def run(self, jsFncs, icon="fas fa-play", tooltip=None):
    """
    Description:
    ------------
    Emtpy run button.
    This function will just add the icon on the actions panel.

    Attributes:
    ----------
    :param icon: String. The font awesome icon
    :param jsFncs: Array. The Javascript functions
    :param tooltip: String. Text to be displayed when mouse is hover
    """
    jsFncs.append(self.dom.querySelector("span").innerHTML(1, append=True, valType=int))
    return self.action(icon, jsFncs, tooltip)

  def save(self, jsFncs, icon="fas fa-save", tooltip=None):
    """
    Description:
    ------------
    Emtpy save button.
    This function will just add the icon on the actions panel.

    Attributes:
    ----------
    :param icon: String. The font awesome icon
    :param jsFncs: Array. The Javascript functions
    :param tooltip: String. Text to be displayed when mouse is hover
    """
    return self.action(icon, jsFncs, tooltip)

  def __str__(self):
    actions = "".join([b.html() for _, b in self.actions])
    return '''
      <div %(attrs)s>
          <div style="padding:10px 5px;float:left;width:50px;height:100%%;vertical-align:middle">
            In [ <span data=count=0 style="display:inline-block;margin-bottom:5px">0</span> ]<br/>%(actions)s
          </div>
          %(textarea)s
      </div>''' % {'attrs': self.get_attrs(pyClassNames=self.style.get_classes()), 'actions': actions, "textarea": self.textarea.html()}


class Code(Html.Html):
  name, category, callFnc = 'Code', 'Text', 'code'
  __reqCss, __reqJs = ['codemirror'], ['codemirror']

  def __init__(self, report, vals, color, width, height, htmlCode, options, helper, profile):
    super(Code, self).__init__(report, vals, code=htmlCode, css_attrs={"width": width, "height": height, "color": color}, profile=profile)
    self.add_helper(helper)
    self.__options = OptCodeMirror.OptionsCode(self, options)
    self.css({'display': 'block', 'margin': '5px 0'})

  @property
  def options(self):
    """
    Description:
    ------------
    Property to set all the possible object for a button

    :rtype: OptCodeMirror.OptionsCode
    """
    return self.__options

  @property
  def js(self):
    """
    Description:
    -----------
    A lot of CodeMirror features are only available through its API. Thus, you need to write code (or use addons) if you want to expose them to your users.

    Related Pages:
    --------------
    https://codemirror.net/doc/manual.html#api

    :rtype: JsCodeMirror.CM
    """
    if self._js is None:
      self._js = JsCodeMirror.CM(self, report=self._report)
    return self._js

  @property
  def dom(self):
    """
    Description:
    ------------
    Javascript Functions

    Return all the Javascript functions defined for an HTML Component.
    Those functions will use plain javascript by default.

    :return: A Javascript Dom object

    :rtype: JsHtmlEditor.CodeMirror
    """
    if self._dom is None:
      self._dom = JsHtmlEditor.CodeMirror(self, report=self._report)
    return self._dom

  @property
  def _js__builder__(self):
    return '''
       htmlObj.setValue(data); Object.keys(options).forEach(function(key){ htmlObj.setOption(key, options[key])}); 
       htmlObj.refresh()'''

  def build(self, data=None, options=None, profile=False):
    if not self.builder_name:
      raise Exception("No builder defined for this HTML component %s" % self.__class__.__name__)

    constructors = self._report._props.setdefault("js", {}).setdefault("constructors", {})

    if isinstance(data, dict):
      # check if there is no nested HTML components in the data
      tmp_data = ["%s: %s" % (JsUtils.jsConvertData(k, None), JsUtils.jsConvertData(v, None)) for k, v in data.items()]
      js_data = "{%s}" % ",".join(tmp_data)
    else:
      js_data = JsUtils.jsConvertData(data, None)
    options, js_options = options or self._jsStyles, []
    for k, v in options.items():
      if isinstance(v, dict):
        row = ["'%s': %s" % (s_k, JsUtils.jsConvertData(s_v, None)) for s_k, s_v in v.items()]
        js_options.append("'%s': {%s}" % (k, ", ".join(row)))
      else:
        if str(v).strip().startswith("function"):
          js_options.append("%s: %s" % (k, v))
        else:
          js_options.append("%s: %s" % (k, JsUtils.jsConvertData(v, None)))
    #
    constructors[
      self.builder_name] = "var %(editorId)s = CodeMirror.fromTextArea(%(htmlId)s, {%(options)s}); %(editorId)s.setSize(null, '%(height)s'); function %(name)s(htmlObj, data, options){%(builder)s}" % {"editorId": self.editorId,
        'htmlId': self.htmlId, 'options': ",".join(js_options), 'name': self.builder_name, 'builder': self._js__builder__, 'height': self.attr['css']['height']}
    return "%s(%s, %s, %s)" % (self.builder_name, self.editorId, js_data, "{%s}" % ",".join(js_options))

  @property
  def editorId(self):
    """
    Description:
    ------------
    Return the Javascript variable of the bespoke
    """
    return "editor_%s" % self.htmlId

  def __str__(self):
    self._report._props.setdefault('js', {}).setdefault("builders", []).append(self.refresh())
    return '<textarea %s></textarea>%s' % (self.get_attrs(pyClassNames=self.style.get_classes()), self.helper)


class Tags(Html.Html):
  name, category, callFnc = 'Tags', None, 'tags'
  # _grpCls = GrpCls.CssGrpClassBase

  def __init__(self, report, vals, title, icon, size, width, height, htmlCode, profile):
    super(Tags, self).__init__(report, vals, width=width[0], widthUnit=width[1], height=height[0], heightUnit=height[1],
                               code=htmlCode, profile=profile)
    self.title, self.icon = title, icon
    self.css({"margin-top": "5px", "font-size": "%s%s" % (size[0], size[1]), "font-family": report.style.defaults.font.family})

  @property
  def val(self):
    return "%(breadCrumVar)s['params']['%(htmlId)s']" % {"htmlId": self.htmlId, "breadCrumVar": self._report.jsGlobal.breadCrumVar}

  def jsEmpty(self):
    return "%(breadCrumVar)s['params']['%(htmlId)s'] = []; $('#%(htmlId)s_tags').text('')" % {"htmlId": self.htmlId, "breadCrumVar": self._report.jsGlobal.breadCrumVar}

  def jsAdd(self, jsData):
    jsData = JsUtils.jsConvertData(jsData, None)
    self.addGlobalFnc('RemoveSelection(srcObj, htmlId)', 'srcObj.parent().remove()',
       fncDsc="Remove the item from the Tags Html component but also from the underlying javascript variable")
    return '''
      $('#%(htmlId)s_tags').append("<span style='margin:2px;background:%(baseColor)s;color:%(whiteColor)s;border-radius:8px;1em;vertical-align:middle;display:inline-block;padding:0 2px 1px 10px;cursor:pointer'>"+ %(jsData)s +"<i onclick='RemoveSelection($(this), \\\"%(htmlId)s\\\")' style='margin-left:10px' class='far fa-times-circle'></i></span>")
      ''' % {"htmlId": self.htmlId, "jsData": jsData, 'whiteColor': self._report.theme.greys[0], "baseColor": self._report.theme.colors[9]}

  def __str__(self):
    return '''
      <div %(attr)s>
        <div style='margin:0;display:inline-block;vertical-align:middle;width:90px;float:left;padding:2px 5px 0 5px;height:30px;border:1px solid %(greyColor)s'>
          <i class="%(icon)s" style="margin-right:10px"></i>%(title)s</div>
        <div id='%(htmlId)s_tags' style='padding:2px 5px 0 5px;border:1px solid %(greyColor)s;height:30px'></div>
      </div>''' % {"attr": self.get_attrs(pyClassNames=self.defined), "title": self.title, 'icon': self.icon,
                   'htmlId': self.htmlId, 'greyColor': self._report.theme.greys[2]}
