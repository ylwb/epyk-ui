
import json
import collections
import datetime
import time

try:
  basestring
except NameError:
  basestring = str

from epyk.core.js import Imports
from epyk.interfaces import Components
from epyk.core.css.themes import Theme
from epyk.core.css import Classes

from epyk.core import html
from epyk.core import js
from epyk.core import data

from epyk.core.html import symboles
from epyk.core.html import entities
from epyk.core.py import OrderedSet
from epyk.core.py import PyOuts
from epyk.core.py import PyExt


class Report(object):
  showNavMenu, withContainer = False, False
  ext_packages = None # For extension modules

  def __init__(self):
    #
    self._css, self._ui, self._js, self._py, self._theme, self.__body = {}, None, None, None, None, None
    self._props, self._tags, self._header_obj, self.__import_manage = {'js': {'onReady': OrderedSet(), 'datasets': {}}}, None, None, None

    self.timestamp, self.runTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), time.time() * 100
    self.content, self.shortcuts, self.exportCsv, self.jsSources = [], {}, {}, {}
    self._dbBindings, self._dbErrors = {}, collections.defaultdict(int)
    self.currentTitleObj, self.navBarContent, self.sideBarActions = {}, {'content': []}, []
    self.htmlItems, self.jsOnLoad, self.http, self.htmlCodes, self.htmlRefs = {}, [], {}, {}, {}
    self.notifications = collections.defaultdict(list)
    self.interruptReport, self._propagate = (False, None), []

    self.sourceDef, self.localFiles, self.libDef, self._run, self._scroll, self._contextMenu = {}, {}, {}, {}, set(), {}
    self.logo, self._dbSettings, self.dbsDef, self._cssText, self._jsText = None, None, {}, [], []

    #
    self.jsOnLoadFnc, self.jsWindowLoadFnc = OrderedSet(), OrderedSet()
    self.jsOnLoadEvtsFnc = OrderedSet()

    self.jsImports, self.cssImport = set(), set()
    self.jsLocalImports, self.cssLocalImports = set(), set()

  @property
  def body(self):
    """
    Description:
    ------------
    Property that returns the Body element of the HTML page
    """
    if self.__body is None:
      self.__body = html.Html.Body(self, None)
    return self.__body

  @body.setter
  def body(self, calc):
    self.__body = calc(self, None)

  @property
  def theme(self):
    """
    Description:
    ------------
    Return the currently used :doc:`report/theme` for the report
    """
    if self._theme is None:
      self._theme = Theme.ThemeDefault()
    return self._theme

  @theme.setter
  def theme(self, theme):
    if isinstance(theme, dict):
      self._theme = Theme.ThemeCustome()
      self._theme = theme
    else:
      self._theme = theme

  def imports(self, online=False):
    """
    Description:
    ------------
    Return the :doc:`report/import_manager`, which allows to import automatically packages for certain components to run.
    """
    if self.__import_manage is None:
      self.__import_manage = Imports.ImportManager(online, report=self)
    return self.__import_manage

  @property
  def symbols(self):
    """
    Description:
    ------------
    Shortcut to the HTML symbols

    Related Pages:

      https://www.w3schools.com/html/html_symbols.asp
      https://www.w3schools.com/charsets/ref_utf_math.asp

    Those can be added in string in order to improve the render of a text.
    """
    return symboles.Symboles()

  @property
  def entities(self):
    """
    Description:
    ------------
    Shortcut to the HTML Entities

    Related Pages:

      https://www.w3schools.com/html/html_entities.asp

    Those can be added in string in order to improve the render of a text.
    """
    return entities.Entities()

  @property
  def ui(self):
    """
    Description:
    ------------
    User Interface section.

    All the :doc:`components <report/ui>` which can be used in the dashboard to display the data.
    Within this object different categories of items can be used like (list, simple text, charts...)

    Related Pages:

	    https://www.w3schools.com/html/default.asp

    :rtype: :doc:`Components.Components <report/ui>`

    :return: Python HTML object
    """
    if self._ui is None:
      self._ui = Components.Components(self)
    return self._ui

  @property
  def css(self):
    """
    Returns the set of :doc:`CSS Classes <css>` for the HTML report
    """
    return Classes.Catalog(self, {'other': set()})._class_type('other')

  @property
  def js(self):
    """
    Description:
    ------------
    Go to the Javascript section. Property to get all the JavaScript features.
    Most of the standard modules will be available in order to add event and interaction to the Js transpiled

    Usage::

      js.console.log("test")

    Related Pages:

      https://www.w3schools.com/js/default.asp

    :return: Python HTML object
    """
    if self._js is None:
      self._js = js.Js.JsBase(self)
    return self._js

  @property
  def py(self):
    """
    Description:
    ------------
    Python external module section.

    Related Pages:

      https://www.w3schools.com/js/default.asp

    :return: Python HTML object
    """
    if self._py is None:
      self._py = PyExt.PyExt(self)
    return self._py

  @property
  def data(self):
    """
    Description:
    ------------
    Python internal data source management

    This can be extended by inheriting from this epyk.core.data.DataSrc.DataSrc
    and adding extra entry points

    :return: The framework available data source
    """
    return data.Data.DataSrc(self)

  def itemFromCode(self, htmlCode):
    """
    Description:
    ------------

    :param htmlCode:

    :rtype: html.Html.Html
    """
    return self.htmlCodes[htmlCode]

  def item(self, itemId):
    """
    Description:
    ------------

    :param itemId:
    :return:
    """
    return self.htmlItems[itemId]

  def socketSend(self, htmlCode, data, report_name=None, script_name=None):
    try:
      from urllib.parse import urlparse, urlencode
      from urllib.request import urlopen, Request
      from urllib.error import HTTPError
    except ImportError:
      from urlparse import urlparse
      from urllib import urlencode
      from urllib2 import urlopen, Request, HTTPError

    urls = [htmlCode]
    if report_name or report_name is None:
      urls.append(self.run.report_name if report_name is None else report_name)
      if script_name or script_name is None:
        urls.append(self.run.script_name if script_name is None else script_name)
    response = urlopen(Request("%s%smessage/%s" % (self.run.url_root, self._urlsApp["index"].replace("/index", "/"), "/".join(urls)),
                    data=urlencode({'data': json.dumps(data)}).encode('utf-8')))
    response.read()

  @property
  def outs(self):
    """
    Description:
    ------------

    :return:
    """
    return PyOuts.PyOuts(self)

  @property
  def headers(self):
    """
    Property to the HTML page header
    """
    if self._header_obj is None:
      self._header_obj = html.Header.Header(self)
    return self._header_obj

  def export(self):
    """
    Description:
    ------------
    Static component export for Angular
    """
    ts_comps = []
    ts_comps.append(html.HtmlButton.Button(self).component.ts())
    ts_comps.append(html.HtmlButton.CheckButton(self).component.ts())
    ts_comps.append(html.HtmlText.Label(self).component.ts())
    ts_comps.append(html.HtmlText.Span(self).component.ts())
    return ts_comps

  def dumps(self, data):
    """
    Description:
    ------------
    Function used to dump the data before being sent to the Javascript layer
    This function relies on json.dumps with a special encoder in order to work with Numpy array and Pandas data structures.

    As NaN is not valid on the Json side those object are not allowed during the dump.
    It is advised to use fillna() in your script before returning the data to the framework to avoid this issue.

    Example::

      report.dumps(result)

    Related Pages:

			https://docs.python.org/2/library/json.html

    :param data: The python dictionary or data structure
    :return: The serialised data
    """
    return json.dumps(data, cls=js.JsEncoder.Encoder, allow_nan=False)
