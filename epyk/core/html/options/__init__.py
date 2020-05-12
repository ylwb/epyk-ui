"""

TODO: Split the component_properies class attribute into two decorators
@js_option =>  self._report._jsStyles
@html_option =>  self._attrs
"""

import sys

from epyk.core.data import DataClass


class Options(DataClass):
  component_properies = ()

  def __init__(self, report, attrs=None, options=None):
    super(Options, self).__init__(report, attrs, options)
    if attrs is not None:
      for k, v in attrs.items():
        if hasattr(self, k):
          setattr(self, k, v)
        else:
          self._report._jsStyles[k] = v

  def _config_get(self, dflt=None, name=None):
    """
    Description:
    ------------
    Get the option attribute to be added on the Javascript side during the component build

    Attributes:
    ----------
    :param name: String. The attribute name
    """
    return self._report._jsStyles.get(name or sys._getframe().f_back.f_code.co_name, dflt)

  def _config(self, value, name=None):
    """
    Description:
    ------------
    Set the option attribute to be added on the Javascript side during the component build

    Attributes:
    ----------
    :param value: Object. The value for the name
    :param name: String. The attribute name
    """
    self._report._jsStyles[name or sys._getframe().f_back.f_code.co_name] = value

  def details(self):
    """
    Description:
    ------------
    Retrieve the defined properties details
    """
    prop_details = []
    for prop_name in self.component_properies:
      prop = getattr(self, prop_name)
      prop_details.append({"name": prop_name, 'value': prop, 'doc':  getattr(self.__class__, prop_name).__doc__})
    return prop_details
