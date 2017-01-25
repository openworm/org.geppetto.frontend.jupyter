import ipywidgets as widgets
from traitlets import (Unicode, List, Float, Integer, Int)
from geppettoJupyter.geppetto_comm import GeppettoJupyterModelSync

# WIDGET
class WidgetSync(widgets.Widget):
    name = Unicode('').tag(sync=True)
    widget_id = Integer(-1).tag(sync=True)
    data = List(Unicode).tag(sync=True)
    position_x = Int(-1).tag(sync=True)
    position_y = Int(-1).tag(sync=True)
    width = Int(-1).tag(sync=True)
    height = Int(-1).tag(sync=True)

    def __init__(self, **kwargs):
        super(WidgetSync, self).__init__(**kwargs)

    def add_data(self, item):
        self.data = [i for i in self.data] + [item]

    def register_to_event(self, events, callback):
        GeppettoJupyterModelSync.events_controller.register_to_event(
            events, callback)

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
        