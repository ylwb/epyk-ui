
from epyk.core.html import geo


class Plotly(object):
  def __init__(self, context):
    self.parent = context
    self.chartFamily = "Plotly"

  @property
  def choropleths(self):
    return PlotlyChoropleth(self.parent)

  @property
  def bubbles(self):
    return PlotlyBubble(self.parent)

  def scattermapbox(self, record, lon_columns=None, lat_columns=None, text_columns=None, title=None, filters=None,
                    profile=None, options=None,  width=(100, "%"), height=(430, "px"), htmlCode=None):
    """

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.Scatter`

    Related Pages:

      https://plot.ly/javascript/mapbox-layers/

    :param record:
    :param lon_columns:
    :param lat_columns:
    :param text_columns:
    :param title:
    :param filters:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    series = []
    for i, l in enumerate(lon_columns):
      series.append({'lon': [], 'lat': [], 'text': []})
      for rec in record:
        series[-1]['lon'].append(rec.get(l, 0))
        series[-1]['lat'].append(rec.get(lat_columns[i], 0))
        if text_columns is not None:
          series[-1]['text'].append(rec.get(text_columns[i], 0))
    line_chart = geo.GeoPlotly.Scatter(self.parent.context.rptObj, width, height, title, options or {}, htmlCode,
                                        filters, profile)
    line_chart.options.responsive = True
    self.parent.context.register(line_chart)
    for i, s in enumerate(series):
      line_chart.add_trace(s)
      line_chart.data.marker.color = self.parent.context.rptObj.theme.colors[::-1][i]
    line_chart.layout.mapbox.style = "open-street-map"
    # line_chart.data.marker.size = 4
    # line_chart.layout.mapbox.style = "open-street-map"
    # line_chart.layout.mapbox.center.lat = 38
    # line_chart.layout.mapbox.center.lon = -90
    # line_chart.layout.dragmode = 'zoom'
    # line_chart.layout.mapbox.zoom = 3
    return line_chart

  def density(self, record, y_columns=None, x_axis=None, title=None, filters=None, profile=None, options=None,
              width=(100, "%"), height=(330, "px"), htmlCode=None):
    """

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.Scatter`

    Related Pages:

      https://plot.ly/javascript/mapbox-density-heatmaps/

    :param record:
    :param y_columns:
    :param x_axis:
    :param title:
    :param filters:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    line_chart = geo.GeoPlotly.Scatter(self.parent.context.rptObj, width, height, title, options or {}, htmlCode,
                                       filters, profile)
    line_chart.options.responsive = True
    self.parent.context.register(line_chart)
    line_chart.add_trace({"lon": [-112.8352], 'lat': [48.4113], 'z': [20], 'text': [0.0875]}, type="densitymapbox")
    line_chart.data.marker.color = "fuchsia"
    line_chart.data.marker.size = 4
    line_chart.layout.mapbox.style = "stamen-terrain"
    line_chart.layout.mapbox.center.lat = 38
    line_chart.layout.mapbox.center.lon = -90
    line_chart.layout.dragmode = 'zoom'
    line_chart.layout.zoom = 3
    return line_chart

  def chorolet(self, record, y_columns=None, x_axis=None, title=None, filters=None, profile=None, options=None,
              width=(100, "%"), height=(330, "px"), htmlCode=None):
    """

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.Chorolet`

    Related Pages:

      https://plotly.com/javascript/mapbox-county-choropleth/

    :param record:
    :param y_columns:
    :param x_axis:
    :param title:
    :param filters:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    :return:
    """
    data = {"locations": ["NY", "MA", "VT"], "z": [-50, -10, -20]}
    line_chart = geo.GeoPlotly.Chorolet(self.parent.context.rptObj, width, height, title, options or {}, htmlCode,
                                       filters, profile)
    line_chart.options.responsive = True
    self.parent.context.register(line_chart)
    data['geojson'] = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json"
    line_chart.add_trace(data)
    line_chart.layout.mapbox.center.lat = 38
    line_chart.layout.mapbox.center.lon = -90
    line_chart.layout.dragmode = 'zoom'
    line_chart.layout.zoom = 3
    return line_chart


class PlotlyBubble(object):
  def __init__(self, context):
    self.parent = context
    self.chartFamily = "Plotly"

  def bubble(self, scope, record=None, size_col=None, country_col=None, long_col=None, lat_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """
    Description:
    -----------

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.BubbleGeo`

    Related Pages:

      https://plotly.com/javascript/bubble-maps/

    Attributes:
    ----------
    :param scope:
    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    dftl_options = {'type': 'scattergeo', 'mode': 'markers'}
    if options is not None:
      dftl_options.update(options)
    map_chart = geo.GeoPlotly.BubbleGeo(self.parent.context.rptObj, width, height, dftl_options, htmlCode, profile)
    map_chart.options.responsive = True

    records = []
    if country_col is not None:
      records = self.parent.context.rptObj.data.plotly.countries(record, country_col, size_col, dftl_options.get('scale', False))
      points = ['locations']
    elif long_col is not None and lat_col is not None:
      records = self.parent.context.rptObj.data.plotly.locations(record, long_col, lat_col, size_col, dftl_options.get('scale', False))
      points = ['lon', 'lat']
    self.parent.context.register(map_chart)
    for record in records:
      map_chart.add_trace({p: record[p] for p in points})
      #map_chart.data.marker.colorbar.title = "Test"
      #map_chart.data.marker.line.color = "black"
      map_chart.data.marker.size = record['marker']['size']
      # map_chart.data.marker.cmin = 0
      # map_chart.data.marker.cmax = max(values)
      map_chart.data.marker.color = record['marker']['size']
      map_chart.data.marker.colorscale = 'Reds'
    map_chart.layout.geo.scope = scope
    map_chart.layout.geo.resolution = 150
    return map_chart

  def usa(self, record=None, size_col=None, country_col=None, long_col=None, lat_col=None, text_columns=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """
    Description:
    -----------

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.BubbleGeo`

    Related Pages:

      https://plotly.com/javascript/bubble-maps/

    Attributes:
    ----------
    :param record:
    :param size_col:
    :param long_col:
    :param lat_col:
    :param text_columns:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    map_usa = self.bubble('usa', record, size_col=size_col, country_col=country_col, long_col=long_col, lat_col=lat_col, profile=profile,
                          options=options, width=width, height=height, htmlCode=htmlCode)
    map_usa.data.locationmode = 'USA-states'
    map_usa.data.locationmode = 'usa'
    map_usa.layout.no_background()
    return map_usa

  def europe(self, record=None, size_col=None, country_col=None, long_col=None, lat_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """
    Description:
    -----------

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.BubbleGeo`

    Related Pages:

      https://plotly.com/javascript/bubble-maps/

    Attributes:
    ----------
    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    return self.bubble('europe', record, size_col=size_col, country_col=country_col, long_col=long_col, lat_col=lat_col,
                       profile=profile, options=options, width=width, height=height, htmlCode=htmlCode)

  def asia(self, record=None, size_col=None, country_col=None, long_col=None, lat_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """
    Description:
    -----------

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.BubbleGeo`

    Related Pages:

      https://plotly.com/javascript/bubble-maps/

    Attributes:
    ----------
    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    return self.bubble('asia', record, size_col=size_col, country_col=country_col, long_col=long_col, lat_col=lat_col,
                       profile=profile, options=options, width=width, height=height, htmlCode=htmlCode)

  def africa(self, record=None, size_col=None, country_col=None, long_col=None, lat_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """
    Description:
    -----------

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.BubbleGeo`

    Related Pages:

      https://plotly.com/javascript/bubble-maps/

    Attributes:
    ----------
    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    return self.bubble('africa', record, size_col=size_col, country_col=country_col, long_col=long_col, lat_col=lat_col,
                       profile=profile, options=options, width=width, height=height, htmlCode=htmlCode)

  def south_america(self, record=None, size_col=None, country_col=None, long_col=None, lat_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """
    Description:
    -----------

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.BubbleGeo`

    Related Pages:

      https://plotly.com/javascript/bubble-maps/

    Attributes:
    ----------
    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    return self.bubble('south america', record, size_col=size_col, country_col=country_col, long_col=long_col, lat_col=lat_col,
                       profile=profile, options=options, width=width, height=height, htmlCode=htmlCode)

  def north_america(self, record=None, size_col=None, country_col=None, long_col=None, lat_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """
    Description:
    -----------

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.BubbleGeo`

    Related Pages:

      https://plotly.com/javascript/bubble-maps/

    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    :return:
    """
    return self.bubble('north america', record, size_col=size_col, country_col=country_col, long_col=long_col, lat_col=lat_col,
                       profile=profile, options=options, width=width, height=height, htmlCode=htmlCode)

  def world(self, record=None, size_col=None, country_col=None, long_col=None, lat_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """
    Description:
    -----------

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.BubbleGeo`

    Related Pages:

      https://plotly.com/javascript/bubble-maps/

    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    :return:
    """
    return self.bubble('world', record, size_col=size_col, country_col=country_col, long_col=long_col, lat_col=lat_col,
                       profile=profile, options=options, width=width, height=height, htmlCode=htmlCode)


class PlotlyChoropleth(object):
  def __init__(self, context):
    self.parent = context
    self.chartFamily = "Plotly"

  def world(self, record, size_col=None, country_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.Choropleth`

    Related Pages:

      https://plotly.com/javascript/choropleth-maps/

    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    dftl_options = {'type': 'choropleth', 'mode': ''}
    if options is not None:
      dftl_options.update(options)

    records = self.parent.context.rptObj.data.plotly.choropleth(record, country_col, size_col, dftl_options.get('scale', False))
    line_chart = geo.GeoPlotly.Choropleth(self.parent.context.rptObj, width, height, dftl_options, htmlCode, profile)
    line_chart.options.responsive = True
    for record in records:
      line_chart.add_trace(record)
    self.parent.context.register(line_chart)
    return line_chart

  def europe(self, record, size_col=None, country_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.Choropleth`

    Related Pages:

      https://plotly.com/javascript/choropleth-maps/

    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    map_chart = self.world(record, size_col, country_col, profile, options, width, height, htmlCode)
    map_chart.layout.geo.scope = 'europe'
    return map_chart

  def asia(self, record, size_col=None, country_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.Choropleth`

    Related Pages:

      https://plotly.com/javascript/choropleth-maps/

    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    map_chart = self.world(record, size_col, country_col, profile, options, width, height, htmlCode)
    map_chart.layout.geo.scope = 'asia'
    return map_chart

  def africa(self, record, size_col=None, country_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.Choropleth`

    Related Pages:

      https://plotly.com/javascript/choropleth-maps/

    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    map_chart = self.world(record, size_col, country_col, profile, options, width, height, htmlCode)
    map_chart.layout.geo.scope = 'africa'
    return map_chart

  def south_america(self, record, size_col=None, country_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.Choropleth`

    Related Pages:

      https://plotly.com/javascript/choropleth-maps/

    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    map_chart = self.world(record, size_col, country_col, profile, options, width, height, htmlCode)
    map_chart.layout.geo.scope = 'south america'
    return map_chart

  def north_america(self, record, size_col=None, country_col=None, profile=None, options=None, width=(100, "%"), height=(430, "px"), htmlCode=None):
    """

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.Choropleth`

    Related Pages:

      https://plotly.com/javascript/choropleth-maps/

    :param record:
    :param size_col:
    :param country_col:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    map_chart = self.world(record, size_col, country_col, profile, options, width, height, htmlCode)
    map_chart.layout.geo.scope = 'north america'
    return map_chart

  def usa(self, record, y_column=None, x_axis=None, title=None, profile=None, options=None,
              width=(100, "%"), height=(330, "px"), htmlCode=None):
    """

    Underlying HTML Objects:

      - :class:`epyk.core.geo.GeoPlotly.Choropleth`

    Related Pages:

      https://plotly.com/javascript/choropleth-maps/

    :param record:
    :param y_column:
    :param x_axis:
    :param title:
    :param profile:
    :param options:
    :param width:
    :param height:
    :param htmlCode:
    """
    map_chart = geo.GeoPlotly.Choropleth(self.parent.context.rptObj, width, height, title, options or {}, htmlCode, profile)
    map_chart.options.responsive = True
    data = {}
    for rec in record:
      if x_axis in rec:
        data[rec[x_axis]] = data.get(x_axis, 0) + float(rec.get(y_column, 0))
    self.parent.context.register(map_chart)
    locations = list(data.keys())
    map_chart.add_trace({'locations': locations, 'z': [data[k] for k in locations]})
    map_chart.data.locationmode = 'USA-states'
    map_chart.layout.geo.scope = 'usa'
    map_chart.layout.geo.showlakes = True
    map_chart.layout.geo.showland = True
    return map_chart
