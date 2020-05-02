

from epyk.core import html


class Steppers(object):

  def __init__(self, context):
    self.context = context

  def stepper(self, records, width=(100, '%'), height=(70, 'px'), color=None, options=None):
    """
    Description:

    Entry point for the stepper object

    Usage::

      rptObj.ui.stepper([
        {"value": 'test 1', "status": 'success', 'label': 'test'},
        {"value": 'test 2', "status": 'error'},
        {"value": 'test 3', "status": 'pending'}])

    Attributes:
    ----------
    :param records: A list with the different steps defined in the workflow
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param color: Optional.
    :param options: Optional. Specific Python options available for this component
    """
    dft_options = {"line": True}
    if options is not None:
      dft_options.update(options)
    st = html.HtmlStepper.Stepper(self.context.rptObj, records, width, height, color, dft_options)
    self.context.register(st)
    return st

  def arrow(self, records, width=(100, '%'), height=(70, 'px'), color=None, options=None):
    dft_options = {"shape": 'arrow'}
    if options is not None:
      dft_options.update(options)
    self.stepper(records, width, height, color, dft_options)

  def rectangle(self, records, width=(100, '%'), height=(70, 'px'), color=None, options=None):
    dft_options = {"shape": 'rectangle'}
    if options is not None:
      dft_options.update(options)
    self.stepper(records, width, height, color, dft_options)

  def triangle(self, records, width=(100, '%'), height=(70, 'px'), color=None, options=None):
    dft_options = {"shape": 'rectangle'}
    if options is not None:
      dft_options.update(options)
    self.stepper(records, width, height, color, dft_options)

  def vertical(self, records, width=(100, '%'), height=(70, 'px'), color=None, options=None):
    """
    Description:

    Entry point for the stepper object

    Usage::

      rptObj.ui.stepper([
        {"value": 'test 1', "status": 'success', 'label': 'test'},
        {"value": 'test 2', "status": 'error'},
        {"value": 'test 3', "status": 'pending'}])

    Attributes:
    ----------
    :param records: A list with the different steps defined in the workflow
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param color: Optional.
    :param options: Optional. Specific Python options available for this component
    """
    dft_options = {"line": False}
    if options is not None:
      dft_options.update(options)
    st = html.HtmlStepper.Stepper(self.context.rptObj, records, width, height, color, options or {})
    self.context.register(st)
    return st
