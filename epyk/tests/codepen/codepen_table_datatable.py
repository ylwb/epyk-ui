from epyk.core.Page import Report
from epyk.tests import test_statics

rptObj = Report()

data = [{"A": 1, "B": 2}]
table = rptObj.ui.tables.datatables.table(data, cols=["A"], rows=["B"])

table.dom.addOnReady(
  [
    table.dom.addClass("red", {"border": "1px solid green"}, extend=False)
  ]
)
rptObj.outs.browser.codepen(path=test_statics.OUTPUT_PATHS, open_browser=True)
