
from epyk.core.html.graph import GraphPlotly

from epyk.core.js.packages import JsPlotly


class DataMarkersChoroMapBar(GraphPlotly.DataMarkers):

  @property
  def title(self):
    return self._attrs["title"]

  @title.setter
  def title(self, val):
    self._attrs["title"] = val

  @property
  def ticksuffix(self):
    return self._attrs["ticksuffix"]

  @ticksuffix.setter
  def ticksuffix(self, val):
    self._attrs["ticksuffix"] = val

  @property
  def showticksuffix(self):
    return self._attrs["showticksuffix"]

  @showticksuffix.setter
  def showticksuffix(self, val):
    self._attrs["showticksuffix"] = val


class DataMarkersChoroMap(GraphPlotly.DataMarkers):

  @property
  def cmax(self):
    return self._attrs["cmax"]

  @cmax.setter
  def cmax(self, val):
    self._attrs["cmax"] = val

  @property
  def cmin(self):
    return self._attrs["cmin"]

  @cmin.setter
  def cmin(self, val):
    self._attrs["cmin"] = val

  @property
  def colorscale(self):
    return self._attrs["colorscale"]

  @colorscale.setter
  def colorscale(self, val):
    self._attrs["colorscale"] = val

  @property
  def colorbar(self):
    """

    :rtype: LayoutMapBox
    """
    return self.sub_data("colorbar", DataMarkersChoroMapBar)


class LayoutCenter(GraphPlotly.Layout):

  @property
  def lat(self):
    return self._attrs["lat"]

  @lat.setter
  def lat(self, val):
    self._attrs["lat"] = val

  @property
  def lon(self):
    return self._attrs["lon"]

  @lon.setter
  def lon(self, val):
    self._attrs["lon"] = val


class LayoutMapBox(GraphPlotly.Layout):

  @property
  def style(self):
    return self._attrs["style"]

  @style.setter
  def style(self, val):
    self._attrs["style"] = val

  @property
  def zoom(self):
    return self._attrs["zoom"]

  @zoom.setter
  def zoom(self, val):
    self._attrs["zoom"] = val

  @property
  def center(self):
    """

    :rtype: LayoutCenter
    """
    return self.sub_data("center", LayoutCenter)


class LayoutGeo(GraphPlotly.Layout):

  @property
  def dragmode(self):
    return self._attrs["dragmode"]

  @dragmode.setter
  def dragmode(self, val):
    self._attrs["dragmode"] = val

  @property
  def mapboxAccessToken(self):
    return self._attrs["mapboxAccessToken"]

  @mapboxAccessToken.setter
  def mapboxAccessToken(self, val):
    self._attrs["mapboxAccessToken"] = val

  @property
  def mapbox(self):
    """

    :rtype: LayoutMapBox
    """
    return self.sub_data("mapbox", LayoutMapBox)


class LayoutGeoMapGeo(LayoutGeo):

  @property
  def scope(self):
    return self._attrs["scope"]

  @scope.setter
  def scope(self, val):
    self._attrs["scope"] = val

  @property
  def resolution(self):
    return self._attrs["resolution"]

  @resolution.setter
  def resolution(self, val):
    self._attrs["resolution"] = val

  @property
  def showlakes(self):
    return self._attrs["showlakes"]

  @showlakes.setter
  def showlakes(self, val):
    self._attrs["showlakes"] = val

  @property
  def showland(self):
    return self._attrs["showland"]

  @showland.setter
  def showland(self, val):
    self._attrs["showland"] = val

  @property
  def lakecolor(self):
    return self._attrs["lakecolor"]

  @lakecolor.setter
  def lakecolor(self, val):
    self._attrs["lakecolor"] = val

  @property
  def landcolor(self):
    return self._attrs["landcolor"]

  @landcolor.setter
  def landcolor(self, val):
    self._attrs["landcolor"] = val


class LayoutGeoMap(LayoutGeo):

  @property
  def geo(self):
    """

    :rtype: LayoutGeoMapGeo
    """
    return self.sub_data("geo", LayoutGeoMapGeo)

  @property
  def mapbox(self):
    """

    :rtype: LayoutMapBox
    """
    return self.sub_data("mapbox", LayoutMapBox)


class DataScatterMapBox(GraphPlotly.DataChart):

  @property
  def lon(self):
    return self._attrs["lon"]

  @lon.setter
  def lon(self, val):
    self._attrs["lon"] = val

  @property
  def lat(self):
    return self._attrs["lat"]

  @lat.setter
  def lat(self, val):
    self._attrs["lat"] = val


class DataChoropleth(GraphPlotly.DataChart):
  @property
  def locationmode(self):
    return self._attrs["locationmode"]

  @locationmode.setter
  def locationmode(self, val):
    self._attrs["locationmode"] = val

  @property
  def autocolorscale(self):
    return self._attrs["autocolorscale"]

  @autocolorscale.setter
  def autocolorscale(self, val):
    self._attrs["autocolorscale"] = val

  @property
  def zmin(self):
    return self._attrs["zmin"]

  @zmin.setter
  def zmin(self, val):
    self._attrs["zmin"] = val

  @property
  def zmax(self):
    return self._attrs["zmax"]

  @zmax.setter
  def zmax(self, val):
    self._attrs["zmax"] = val

  @property
  def marker(self):
    """

    https://plot.ly/javascript/bubble-maps/
    """
    return self.sub_data("marker", DataMarkersChoroMap)


class DataBubble(DataChoropleth):

  @property
  def locations(self):
    return self._attrs["locations"]

  @locations.setter
  def locations(self, val):
    self._attrs["locations"] = val


class Scatter(GraphPlotly.Chart):

  __reqJs = ['plotly.js']

  @property
  def chart(self):
    """
    :rtype: JsPlotly.Bar
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(self._report, varName=self.chartId)
    return self._chart

  @property
  def layout(self):
    """

    :rtype: LayoutGeo
    """
    if self._layout is None:
      self._layout = LayoutGeo(self._report)
    return self._layout

  @property
  def data(self):
    return self._traces[-1]

  def add_trace(self, data, type='scattermapbox', mode=None):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = type
    if mode is not None:
      c_data['mode'] = mode
    self._traces.append(DataScatterMapBox(self._report, attrs=c_data))
    return self


class Chorolet(GraphPlotly.Chart):

  __reqJs = ['plotly.js']

  @property
  def chart(self):
    """
    :rtype: JsPlotly.Bar
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(self._report, varName=self.chartId)
    return self._chart

  @property
  def layout(self):
    """

    :rtype: LayoutGeo
    """
    if self._layout is None:
      self._layout = LayoutGeo(self._report)
    return self._layout

  @property
  def data(self):
    return self._traces[-1]

  def add_trace(self, data, type='choroplethmapbox', mode=None):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = type
    if mode is not None:
      c_data['mode'] = mode
    self._traces.append(DataScatterMapBox(self._report, attrs=c_data))
    return self


class Choropleth(GraphPlotly.Chart):

  __reqJs = ['plotly.js']

  @property
  def chart(self):
    """
    :rtype: JsPlotly.Bar
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(self._report, varName=self.chartId)
    return self._chart

  @property
  def layout(self):
    """

    :rtype: LayoutGeo
    """
    if self._layout is None:
      self._layout = LayoutGeoMap(self._report)
    return self._layout

  @property
  def data(self):
    return self._traces[-1]

  def add_trace(self, data, type='choropleth', mode=None):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = type
    if mode is not None:
      c_data['mode'] = mode
    self._traces.append(DataChoropleth(self._report, attrs=c_data))
    return self


class ScatterGeo(GraphPlotly.Chart):

  __reqJs = ['plotly.js']

  @property
  def chart(self):
    """
    :rtype: JsPlotly.Bar
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(self._report, varName=self.chartId)
    return self._chart

  @property
  def layout(self):
    """

    :rtype: LayoutGeo
    """
    if self._layout is None:
      self._layout = LayoutGeoMap(self._report)
    return self._layout

  @property
  def data(self):
    return self._traces[-1]

  def add_trace(self, data, type='scattergeo', mode='markers'):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = type
    if mode is not None:
      c_data['mode'] = mode
    self._traces.append(DataChoropleth(self._report, attrs=c_data))
    return self


class BubbleGeo(GraphPlotly.Chart):

  __reqJs = ['plotly.js']

  @property
  def chart(self):
    """
    :rtype: JsPlotly.Bar
    """
    if self._chart is None:
      self._chart = JsPlotly.Pie(self._report, varName=self.chartId)
    return self._chart

  @property
  def layout(self):
    """

    :rtype: LayoutGeo
    """
    if self._layout is None:
      self._layout = LayoutGeoMap(self._report)
    return self._layout

  @property
  def data(self):
    return self._traces[-1]

  def add_trace(self, data, type='scattergeo', mode='markers'):
    c_data = dict(data)
    if type is not None:
      c_data['type'] = type
    if mode is not None:
      c_data['mode'] = mode
    self._traces.append(DataBubble(self._report, attrs=c_data))
    return self
