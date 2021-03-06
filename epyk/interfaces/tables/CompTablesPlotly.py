
from epyk.core.html import tables as html_tables


class Plotly(object):
  def __init__(self, context):
    self.parent = context

  def table(self, records, cols=None, rows=None, header=None, width=(100, '%'), height=(None, 'px'), htmlCode=None, options=None, profile=None):
    """
    Description:
    ------------

    Usage::

      Related Pages:

      https://plot.ly/javascript/table-subplots/

    Attributes:
    ----------
    :param records:
    :param cols:
    :param rows:
    :param header:
    :param width:
    :param height:
    :param htmlCode:
    :param options:
    :param profile: 
    """
    data_rows, _header = [], []
    cols = cols or []
    rows = rows or []
    if len(records) > 0 and not cols and not rows:
      cols = list(records[0].keys())
    for r in rows:
      data_rows.append([])
      _header.append(r)
    data_cols = []
    for r in cols:
      data_cols.append([])
      _header.append(r)
    for rec in records:
      for i, r in enumerate(rows):
        data_rows[i].append(rec.get(r, ''))
      for i, r in enumerate(cols):
        data_cols[i].append(rec.get(r, ''))

    header = header or _header
    options = options or {}
    options.update({'type': 'table', 'mode': ''})
    h_table = html_tables.HtmlTablePlotly.Table(self.parent.context.rptObj, width, height, options, htmlCode, profile)
    h_table.add_trace(data_rows + data_cols)
    h_table.options.responsive = True
    h_table.data.header.values = [[h] for h in header]
    h_table.layout.no_background()
    return h_table
