"""

"""

import json

from epyk.core.js.primitives import JsArray
from epyk.core.js.primitives import JsObject
from epyk.core.js.primitives import JsNumber

from epyk.core.js.objects import jsText

from epyk.core.js.packages.JsCrossFilter import CrossFilter
from epyk.core.js.packages.JsVis import VisDataSet

from epyk.core.js.fncs import JsFncs


class DataLoop(object):
  """
  Data Class used for all the loop and map in the Javascript side.
  This will get the below attributes

  val   : The current value in the loop
  index : The index item
  arr   : The full array (only available in case of arrays, map, filter, every  )
  """
  val, index, arr = JsObject.JsObject("value"), JsNumber.JsNumber("index", isPyData=False), JsArray.JsArray("arr")


class DataReduce(object):
  """

  rVal  :
  val   :
  index :
  """
  rVal, val, index = JsObject.JsObject("r"), JsNumber.JsNumber("o", isPyData=False), JsNumber.JsNumber("i", isPyData=False)


class DataSort(object):
  """

  """


class DataEach(object):
  """
  Data Class for the Jquery each loop

  index : index
  data  : element
  """
  index, data = JsNumber.JsNumber("index", isPyData=False), JsObject.JsObject("data", isPyData=False)


class ContainerData(object):
  def __init__(self, report, schema):
    self._report, self._schema = report, schema

  @property
  def f(self):
    return JsFncs.FncOnRecords(self._report._props, self._schema)


class RawData(object):
  def __init__(self, report, records=None, profile=False):
    self._report, self._data_id = report, id(records)
    if "data" not in self._report._props:
      self._report._props["data"] = {"sources": {}, "schema": {}}
    self._report._props["data"]["sources"][self._data_id] = records
    self._report._props["data"]["schema"][self._data_id] = {'fncs': [], "profile": profile}
    self._data = self._report._props["data"]["sources"][self._data_id]
    self._schema = self._report._props["data"]["schema"][self._data_id]

  @classmethod
  def get(cls, report, varName):
    """
    Return the internal RawData object

    :return: A internal data object
    """
    return RawData(report, None)

  def setId(self, jqId):
    """
    Change the Id variable name for the javascript data source.

    Example

    :param jqId:

    :return: The Python object
    """
    self.jqId = jqId if jqId is not None else self._jqId
    return self

  def attach(self, html_obj, profile=False):
    """
    Attach the data object to a HTML Object.

    This function is automatically used in the different components in order
    to guarantee the link of the data. This will also ensure that the same data set will be store only once in the page

    Example

    :param html_obj:
    :param profile:

    """
    self._data["schema"][self._data_id].setdefault('containers', {})[html_obj.htmlId] = {'fncs': [], 'outs': None, "profile": profile}
    return ContainerData(self._report, self._data["schema"][self._data_id]['containers'][html_obj.htmlId])

  def toTsv(self, process='input'):
    """

    :return: A String with the Javascript function to be used
    """
    self._report.jsGlobal.fnc("ToTsv(data, colNames)", "%s; return result" % jsText.JsTextTsv().value)
    return "ToTsv(%s, %s)" % (self.jqId, json.dumps(list(self._schema['keys'] | self._schema['values'])))

  @property
  def f(self):
    return JsFncs.FncOnRecords(self._report._props, self._schema)

  def toStr(self):
    data = "data_%s" % self._data_id
    for fnc in self._schema.get('fncs', []):
      data = fnc % data
    return data


class JsData(object):

  def __init__(self, src):
    self._src = src

  def loop(self):
    return DataLoop()

  def reduce(self):
    return DataReduce()

  def sort(self):
    return DataSort()

  def each(self):
    return DataEach()

  def crossfilter(self, data, var_name):
    """

    :param data:

    :return:
    """
    return CrossFilter(self._src, varName=var_name, data=data)

  def dataset(self, data):
    """

    :param data:

    :return:
    """
    return VisDataSet(self._src, data)

  def records(self, data):
    """

    :param data:

    :return:
    """
    return RawData(self._src, data)
