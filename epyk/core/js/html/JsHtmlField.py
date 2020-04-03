
from epyk.core.js.html import JsHtml

from epyk.core.js.primitives import JsObjects


class JsHtmlFields(JsHtml.JsHtmlRich):

  @property
  def val(self):
    """
    Description:
    -----------

    :return:
    """
    return self._src.input.dom.val

  @property
  def content(self):
    """
    Description:
    -----------

    :return:
    """
    return self._src.input.dom.content

  def empty(self):
    """
    Description:
    -----------

    :return:
    """
    return JsObjects.JsObjects.get('%s = ""' % self.content.toStr())
