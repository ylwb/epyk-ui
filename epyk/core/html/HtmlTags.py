
from epyk.core.html import Html
from epyk.core.js.html import JsHtml


class HtmlGeneric(Html.Html):
  category, name = 'Tags', 'tag'

  def __init__(self, report, tag, text, width, height, htmlCode, tooltip, options, profile):
    self.tag = tag
    super(HtmlGeneric, self).__init__(report, text, htmlCode=htmlCode, css_attrs={"width": width, "height": height}, profile=profile)
    if tooltip:
      self.tooltip(tooltip)
    if options is not None and not options.get('managed', True):
      self.inReport = False

  @property
  def dom(self):
    """
    Description:
    ------------
    Javascript Functions

    Return all the Javascript functions defined for an HTML Component.
    Those functions will use plain javascript by default.

    :return: A Javascript Dom object

    :rtype: JsHtml.JsHtmlRich
    """
    if self._dom is None:
      self._dom = JsHtml.JsHtmlRich(self, report=self._report)
    return self._dom

  @property
  def _js__builder__(self):
    return 'htmlObj.innerHTML = data'

  def __str__(self):
    return '<%s %s>%s</%s>%s' % (self.tag, self.get_attrs(pyClassNames=self.style.get_classes()), self.val, self.tag, self.helper)


class HtmlGenericLInk(HtmlGeneric):
  category, name = 'Tags', 'tag'

  def preview(self, url):
    """
    Description:
    ------------

    Attributes:
    ----------
    :param url:

    :return:
    """
    self.on('mouseenter', [
      self._report.js.request_http("test", 'GET', url).send().onSuccess([
        self._report.js.createElement("div", "popup").innerHTML(self._report.js.object("data")).attr('id', 'popup').css({
          'color': 'red', 'display': 'block', 'background': 'white', 'width': '250px', 'padding': '10px'}).position(),
        self._report.body.dom.appendChild(self._report.js.object("popup"))]
      )
    ])

    self.on('mouseleave', [self._report.js.getElementById("popup").remove()])


class HtmlComment(Html.Html):
  category, name = 'Tags', 'comment'

  def __str__(self):
    return '<!--%s-->' % self.val
