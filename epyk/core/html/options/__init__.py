"""

TODO: Split the component_properies class attribute into two decorators
@js_option =>  self._report._jsStyles
@html_option =>  self._attrs
"""

import sys

from epyk.core.data.DataClass import DataClass


class Options(DataClass):
  component_properties = ()

  def __init__(self, report, attrs=None, options=None):
    super(Options, self).__init__(report, attrs, options)
    self.js_type = {}
    # Set the default options for a component
    for c in self.component_properties:
      setattr(self, c, getattr(self, c))
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

  def _config_group_get(self, group, dflt=None, name=None):
    """
    Description:
    ------------
    Get second level configuration options

    Attributes:
    ----------
    :param group: String. The group attribute name
    :param name: String. The attribute name
    """
    return self._report._jsStyles.get(group, {}).get(name or sys._getframe().f_back.f_code.co_name, dflt)

  def _config_group(self, group, value, name=None):
    """
    Description:
    ------------
    Set second level configuration options

    Attributes:
    ----------
    :param group: String. The group name
    :param value: Object. The value for the name
    :param name: String. The attribute name
    """
    if not group in self._report._jsStyles:
      self._report._jsStyles[group] = {}
    self._report._jsStyles[group][name or sys._getframe().f_back.f_code.co_name] = value

  def isJsContent(self, property_name):
    """
    Description:
    ------------
    Check if the content of a property is defined to always be a JavaScript fragment.
    Thus the frameowrk will not convert it to a Json content

    Attributes:
    ----------
    :param property_name:
    """
    return self.js_type.get(property_name, False)

  @property
  def managed(self):
    """
    Description:
    ------------
    """
    return self.get(True)

  @managed.setter
  def managed(self, bool):
    self.set(bool)
    #for component in self._report.components.values():
    #  component.options.managed = bool

  def details(self):
    """
    Description:
    ------------
    Retrieve the defined properties details
    """
    prop_details = []
    for prop_name in self.component_properties:
      prop = getattr(self, prop_name)
      prop_details.append({"name": prop_name, 'value': prop, 'doc':  getattr(self.__class__, prop_name).__doc__})
    return prop_details
