
import re
import json
import collections
import functools
import logging

from epyk.core.js import JsUtils
from epyk.core.js import Js
from epyk.core.js.html import JsHtml
from epyk.core.js import packages

from epyk.core.css.styles import GrpCls
from epyk.core.html import Aria

try:  # For python 3
  import urllib.request as urllib2
  import urllib.parse as parse
except:  # For Python 2
  import urllib2
  import urllib as parse


regex = re.compile('[^a-zA-Z0-9_]')


def cleanData(value):
  """ Function to clean the javascript data to allow the use of variables """
  return regex.sub('', value.strip())


# ---------------------------------------------------------------------------------------------------------
#                                          FRAMEWORK DECORATORS
#
# ---------------------------------------------------------------------------------------------------------
def deprecated(func):
  """
  This is a decorator which can be used to mark functions
  as deprecated. It will result in a warning being emmitted
  when the function is used.
  """

  @functools.wraps(func)
  def new_func(*args, **kwargs):
    logging.warn('#########################################')
    logging.warn("Call to deprecated function {}.".format(func.__name__))
    logging.warn('#########################################')
    return func(*args, **kwargs)
  return new_func


def inprogress(func):
  @functools.wraps(func)
  def new_func(*args, **kwargs):
    # warnings.simplefilter('always', DeprecationWarning)  # turn off filter
    # warnings.warn('############################################################################')
    # warnings.warn("Call to a test function {}.".format(func.__name__), category=DeprecationWarning, stacklevel=2)
    # warnings.warn('############################################################################')
    # warnings.simplefilter('default', DeprecationWarning)  # reset filter
    return func(*args, **kwargs)

  return new_func


class Html(object):
  """
  Parent class for all the HTML components. All the function defined here are available in the children classes.
  Child class can from time to time re implement the logic but the function will always get the same meaning (namely the same signature and return)
  """
  cssCls = None
  # Those variables should not be used anymore and should be replaced by the __ ones
  # This is done in order to avoid having users to change them. Thanks to the name
  # mangling technique Python will make the change more difficult and easier to see
  reqJs, reqCss = [], []
  htmlCode, dataSrc, _code, inReport, builder_name = None, None, None, True, None

  def __init__(self, report, vals, htmlCode=None, code=None, width=None, widthUnit=None, height=None,
               heightUnit=None, globalFilter=None, dataSrc=None, options=None, profile=None, css_attrs=None):
    """ Create an python HTML object """
    self._triggerEvents, self.profile = set(), profile
    self._report, self._styleObj = report, None # The html object ID
    self._dom, self._container, self._sub_htmls, self._js, self.helper = None, None, [], None, ""
    self.jsImports = report.jsImports
    self.cssImport = report.cssImport
    self.attr = {'class': self.style.classList['main'], 'css': self.style.css.attrs}
    if css_attrs is not None:
      self.css(css_attrs)
    self.jsFncFrag, self._code, self._jsStyles, self._events = {}, code, {}, {"comp_ready": {}, 'doc_ready': {}}
    self.innerPyHTML = None
    if code is not None:
      # Control to ensure the Javascript problem due to multiple references is highlighted during the report generation
      if code in self._report.htmlRefs:
        raise Exception("Duplicated Html Code %s in the script !" % code)

      self._report.htmlRefs[code] = True
      self._report.htmlCodes[code] = self
      if code[0].isdigit() or cleanData(code) != code:
        raise Exception("htmlCode %s cannot start with a number or contain, suggestion %s " % (code, cleanData(code)))

    if htmlCode is not None:
      self._report.htmlRefs[htmlCode] = True
      if htmlCode[0].isdigit() or cleanData(htmlCode) != htmlCode:
        raise Exception("htmlCode %s cannot start with a number or contain, suggestion %s " % (htmlCode, cleanData(htmlCode)))

      self._report.htmlCodes[htmlCode] = self
      try:
        int(htmlCode[0])
        raise Exception("htmlCode cannot start with a number - %s" % htmlCode)

      except: pass

      self.htmlCode = htmlCode
      # self._report.jsGlobal.reportHtmlCode.add(htmlCode)
      if htmlCode in self._report.http:
        self.vals = self._report.http[htmlCode]

    #css = None
    self.pyStyle = None #list(getattr(self, '_%s__pyStyle' % self.__class__.__name__, []))
    if hasattr(self, '_%s__reqJs' % self.__class__.__name__):
      self.reqJs = list(getattr(self, '_%s__reqJs' % self.__class__.__name__, []))
    if hasattr(self, '_%s__reqCss' % self.__class__.__name__):
      self.reqCss = list(getattr(self, '_%s__reqCss' % self.__class__.__name__, []))
    self.pyCssCls = set()
    self.jsOnLoad, self.jsEvent, self.jsEventFnc = set(), {}, collections.defaultdict(set)
    self._vals = vals
    self.jsVal = "%s_data" % self.htmlId
    if self._report is not None:
       # Some components are not using _report because they are directly used for the display
       if self.reqJs is not None:
         for js in self.reqJs:
           self._report.jsImports.add(js)

       if self.reqCss is not None:
         for css in self.reqCss:
           self._report.cssImport.add(css)
    # Add the CSS dimension
    if width is not None:
      self.css({'width': "%s%s" % (width, widthUnit)})
    if height is not None:
      self.css('height', "%s%s" % (height, heightUnit))
    if htmlCode is not None and globalFilter is not None:
      self.filter(**globalFilter)
    if dataSrc is not None:
      self.dataSrc = dataSrc
    self.builder_name = self.builder_name if self.builder_name is not None else self.__class__.__name__

  @property
  def style(self):
    if self._styleObj is None:
      self._styleObj = GrpCls.ClassHtml(self)
    return self._styleObj

  @property
  def htmlId(self):
    if self._code is not None:
      # This is a special code used to update components but not to store the results to the breadcrumb
      # Indeed for example for components like paragraph this does not really make sense to use the htmlCode
      return self._code

    if self.htmlCode is not None:
      return self.htmlCode

    return "%s_%s" % (self.__class__.__name__.lower(), id(self))

  @property
  def js(self):
    """
    Description:
    -----------
    Javascript base function

    Return all the Javascript functions defined in the framework.
    THis is an entry point to the full Javascript ecosystem.

    :return: A Javascript object
    :rtype: Js.JsBase
    """
    if self._js is None:
      self._js = Js.JsBase(self._report)
    return self._js

  @property
  def dom(self):
    """
    Javascript Functions

    Return all the Javascript functions defined for an HTML Component.
    Those functions will use plain javascript by default.

    :return: A Javascript Dom object

    :rtype: JsHtml.JsHtml
    """
    if self._dom is None:
      self._dom = JsHtml.JsHtml(self, report=self._report)
    return self._dom

  def prepend_child(self, htmlObj):
    """
    Description:
    -----------
    Wrapper to the Javascript method insertChild to add an HTML component

    Usage::

      for i in range(10):
      encore = rptObj.ui.texts.label("Add Label %s" % i).css({"width": "100%", "display": 'block'})
      select.prepend_child(encore)

    Related Pages:

			https://www.w3schools.com/jsref/met_node_insertbefore.asp

    Attributes:
    ----------
    :param htmlObj: The html component
    :return: The htmlObj
    """
    self._sub_htmls.append(htmlObj)
    htmlObj.inReport = False
    # add a flag to propagate on the Javascript the fact that some child nodes will be added
    # in this case innerHYML cannot be used anymore
    self._jsStyles["_children"] = self._jsStyles.get("_children", 0) + 1
    self._report.js.addOnLoad([self.dom.insertBefore(htmlObj.dom)])
    return self

  def append_child(self, htmlObj):
    """
    Description:
    -----------
    Wrapper to the Javascript method appendChild to append an HTML component

    Usage::

      for i in range(10):
      encore = rptObj.ui.texts.label("Add Label %s" % i).css({"width": "100%", "display": 'block'})
      select.append_child(encore)

    Related Pages:

			https://www.w3schools.com/jsref/met_node_appendchild.asp

    Attributes:
    ----------
    :param htmlObj: The html component

    :return: The htmlObj
    """
    self._sub_htmls.append(htmlObj)
    htmlObj.inReport = False
    # add a flag to propagate on the Javascript the fact that some child nodes will be added
    # in this case innerHYML cannot be used anymore
    self._jsStyles["_children"] = self._jsStyles.get("_children", 0) + 1
    self._report.js.addOnLoad([self.dom.appendChild(htmlObj.dom)])
    return self

  def onReady(self, jsFncs):
    """
    Description:
    -----------
    Add set of event / actions whihc will be triggered after the build of the object.
    usually this can be used to add js functions on a chart or a table

    Usage::

      network = rptObj.ui.charts.vis.network()
    network.onReady([
      network.js.setData({"nodes": [{"id": 0, "label": "test"}], "edges": []}),
    ])

    Attributes:
    ----------
    :param jsFncs: List. Javascript function to be added once the object is built
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    self._report.js.addOnReady(jsFncs)

  def add_menu(self, context_menu):
    """
    Description:
    -----------
    Attach a context menu to an existing component. A context menu must have a component attached to otherwise
    the report will not be triggered

    Attributes:
    ----------
    :param context_menu: A Python context menu object
    """
    context_menu.source = self
    self._report._contextMenu[self.dom.jquery.varName] = context_menu
    return self

  def add_icon(self, text, css=None, position="before"):
    """
    Description:
    ------------
    Add an icon to the HTML object

    Usage::

      checks.title.add_icon("fas fa-align-center")

    Related Pages:
Attributes:
    ----------
    :param text: The icon reference from font awsome website
    :param css: Optional. A dictionary with the CSS style to be added to the component
    :param position:

    :return: The Html object
    """
    self.icon = ""
    if text is not None:
      self.icon = self._report.ui.images.icon(text).css({"margin-right": '5px'})
      if position == "before":
        self.prepend_child(self.icon)
      else:
        self.append_child(self.icon)
      #elf.icon.inReport = False
      if css is not None:
        self.icon.css(css)
    return self

  def add_label(self, text, css=None, position="before", for_=None):
    """
    Description:
    -----------
    Add an elementary label component

    Usage::

      Related Pages:

			https://www.w3schools.com/tags/tag_label.asp

    Attributes:
    ----------
    :param text: The label content
    :param css: Optional. A dictionary with the CSS style to be added to the component
    :param position:
    :param for_: Specifies which form element a label is bound to
    """
    self.label = ""
    if text is not None:
      self.label = self._report.ui.texts.label(text)
      if for_ is not None:
        # Attach the label to another HTML component based on the ID
        self.label.attr['for'] = for_
      if position == "before":
        self.prepend_child(self.label)
      else:
        self.append_child(self.label)
      if css == False:
        self.label.attr['css'] = {}
      elif css is not None:
        self.label.css(css)
    return self

  def add_span(self, text, css=None, position="before", i=None):
    """
    Description:
    -----------
    Add an elementary span component

    Usage::

      Related Pages:

			https://fontawesome.com/how-to-use/on-the-web/styling/layering

    Attributes:
    ----------
    :param text: The Span content
    :param css: Optional. A dictionary with the CSS style to be added to the component
    :param position:
    :param i:
    """
    if i is not None:
      key_attr = 'span_%s' % i
    else:
      key_attr = 'span'
    setattr(self, key_attr, '')
    if text is not None:
      setattr(self, key_attr, self._report.ui.texts.span(text))
      span = getattr(self, key_attr)
      if position == "before":
        self.prepend_child(span)
      else:
        self.append_child(span)
      if css == False:
        span.attr['css'] = {}
      elif css is not None:
        span.css(css)
    return self

  def add_link(self, text, url=None, script_name=None, report_name=None, name=None, icon=None, css=None, position="before"):
    """
    Description:
    -----------
    Add an elementary label component

    Usage::

      div = rptObj.ui.div()
    div.add_link("test.py", name="Click to go to the test report")

    Attributes:
    ----------
    :param text:
    :param url:
    :param script_name:
    :param report_name:
    :param name:
    :param icon:
    :param css: Optional. A dictionary with the CSS style to be added to the component
    :param position:
    """
    self.link = ""
    if url is not None or script_name is not None:
      options = {"name": name} if name is not None else {}
      if url is not None:
        self.link = self._report.ui.links.external(text, url)
      else:
        self.link = self._report.ui.links.script(text, script_name, report_name, icon=icon, options=options)
      if position == "before":
        self.prepend_child(self.link)
      else:
        self.append_child(self.link)
      if css is not None:
        self.link.css(css)
    return self

  def add_title(self, text, level=None, css=None, position="before", options=None):
    """
    Description:
    -----------
    Add an elementary title component

    Usage::

      Attributes:
    ----------
    :param text: The title content
    :param css: Optional. A dictionary with the CSS style to be added to the component
    :param position:
    """
    self.title = ""
    if text is not None:
      self.title = self._report.ui.texts.title(text, level=level, options=options)
      if options.get('managed', True):
        if position == "before":
          self.prepend_child(self.title)
        else:
          self.append_child(self.title)
      else:
        self.title.inReport = False
      if css == False:
        self.title.attr['css'] = {}
      elif css is not None:
        self.title.css(css)
    return self

  def add_input(self, text, css=None, attrs=None, position="before"):
    """
    Description:
    -----------
    Add an elementary input component

    Usage::

      Attributes:
    ----------
    :param text: The title content
    :param css: Optional. A dictionary with the CSS style to be added to the component
    :param attrs: Optional
    :param position:
    """
    self.input = ""
    if text is not None:
      self.input = self._report.ui.inputs.input(text)
      if position == "before":
        self.prepend_child(self.input)
      else:
        self.append_child(self.input)
      if css is not None:
        self.input.css(css)
      if attrs is not None:
        self.input.set_attrs(attrs=attrs)
    return self

  def add_checkbox(self, flag, css=None, attrs=None, position="before"):
    """
    Description:
    -----------
    Add an elementary checkbox component

    Usage::

      Attributes:
    ----------
    :param flag: Boolean. The state of the checkbox component
    :param css: Optional. A dictionary with the CSS style to be added to the component
    :param attrs: Optional
    :param position:
    """
    self.checkbox = ""
    if flag is not None:
      self.checkbox = self._report.ui.inputs.checkbox(flag)
      if position == "before":
        self.prepend_child(self.checkbox)
      else:
        self.append_child(self.checkbox)
      if css is not None:
        self.checkbox.css(css)
      if attrs is not None:
        self.checkbox.set_attrs(attrs=attrs)
    return self

  def add_helper(self, text, css=None):
    """
    Description:
    -----------
    Add an elementary helper icon

    Usage::

      Attributes:
    ----------
    :param text: The helper content
    :param css: Optional. A dictionary with the CSS style to be added to the component

    :rtype: self._report.ui.rich.info
    """
    if text is not None:
      self.helper = self._report.ui.rich.info(text)
      self.helper.inReport = False
      if css is not None:
        self.helper.css(css)
    return self

  @property
  def aria(self):
    """
    Accessible Rich Internet Applications is a [HTML] specification module.
    Web developers MAY use the ARIA role and aria-* attributes on HTML elements

    Related Pages:

			https://www.w3.org/TR/html-aria/#allowed-aria-roles-states-and-properties
    """
    return Aria.Aria(self)

  @property
  def val(self):
    """
    Description:
    -----------
    Property to get the jquery value of the HTML object in a python HTML object.
    This method can be used in any jsFunction to get the value of a component in the browser.
    This method will only be used on the javascript side, so please do not consider it in your algorithm in Python

    :returns: Javascript string with the function to get the current value of the component
    """
    return self._vals

  @property
  def content(self):
    if self.innerPyHTML is not None:
      if isinstance(self.innerPyHTML, list):
        return "".join([h.html() for h in self.innerPyHTML])

      return self.innerPyHTML.html()

    return self.val if not hasattr(self.val, "html") else self.val.html()

  def move(self):
    """
    Description:
    -----------
    Move the component to this position in the page
    """
    comp_id = id(self)
    self._report.content.remove(comp_id)
    self._report.content.append(comp_id)

  def css(self, key, value=None, reset=False):
    """
    Description:
    -----------
    Change the CSS Style of a main component. This is trying to mimic the signature of the Jquery css function

    Related Pages:
http://api.jquery.com/css/

    Attributes:
    ----------
    :param key: The key style in the CSS attributes (Can also be a dictionary)
    :param value: The value corresponding to the key style
    :param reset: Boolean

    :return: The python object itself
    """
    if reset:
      self.style.css.attrs = {}
      self.attr['css'] = self.style.css.attrs
    if value is None and isinstance(key, dict):
      # Do not add None value to the CSS otherwise it will break the page on the front end side
      css_vals = key if isinstance(key, dict) else {}
    elif value is None and not isinstance(key, dict):
      return self.attr['css'].get(key)

    else:
      if isinstance(value, tuple):
        value = value[0] if value[0] is None else "%s%s" % (value[0], value[1])
      css_vals = {key: value}
    if not 'css' in self.attr:
      self.attr['css'] = self.style.css.attrs
    for key, value in css_vals.items():
      if isinstance(value, tuple):
        if value[0] is None:
          continue

        value = "%s%s" % (value[0], value[1])
      if value is None:
        continue

      self.attr['css'][key] = value if isinstance(value, str) else json.dumps(value)
    return self

  def tooltip(self, value, location='top'):
    """
    Description:
    -----------
    Add the Tooltip feature when the mouse is over the component.
    This tooltip version is coming from Bootstrap

    Usage::

      htmlObj.tooltip("My tooltip", location="bottom")

    Related Pages:

			https://getbootstrap.com/docs/4.1/components/tooltips/

    Attributes:
    ----------
    :param value:
    :param location:

    :return: The Python object self
    """
    self.attr.update({'title': value, 'data-toggle': 'tooltip', 'data-placement': location})
    self._report._props['js']['onReady'].add("%s.tooltip()" % self.dom.jquery.varId)
    return self

  @packages.packageImport('bootstrap', 'bootstrap')
  def popover(self, content, title=None, options=None):
    """
    Description:
    -----------
    All the attributes will be added to the

    Related Pages:

			https://getbootstrap.com/docs/4.4/components/popovers/

    Attributes:
    ----------
    :param content: String. The tooltip content
    :param title: String. The tooltip title
    :param options: Dictionary all the options to be attached to the component
    """
    self.attr["data-content"] = content
    if title is not None:
      self.attr["data-title"] = title
    if options is not None:
      for k, v in options.items():
        self.attr["data-%s" % k] = title
    self.attr["data-toggle"] = 'popover'
    self._report._props['js']['onReady'].add("$('[data-toggle=\"popover\"]').popover()")
    return self

  def add_options(self, options=None, name=None, value=None):
    """
    Description:
    -----------
    Change the Javascript options of the component.
    This will change the options sent to the Javascript

    Attributes:
    ----------
    :param options: Dictionary with the options
    :param name: String. The key
    :param value: String. The value

    :return: self to allow the chains
    """
    if options is None and name is None:
      raise Exception("Either the attrs or the name should be specified")

    if options is None:
      options = {name: value}
    for k, v in options.items():
      self._jsStyles[k] = v
    return self

  def set_attrs(self, attrs=None, name=None, value=None):
    """
    Description:
    -----------
    Function to update the internal dictionary of object attributes. Those attributes will be used when the HTML component will be defined.
    Basically all sort of attributes can be defined here: CSS attributes, but also data, name...
    Either the attrs or the tuple (name, value) can be used to add information to the dom object.

    All the attributes should be Python object which are ready to use on the Javascript side.
    For example True should be written 'true'

    Tips: It is possible to use the data- attributes to store any kind of information in the dom.

    Related Pages:
Attributes:
    ----------
    :param attrs: A python dictionary with the attributes
    :param name: A python string with the name of the attribute
    :param value: A python string with the value of the attribute
    """
    if attrs is None and name is None:
      raise Exception("Either the attrs or the name should be specified")

    if attrs is None:
      attrs = {name: value}
    for k, v in attrs.items():
      if k == 'css':
        # Section for the Style attributes
        if v is None:
          self.style.clear_style()
          continue

        if not 'css' in self.attr:
          self.attr['css'] = dict(v)
        else:
          self.attr['css'].update(v)
      elif k == 'class':
        self.style.clear()
        if v is None:
          continue

        if not isinstance(v, set):
          v = set(v.split(" "))
        for c in v:
          self.attr['class'].add(c)
      else:
        # Section for all the other attributes#
        if v is not None:
          self.attr[k] = v
    return self

  def get_attrs(self, withId=True, pyClassNames=None):
    """
    Description:
    -----------
    Return the string line with all the attributes

    All the attributes in the div should use double quote and not simple quote to be consistent everywhere in the framework
    and also in the javascript. If there is an inconsistency, the aggregation of the string fragments will not work

    Attributes:
    ----------
    :param withId:
    :param pyClassNames:

    :return: A string with the dom attributes
    """
    cssStyle, cssClass, classData = '', '', ''
    if 'css' in self.attr:
      styles = ";".join(["%s:%s" % (key, val) for key, val in self.attr["css"].items()])
      if styles:
        cssStyle = 'style="%s"' % styles
    if 'class' in self.attr and len(self.attr['class']) > 0 and classData:
      if pyClassNames is not None:
        # Need to merge in the class attribute some static classes coming from external CSS Styles sheets
        # and the static python classes defined on demand in the header of your report
        # self._report.cssObj.getClsTag(pyClassNames)[:-1] to remove the ' generated in the module automatically
        cssClass = self._report.style.getClsTag(pyClassNames.clsMap).replace('class="', 'class="%s ')
        if cssClass:
          cssClass %= classData
        else:
          cssClass = 'class="%s"' % classData
      else:
        cssClass = 'class="%s"' % classData
    elif pyClassNames is not None:
      pyClsNames = [cls.get_ref() if hasattr(cls, 'get_ref') else cls for cls in pyClassNames['main']]
      cssClass = 'class="%s"' % " ".join(pyClsNames) if len(pyClsNames) > 0 else ""
    if withId:
      str_tag = 'id="%s" %s %s %s' % (self.htmlId, " ".join(['%s="%s"' % (key, str(val).replace('"', "'")) if val is not None else key for key, val in self.attr.items() if key not in ('css', 'class')]), cssStyle, cssClass)
      return str_tag.strip()

    str_tag = '%s %s %s' % (" ".join(['%s="%s"' % (key, str(val).replace('"', "'")) if val is not None else key for key, val in self.attr.items() if key not in ('css', 'class')]), cssStyle, cssClass)
    return str_tag.strip()

  # -------------------------------------------------------------
  # Javascript Event wrappers
  #
  def on(self, event, jsFncs, profile=False):
    """
    Description:
    -----------
    Add an event to the document ready function.
    This is to mimic the Jquery on function.

    Related Pages:

			https://www.w3schools.com/jquery/event_on.asp
    https://www.w3schools.com/js/js_htmldom_eventlistener.asp
    https://www.w3schools.com/jsref/dom_obj_event.asp

    Attributes:
    ----------
    :param event: A string with the Javascript event type from the dom_obj_event.asp
    :param jsFncs: A Javascript Python function
    :param profile: A Boolean. Set to true to get the profile for the function on the Javascript console

    :return: self to allow the chains
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    # JsUtils.jsConvertFncs needs to be applied in order to freeze the function
    # span.on("mouseover", span.dom.css("color", "red"))
    # span.on("mouseleave", span.dom.css("color", "blue"))
    self._events['doc_ready'].setdefault(event, {}).setdefault("content", []).extend(JsUtils.jsConvertFncs(jsFncs))
    self._events['doc_ready'][event]['profile'] = profile
    return self

  def drop(self, jsFncs, preventDefault=True, profile=False):
    """
    Description:
    -----------
    Add a drag and drop property to the element

    Usage::

      d = rptObj.ui.div()
    d.drop([rptObj.js.objects.data.toRecord([1, 2, 3, 4], "result")])

    Attributes:
    ----------
    :param jsFncs:
    :param preventDefault: Boolean.
    :param profile:

    :return: Return self to allow the chaining
    """
    dft_fnc = ""
    if preventDefault:
      dft_fnc = self.js.objects.event.preventDefault()
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    str_fncs = JsUtils.jsConvertFncs(["var data = %s" % self.js.objects.event.dataTransfer.text] + jsFncs, toStr=True)
    self.attr["ondrop"] = "(function(event){%s; %s; return false})(event)" % (dft_fnc, str_fncs)
    self.attr["ondragover"] = "(function(event){%s})(event)" % dft_fnc
    return self

  def hover(self, jsFncs, profile=False):
    return self.on("mouseover", jsFncs, profile)

  def click(self, jsFncs, profile=False):
    return self.on("click", jsFncs, profile)

  def mouse(self, on_fncs=None, out_fncs=None):
    """
    Description:
    -----------
    Wrapper function fot the mouse event.
    This function will cover the on mouse hover event and mouse out.

    More specific events are possible using the generic out function

    Usage::

      span.mouse([
        span.dom.css("color", "red"),
        span.dom.css("cursor", "pointer").r],
        span.dom.css("color", "blue").r)

    Related Pages:
Attributes:
    ----------
    :param on_fncs: Array or String of Javascript events
    :param out_fncs: Array or String of Javascript events

    :return: self to allow the chains
    """
    if on_fncs is not None:
      self.on("mouseover", on_fncs)
    if out_fncs is not None:
      self.on("mouseleave", out_fncs)
    return self

  def contextMenu(self, menu, jsFncs, profile=False):
    """
    Description:
    -----------
    Attach a context menu to a component and set a function to called before the display

Attributes:
    ----------
    :param menu:
    :param jsFncs:
    :param profile:
    """
    menu.source = self
    # event.stopPropagation(); %(jqId)s.css({left: event.pageX + 1, top: event.pageY + 1, display: 'block'}); event.preventDefault()
    new_js_fncs = jsFncs + [self._report.js.objects.mouseEvent.stopPropagation(),
                   menu.dom.css({"display": 'block', 'left': self._report.js.objects.mouseEvent.clientX + "'px'",
                                 'top': self._report.js.objects.mouseEvent.clientY + "'px'"}),
                   self._report.js.objects.mouseEvent.preventDefault()]
    self.on("contextmenu", new_js_fncs, profile)
    return self

  # -------------------------------------------------------------
  # Builder functions
  #
  @property
  def _js__builder__(self):
    raise Exception("Constructor must be defined in %s" % self.__class__.__name__)

  def build(self, data=None, options=None, profile=False):
    if not self.builder_name:
      raise Exception("No builder defined for this HTML component %s" % self.__class__.__name__)

    constructors = self._report._props.setdefault("js", {}).setdefault("constructors", {})
    constructors[self.builder_name] = "function %s(htmlObj, data, options){%s}" % (
    self.builder_name, self._js__builder__)

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
    return "%s(%s, %s, %s)" % (self.builder_name, self.dom.varId, js_data, "{%s}" % ",".join(js_options))

  def refresh(self):
    # self._report._props.setdefault('js', {}).setdefault("builders", []).append(refresh_js)
    return self.build(self.val, self._jsStyles)

  def onDocumentLoadContextmenu(self):
    self._report.jsGlobal.fnc("ContextMenu(htmlObj, data, markdownFnc)",
        '''
        $('#popup').empty(); $('#popup').append('<ul style="width:100%%;height:100%%;margin:0;padding:0"></ul>');
        var listMenu = $('#popup').find('ul');
        data.forEach(function(rec){
          if ('title' in rec) {
            listMenu.append('<li class="list-group-item" style="cursor:cursor;width:100%%;display:inline-block;padding:5px 5px 2px 10px;font-weight:bold;color:white;background:%(color)s">' + rec.title + '</li> ');
          } else {
            if (rec.url != undefined) { var content = '<a href="' + rec.url + '" style="color:black">' + rec.label + '</a>' ;} else {var content = rec.label;};
            listMenu.append('<li class="list-group-item" style="cursor:pointer;width:100%%;display:inline-block;padding:2px 5px 2px 10px">' + content + '</li> '); }
        });
        if (markdownFnc != false) {
          listMenu.append('<li class="list-group-item" style="cursor:cursor;width:100%%;display:inline-block;padding:5px 5px 2px 10px;font-weight:bold;color:white;background:%(color)s">MarkDown</li> ');
          listMenu.append('<li onclick="CopyMarkDown(\\''+ markdownFnc +'\\');" class="list-group-item" style="cursor:pointer;width:100%%;display:inline-block;padding:2px 5px 2px 10px"><i class="fas fa-thumbtack"></i>&nbsp;&nbsp;Copy MarkDown</li> ');};
        $('#popup').css({'padding': '0', 'width': '200px'});
        $('#popup').show()''' % {'color': self._report.theme.colors[9]})

  def paste(self, jsFnc):
    """ Generic click function """
    self._report.jsOnLoadFnc.add('''%(jqId)s.on('paste', function(event) { 
       var data;
       if (window.clipboardData && window.clipboardData.getData) { // IE
            data = window.clipboardData.getData('Text'); }
        else if (event.originalEvent.clipboardData && event.originalEvent.clipboardData.getData) { // other browsers
            data = event.originalEvent.clipboardData.getData('text/plain')} 
        %(jsFnc)s 
      })''' % {'jqId': self.jqId, 'jsFnc': jsFnc})

  def filter(self, jsId, colName, allSelected=True, filterGrp=None, operation="=", itemType="string"):
    filterObj = {"operation": operation, 'itemType': itemType, 'allIfEmpty': allSelected, 'colName': colName, 'val': self.val, 'typeVal': 'js'}
    self._report.jsSources.setdefault(jsId, {}).setdefault('_filters', {})[self.htmlCode] = filterObj
    return self

  # def _addToContainerMap(self, htmlObj):
  #   if hasattr(self, 'htmlMaps'):
  #     if hasattr(htmlObj, 'htmlMaps'):
  #       # It is a container and we need to get the mapping of the different components inside
  #       self.htmlMaps.update(htmlObj.htmlMaps)
  #     else:
  #       if getattr(htmlObj, 'htmlCode', None) is not None:
  #         if htmlObj.category == 'Table':
  #           self.htmlMaps[htmlObj.htmlCode] = (htmlObj.__class__.__name__, '%s_table' % htmlObj.htmlCode)
  #         elif htmlObj.category == 'Charts':
  #           self.htmlMaps[htmlObj.htmlCode] = ('PyChartJs', '$("#%s")' % htmlObj.htmlCode)
  #         else:
  #           self.htmlMaps[htmlObj.htmlCode] = (htmlObj.__class__.__name__, htmlObj.jqId)
  #       elif getattr(htmlObj, '_code', None) is not None:
  #         if htmlObj.category == 'Table':
  #           self.htmlMaps[htmlObj._code] = (htmlObj.__class__.__name__, '%s_table' % htmlObj._code)
  #         elif htmlObj.category == 'Charts':
  #           self.htmlMaps[htmlObj._code] = ('PyChartJs', '$("#%s")' % htmlObj._code)
  #         else:
  #           self.htmlMaps[htmlObj._code] = (htmlObj.__class__.__name__, htmlObj.jqId)

  # -------------------------------------------------------------------------------------------------------------------
  #                    OUTPUT METHODS
  # -------------------------------------------------------------------------------------------------------------------
  def __str__(self):
    """
    Description:
    -----------
    Apply the corresponding function to build the HTML result.
    This function is very specific and it has to be defined in each class.
    """
    raise NotImplementedError('subclasses must override __str__()!')

  def to_word(self, document):
    """
    Description:
    -----------
    Apply the corresponding function to produce the same result in a word document.
    This function is very specific and it has to be defined in each class.

    Related Pages:
http://python-docx.readthedocs.io/en/latest/
    """
    raise NotImplementedError('''
      subclasses must override to_word(), %s !
      Go to http://python-docx.readthedocs.io/en/latest/user/quickstart.html for more details  
    ''' % self.__class__.__name__)

  def to_xls(self, workbook, worksheet, cursor):
    """
    Description:
    -----------
    Apply the corresponding function to produce the same result in a word document.
    This function is very specific and it has to be defined in each class.

    Related Pages:

			https://xlsxwriter.readthedocs.io/
    """
    raise NotImplementedError('''
      subclasses must override to_xls(), %s !
      Go to https://xlsxwriter.readthedocs.io/working_with_tables.html for more details  
    ''' % self.__class__.__name__)

  def html(self):
    str_result = []
    for htmlObj in self._sub_htmls:
      str_result.append(htmlObj.html())
    if self.helper != "":
      self.helper.html()
    #if self.builder_name:
    #  self._report._props.setdefault('js', {}).setdefault("builders", []).append(self.refresh())
    for c in self.style.get_classes()['main']:
      if hasattr(c, 'get_ref'):
        self.pyCssCls.add(c.get_ref())
    str_result.append(str(self))
    return "".join(str_result)


class Body(Html):
  name = "Body"

  @property
  def style(self):
    if self._styleObj is None:
      self._styleObj = GrpCls.ClassPage(self)
    return self._styleObj

  @property
  def htmlId(self):
    return "body"

  @property
  def dom(self):
    """
    Javascript Functions

    Return all the Javascript functions defined for an HTML Component.
    Those functions will use plain javascript by default.

    :return: A Javascript Dom object

    :rtype: JsHtml.JsHtml
    """
    if self._dom is None:
      self._dom = JsHtml.JsHtml(self, report=self._report)
      self._dom.varName = "document.body"
    return self._dom

  def onReady(self, jsFncs):
    """
    Description:
    -----------
    Add set of event / actions whihc will be triggered after the build of the object.
    usually this can be used to add js functions on a chart or a table

    Usage::

      network = rptObj.ui.charts.vis.network()
    network.onReady([
      network.js.setData({"nodes": [{"id": 0, "label": "test"}], "edges": []}),
    ])

    Attributes:
    ----------
    :param jsFncs: List. Javascript function to be added once the object is built
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    self._report.js.addOnReady(jsFncs)

  def onLoad(self, jsFncs):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param jsFncs:
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    self._report._props.setdefault('js', {}).setdefault("builders", []).append(JsUtils.jsConvertFncs(jsFncs, toStr=True))

  def set_content(self, report, page_content):
    """
    Description:
    ------------
    Function to allow the templating of the report.
    This can be overridden by a generic class which can be shared within a set of report

    Attributes:
    ----------
    :param report: Report. The main report object
    :param page_content: String. The html content of the page

    :return: The Body HTML object
    """
    self._html_content = page_content
    return self

  def set_background(self, start_color=None, end_color=None, from_theme=False):
    """
    Description:
    ------------
    Change the body background color

    Usage::

      rptObj.body.set_background("#101626", "#374F67")

    Attributes:
    ----------
    :param start_color:
    :param end_color:
    """
    if from_theme or (start_color is None and end_color is None):
      self.style.css.background = "linear-gradient(%s 0%%, %s 100%%)" % (self._report.theme.colors[-1], self._report.theme.colors[2])
    elif end_color is not None:
      self.style.css.background = "linear-gradient(%s 0%%, %s 100%%)" % (start_color, end_color)
    else:
      self.style.css.background = start_color
    self.style.css.background_repeat = "no-repeat"
    self.style.css.background_color = self._report.theme.colors[2]

  def __str__(self):
    return '<body %s>%s</body>' % (self.get_attrs(pyClassNames=self.style.get_classes(), withId=False), self._html_content)
