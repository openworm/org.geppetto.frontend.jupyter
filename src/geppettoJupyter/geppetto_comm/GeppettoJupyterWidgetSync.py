import ipywidgets as widgets
from traitlets import (Unicode, List, Float, Integer)

# WIDGET
class WidgetSync(widgets.Widget):
    name = Unicode('').tag(sync=True)
    widget_id = Integer(-1).tag(sync=True)
    data = List(Unicode).tag(sync=True)
    positionX = Float(-1).tag(sync=True)
    positionY = Float(-1).tag(sync=True)

    def __init__(self, **kwargs):
        super(WidgetSync, self).__init__(**kwargs)

class PlotWidgetSync(WidgetSync):
    _model_name = Unicode('PlotWidgetSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    def __init__(self, **kwargs):
        super(PlotWidgetSync, self).__init__(**kwargs)

class PopupWidgetSync(WidgetSync):
    _model_name = Unicode('PopupWidgetSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    def __init__(self, **kwargs):
        super(PopupWidgetSync, self).__init__(**kwargs)