from epyk.core.js import JsHtml
from epyk.core.js import JsUtils

class HtmlComp(object):
  htmlId = "test"


# ------------------------------------------------------------------------------------------------------------------
#
dom = JsHtml.JsHtml(HtmlComp())
f = JsUtils.JsFile("Dom", path=r"../outs")

f.writeJs([
  dom.hide(),
  dom.toggle()
])
f.close()