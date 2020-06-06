
from epyk.core.data import Data
from epyk.core.data import DataPy
from epyk.core.data import DataEvent


# Shortcut data in the framework.
# All those features are available in the report object but this allow a shortcut when the context is not necessary
chartJs = DataPy.ChartJs()

plotly = DataPy.Plotly()

vis = DataPy.Vis()

nvd3 = DataPy.NVD3()

c3 = DataPy.C3()

bb = DataPy.C3()

google = DataPy.Google()

datatable = DataPy.Datatable()

events = DataEvent.DataEvents()

loops = DataEvent.DataLoops()

primitives = DataEvent.DataPrimitives()
