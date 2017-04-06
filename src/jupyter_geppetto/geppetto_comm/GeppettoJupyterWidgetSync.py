import ipywidgets as widgets
from traitlets import (Unicode, List, Float, Integer, Int)
from jupyter_geppetto.geppetto_comm import GeppettoJupyterModelSync
import logging

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
        self._close_handlers = widgets.CallbackDispatcher()
        self.on_msg(self._handle_widget_msg)

    def on_close(self, callback, remove=False):
        self._close_handlers.register_callback(callback, remove=remove)

    def _handle_widget_msg(self, _, content, buffers):
        if content.get('event', '') == 'close':
            self._close_handlers(self, content)

    def add_data(self, item):
        self.data = [i for i in self.data] + [item]

    def register_to_event(self, events, callback):
        GeppettoJupyterModelSync.events_controller.register_to_event(
            events, callback)

    def unregister_to_event(self, events, callback):
        GeppettoJupyterModelSync.events_controller.unregister_to_event(
            events, callback)

    def shake(self):
        self.send({"command": "shake"})

class PlotWidgetSync(WidgetSync):
    _model_name = Unicode('PlotWidgetSync').tag(sync=True)
    _model_module = Unicode('jupyter_geppetto').tag(sync=True)

    def __init__(self, **kwargs):
        super(PlotWidgetSync, self).__init__(**kwargs)

    def plot_data(self, plot_widget_data = None):
        if plot_widget_data is not None:
            self.data = plot_widget_data
        self.send({"command": "plot", "plot_mode": "plot_data"})

    def plot_XY_data(self, plot_widget_data = None):
        if plot_widget_data is not None:
            self.data = plot_widget_data
        self.send({"command": "plot", "plot_mode": "plot_XY_data"})


class PopupWidgetSync(WidgetSync):
    _model_name = Unicode('PopupWidgetSync').tag(sync=True)
    _model_module = Unicode('jupyter_geppetto').tag(sync=True)

    def __init__(self, **kwargs):
        super(PopupWidgetSync, self).__init__(**kwargs)
