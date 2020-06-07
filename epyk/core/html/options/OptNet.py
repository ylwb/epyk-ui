

from epyk.core.html.options import Options
from epyk.core.js.packages import packageImport


class OptionsNews(Options):

  @property
  def dated(self):
    """
    Description:
    ------------
    Check default value for radio and check lists
    """
    return self._config_get(True)

  @dated.setter
  def dated(self, bool):
    if bool:
      self._report.jsImports.add('moment')
    self._config(bool)

  @property
  def classes(self):
    """
    Description:
    ------------
    Check default value for radio and check lists
    """
    return self._config_get([])

  @classes.setter
  def classes(self, class_names):
    self._config(class_names)

  @property
  def markdown(self):
    """
    Description:
    ------------
    Showdown is a Javascript Markdown to HTML converter, based on the original works by John Gruber.
    Showdown can be used client side (in the browser) or server side (with NodeJs).

    Related Pages:

      https://github.com/showdownjs/showdown
    """
    return self._config_get(False, 'showdown')

  @markdown.setter
  @packageImport("showdown")
  def markdown(self, values):
    values = {} if values is True else values
    self._config(values, 'showdown')


class OptionsAlert(Options):

  @property
  def time(self):
    """
    Description:
    ------------
    """
    return self._config_get(1000)

  @time.setter
  def time(self, attrs):
    self._config(attrs)

  @property
  def delay(self):
    """
    Description:
    ------------
    """
    return self._config_get(1000)

  @delay.setter
  def delay(self, attrs):
    self._config(attrs)

  @property
  def close(self):
    """
    Description:
    ------------
    """
    return self._config_get(True)

  @close.setter
  def close(self, bool):
    self._config(bool)

  @property
  def type(self):
    """
    Description:
    ------------
    """
    return self._config_get(None)

  @type.setter
  def type(self, value):
    self._config(value)

  @property
  def markdown(self):
    """
    Description:
    ------------
    Showdown is a Javascript Markdown to HTML converter, based on the original works by John Gruber.
    Showdown can be used client side (in the browser) or server side (with NodeJs).

    Related Pages:

      https://github.com/showdownjs/showdown
    """
    return self._config_get(False, 'showdown')

  @markdown.setter
  @packageImport("showdown")
  def markdown(self, values):
    values = {} if values is True else values
    self._config(values, 'showdown')


class OptionsChat(Options):

  @property
  def dated(self):
    """
    Description:
    ------------
    Check default value for radio and check lists
    """
    return self._config_get(True)

  @dated.setter
  def dated(self, bool):
    if bool:
      self._report.jsImports.add('moment')
    self._config(bool)

  @property
  def readonly(self):
    """
    Description:
    ------------
    Check default value for radio and check lists
    """
    return self._config_get(True)

  @readonly.setter
  def readonly(self, bool):
    self._config(bool)

  @property
  def markdown(self):
    """
    Description:
    ------------
    Showdown is a Javascript Markdown to HTML converter, based on the original works by John Gruber.
    Showdown can be used client side (in the browser) or server side (with NodeJs).

    Related Pages:

      https://github.com/showdownjs/showdown
    """
    return self._config_get(False, 'showdown')

  @markdown.setter
  @packageImport("showdown")
  def markdown(self, values):
    values = {} if values is True else values
    self._config(values, 'showdown')