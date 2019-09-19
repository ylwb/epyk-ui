"""
Module with some Python helpers for the Javascript framework
"""

import os
import re
import json
import functools

from epyk.core.js import Imports
from epyk.core.js.primitives import JsObject


#--------------------------------------------------------------------------------------------------------------
#                                                       DECORATORS
#
def fromVersion(data):
  """
  This system decorate will decorate a component function to specify during the Python execution
  if a method is not yet available in the current state of the Javascript modules.

  Example
  .fromVersion({'jqueryui': '1.12.0'})

  :param data:

  :return:
  """
  def decorator(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
      for k, v in data.items():
        if k in Imports.JS_IMPORTS:
          for mod in Imports.JS_IMPORTS[k]['modules']:
            if mod['version'] < v:
              raise Exception("Function %s can only be used from %s version %s (current %s)" % (func.__name__, k, v, mod['version']))

      return func(*args, **kwargs)

    return decorated

  return decorator

def untilVersion(data, newFeature):
  """
  This system decorate will decorate a component function to specify during the Python execution
  if a method is not available since the current state of the Javascript modules.
  Indeed as it is possible to override JS version on the fly it is also important to get notify with functions
  are not compatible anymore.
  This decorator will also propose an alternative with the new feature to.

  Example
  .untilVersion({'jqueryui': '1.12.0'}, "new function")

  :param data:
  :param newFeature:

  :return:
  """
  def decorator(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
      for k, v in data.items():
        if k in Imports.JS_IMPORTS:
          for mod in Imports.JS_IMPORTS[k]['modules']:
            if mod['version'] > v:
              raise Exception("Function %s can only be used since %s version %s (current %s). It has been replaced by %s" % (func.__name__, k, v, mod['version'], newFeature))

      return func(*args, **kwargs)
    return decorated
  return decorator


#--------------------------------------------------------------------------------------------------------------
#                                                       FUNCTIONS
#
def jsConvertData(jsData, jsFnc):
  """

  :param jsData:
  :param jsFnc:
  :return:
  """
  if not hasattr(jsData, 'varData') and not hasattr(jsData, 'fncName'):
    if hasattr(jsData, 'toStr'):
      return jsData.toStr()
    else:
      try:
        return JsObject.JsObject(json.dumps(jsData))

      except Exception as err:
        if isinstance(jsData, range):
          return JsObject.JsObject(json.dumps(list(jsData)))

        raise

  return jsData


def jsConvert(jsData, jsDataKey, isPyData, jsFnc):
  """

  :param jsData:
  :param jsDataKey:
  :param isPyData:
  :param jsFnc:

  :return:
  """
  if isPyData:
    if hasattr(jsData, 'toStr'):
      return jsData.toStr()
    else:
      try:
        return json.dumps(jsData)

      except Exception as err:
        if isinstance(jsData, range):
          return json.dumps(list(jsData))

        raise

  if jsDataKey is not None:
    jsData = "%s['%s']" % (jsData, jsDataKey)
  if jsFnc is not None:
    jsData = "%s(%s)" % (jsFnc, jsData)
  return jsData


def getJsValid(value, fail=True):
  """
  Return an error if the variable name is not valid following the Javascript naming conventions.
  Even if the function will fail it will propose a valid name to replace the one passed in input

  Example
  >>> getJsValid("test-js", False)
  'testjs'

  >>> getJsValid("234@test-js", False)
  'js234testjs'

  >>> getJsValid("234@test-js", True)
  Traceback (most recent call last):
      ...
  Exception: Javascript Variable name 234@test-js, for example you could use js234testjs instead

  Documentation
  https://www.w3schools.com/js/js_conventions.asp

  :param value: The Javascript variable name
  :param fail: Boolean to raise an exception if the name is not valid on the Javascript side
  :return: The input variable name or a suggested one
  """
  regex = re.compile('[^a-zA-Z0-9_]')
  cleanName = regex.sub('', value.strip())
  isValid = not value[0].isdigit() and cleanName == value
  if fail and not isValid:
    raise Exception("Javascript Variable name %s, for example you could use js%s instead" % (value, cleanName))

  if cleanName[0].isdigit():
    cleanName = "js%s" % cleanName
  return cleanName


def jsConvertFncs(jsFncs, isPyData=False, jsFncVal=None):
  """

  :param jsFncs:
  :param isPyData:
  :param jsFncVal:

  :return:
  """
  if not isinstance(jsFncs, list):
    jsFncs = [jsFncs]

  cnvFncs = []
  for f in jsFncs:
    if hasattr(f, 'toStr'):
      strFnc = f.toStr()
      if jsFncVal is not None:
        strFnc = strFnc.replace("trans_val", jsFncVal)
      cnvFncs.append(strFnc)
    else:
      if isPyData:
        strVal = json.dumps(f)
        if jsFncVal is not None:
          strVal = strVal.replace("trans_val", jsFncVal)
        cnvFncs.append(strVal)
      else:
        if jsFncVal is not None:
          f = str(f).replace("trans_val", jsFncVal)
        cnvFncs.append(f)
  return cnvFncs


class JsFile(object):
  def __init__(self, scriptName, path=None):
    self.scriptName, self.path = scriptName, path
    file_path = os.path.join(path, "js") # all the files will be put in a common directory
    if not os.path.exists(file_path):
      os.mkdir(file_path)
    self.outFile = open(os.path.join(file_path, "%s.js" % scriptName), "w")
    self.__data = []

  def writeJs(self, jsFncs):
    """
    Write the Javascript piece of code to the file

    Example
    dt = JsDate.new("2019-05-03")
    f.writeJs([dt,
      Js.JsConsole().log(dt.getDay()),
      Js.JsConsole().log(dt.getFullYear())])

    :param jsFncs: The Javascript fragments

    :return: The File object
    """
    self.__data.extend(jsConvertFncs(jsFncs))
    return self

  def writeReport(self, rptObj):
    """

    :param rptObj:

    :return:
    """
    pass

  def toCodePen(self):
    """
    Send the piece of Javascript to Codepen for testing

    https://codepen.io/
    """
    import webbrowser

  def close(self, jsObj=None):
    """
    Write the file and close the buffer

    :param jsObj: The internal JsObject

    """
    if jsObj is not None:
      self.outFile.write("//Javascript Prototype extensions \n\n")
      for fnc, details in jsObj._src._props.get('js', {}).get('prototypes', {}).items():
        self.outFile.write("%s = function(%s){%s};" % (fnc, ",".join(details.get('pmts', [])), details["content"]))

      self.outFile.write("\n\n//Javascript Global functions \n\n")
      for fnc, details in jsObj._src._props.get('js', {}).get('functions', {}).items():
        self.outFile.write("%s(%s)" % (fnc, ",".join(details.get('pmt', []))), details["content"])

    self.outFile.write("\n\n")
    self.outFile.write("//Javascript functions\n\n")
    self.outFile.write(";".join(self.__data))
    self.outFile.close()
    with open(r"%s\Launche_%s.html" % (self.path, self.scriptName), "w") as f:
      f.write('<html><head></head><body></body><script src="%s.js"></script></html>' % self.scriptName)
