"""

"""

from epyk.core import html


class Forms(object):
  def __init__(self, context):
    self.context = context

  def new(self, action=None, method=None, helper=None):
    """
    Creates an new empty form

    Example
    f = rptObj.ui.form()

    :param action:
    :param method:
    :param helper:
    """
    form = html.HtmlContainer.Form(self.context.rptObj, [], action, method, helper)
    self.context.register(form)
    return form

  def date(self, action, method, htmlCode="Current", helper=None):
    """

    Example
    rptObj.ui.forms.date("http://127.0.0.1:5000", "POST")

    :param action:
    :param method:
    :param htmlCode:
    :param helper:
    """
    date = self.context.rptObj.ui.fields.today(label=htmlCode)
    date.input.set_attrs({"name": htmlCode.upper()})
    col = self.context.rptObj.ui.col([date])
    col.css({"border": '1px solid %s' % self.context.rptObj.theme.greys[4],
                                   "text-align": 'center', "width": 'none', "padding": '5px', "border-radius": '5px'})
    form = html.HtmlContainer.Form(self.context.rptObj, [col], action, method, helper)
    col += form.submit
    self.context.register(form)
    return form

  def dates(self, action, method, htmlCode1="current", htmlCode2="Previous",  helper=None):
    """

    Example
    rptObj.ui.forms.dates("http://127.0.0.1:5000", "POST")

    :param action:
    :param method:
    :param htmlCode1:
    :param htmlCode2:
    :param helper:
    """
    date1 = self.context.rptObj.ui.fields.today(label=htmlCode1)
    date1.input.set_attrs({"name": htmlCode1.upper()})
    date2 = self.context.rptObj.ui.fields.today(label=htmlCode2)
    date2.input.set_attrs({"name": htmlCode2.upper()})

    col = self.context.rptObj.ui.col([date1, date2])
    col.css({"border": '1px solid %s' % self.context.rptObj.theme.greys[4],
             "text-align": 'center', "width": 'none', "padding": '5px', "border-radius": '5px'})
    form = html.HtmlContainer.Form(self.context.rptObj, [col], action, method, helper)
    col += form.submit
    self.context.register(form)
    return form

  def input(self, htmlCode, action, method, helper=None):
    """

    :param action:
    :param method:
    :param helper:
    """
    inp = self.context.rptObj.ui.fields.input()
    inp.input.set_attrs({"name": htmlCode})
    form = html.HtmlContainer.Form(self.context.rptObj, [inp], action, method, helper)
    self.context.register(form)
    return form

  def inputs(self, records, action, method, helper=None):
    """
    Example
    rptObj.ui.forms.inputs([
      {"label": "name", "htmlCode": "input"},
      {"label": "name 2", "htmlCode": "input2"},
    ], "http://127.0.0.1:5000", "POST")

    :param records:
    :param action:
    :param method:
    :param helper:
    :return:
    """
    html_objs = []
    for rec in records:
      inp = self.context.rptObj.ui.fields.input(label=rec["label"])
      inp.input.set_attrs({"name": rec["htmlCode"]})
      html_objs.append(inp)
    col = self.context.rptObj.ui.col(html_objs).css({"border": '1px solid %s' % self.context.rptObj.theme.greys[4],
                                   "text-align": 'center', "width": 'none', "padding": '5px', "border-radius": '5px'})
    form = html.HtmlContainer.Form(self.context.rptObj, [col], action, method, helper)
    col += form.submit
    self.context.register(form)
    return form
