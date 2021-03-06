#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core.js import JsUtils
from epyk.core.js.primitives import JsObjects


class JsSwitch(object):
  """
    Description:
    ------------

  Documentation:
    - https://www.w3schools.com/js/js_switch.asp

  """

  def __init__(self, variable):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param variable:
    """
    self.__selector = variable
    self.__js, self.__default = [], None

  def case(self, value, jsFncs, strict=False):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param value: Object. The pivot value
    :param jsFncs: List or String. The JavaScript functions
    :param strict: Boolean.
    """
    if strict:
      self.__js.append((JsObjects.JsVoid("(%s === %s)" % (self.__selector, value)), jsFncs))
    else:
      self.__js.append((JsObjects.JsVoid("(%s == %s)" % (self.__selector, value)), jsFncs))
    return self

  def caseRange(self, min, max, jsFncs, include_value=True):
    """
    Description:
    ------------
    Range case. The value should be within the range [min, max]

    Attributes:
    ----------
    :param max: Number. The min value for this range
    :param min:  Number. The max value for this range
    :param jsFncs: List or String. The JavaScript functions
    :param include_value: Boolean. To specify if the pivot value is included
    """
    max = JsUtils.jsConvertData(max, None)
    min = JsUtils.jsConvertData(min, None)
    if include_value:
      self.__js.append((JsObjects.JsVoid("(%s <= %s) && (%s <= %s)" % (min, self.__selector, self.__selector, max)), jsFncs))
    else:
      self.__js.append((JsObjects.JsVoid("(%s < %s) && (%s < %s)" % (min, self.__selector, self.__selector, max)), jsFncs))
    return self

  def caseBelow(self, value, jsFncs, include_value=True):
    """
    Description:
    ------------
    Below case. The switch value should be below the value.

    Attributes:
    ----------
    :param value: Number. The pivot value
    :param jsFncs: List or String. The JavaScript functions
    :param include_value: Boolean. To specify if the pivot value is included
    """
    value = JsUtils.jsConvertData(value, None)
    if include_value:
      self.__js.append((JsObjects.JsVoid("(%s <= %s)" % (self.__selector, value)), jsFncs))
    else:
      self.__js.append((JsObjects.JsVoid("(%s < %s)" % (self.__selector, value)), jsFncs))
    return self

  def caseAbove(self, value, jsFncs, include_value=True):
    """
    Description:
    ------------
    Above case. The switch value should be above the value.

    Attributes:
    ----------
    :param value: Number. The pivot value
    :param jsFncs: List or String. The JavaScript functions
    :param include_value: Boolean. To specify if the pivot value is included
    """
    value = JsUtils.jsConvertData(value, None)
    if include_value:
      self.__js.append((JsObjects.JsVoid("(%s >= %s)" % (self.__selector, value)), jsFncs))
    else:
      self.__js.append((JsObjects.JsVoid("(%s > %s)" % (self.__selector, value)), jsFncs))
    return self

  def default_(self, jsFncs):
    """
    Description:
    ------------
    Default case value

    Attributes:
    ----------
    :param jsFncs: List or String. The JavaScript functions
    """
    self.__default = jsFncs
    return self

  def toStr(self):
    strData = []
    for var, jsFncs in self.__js:
      strData.append("case %s: {%s; break}" % (JsUtils.jsConvertData(var, None), JsUtils.jsConvertFncs(jsFncs, toStr=True)))
    if self.__default is not None:
      strData.append("default: {%s}" % JsUtils.jsConvertFncs(self.__default, toStr=True))
    self.__jsFncs, self.__default = [], None # empty the stack
    return "switch (true){%s}" % ("".join(strData))

  def __str__(self):
    return self.toStr()
