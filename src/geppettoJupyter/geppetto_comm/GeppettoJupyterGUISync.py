"""
GeppettoJupyterGUISync.py
Component (textfield, button, checkbox, etc...) and Panel Sync 
"""
from collections import defaultdict
import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Dict, Bool, Float)

from geppettoJupyter.geppetto_comm import GeppettoJupyterModelSync

# Current variables
sync_values = defaultdict(list)

class ComponentSync(widgets.Widget):
    _model_name = Unicode('ComponentSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    widget_id = Unicode('').tag(sync=True)
    widget_name = Unicode('').tag(sync=True)
    embedded = Bool(True).tag(sync=True)

    component_name = Unicode('').tag(sync=True)

    sync_value = Unicode().tag(sync=True)
    value = None
    extraData = None

    clickCallbacks = []
    changeCallbacks = []
    blurCallbacks = []

    def __init__(self, **kwargs):
        super(ComponentSync, self).__init__(**kwargs)

        if 'value' in kwargs and kwargs["value"] is not None:
            sync_values[kwargs["value"]] = self

        self._click_handlers = widgets.CallbackDispatcher()
        self._change_handlers = widgets.CallbackDispatcher()
        self._blur_handlers = widgets.CallbackDispatcher()

        self.on_msg(self._handle_button_msg)

    def fireChangeCallbacks(self, *args, **kwargs):
        self.fireCallbacks(self.changeCallbacks, args)

    def fireClickCallbacks(self, *args, **kwargs):
        self.fireCallbacks(self.clickCallbacks, args)

    def fireBlurCallbacks(self, *args, **kwargs):
        self.fireCallbacks(self.blurCallbacks, args)

    def fireCallbacks(self, cbs, args):
        try:
            cbs(self, args)
        except Exception as exception:
            self.log.exception("Unexpected error executing callback for component:")
            raise

    def on_click(self, callbacks, remove=False):
        self.clickCallbacks = callbacks
        self._click_handlers.register_callback(
            self.fireClickCallbacks, remove=remove)

    def on_change(self, callbacks, remove=False):
        self.changeCallbacks = callbacks
        self._change_handlers.register_callback(
            self.fireChangeCallbacks, remove=remove)

    def on_blur(self, callbacks, remove=False):
        self.blurCallbacks = callbacks
        self._blur_handlers.register_callback(
            self.fireBlurCallbacks, remove=remove)

    def _handle_button_msg(self, _, content, buffers):
        if content.get('event', '') == 'click':
            self._click_handlers(self, content)
        elif content.get('event', '') == 'change':
            self._change_handlers(self, content)
        elif content.get('event', '') == 'blur':
            self._blur_handlers(self, content)

# PANEL
class PanelSync(widgets.Widget):
    _model_name = Unicode('PanelSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    widget_id = Unicode('').tag(sync=True)
    widget_name = Unicode('').tag(sync=True)

    items = List(Instance(widgets.Widget)).tag(
        sync=True, **widgets.widget_serialization)
    parentStyle = Dict({'flexDirection': 'column'}).tag(sync=True)
    embedded = Bool(False).tag(sync=True)
    positionX = Float(-1).tag(sync=True)
    positionY = Float(-1).tag(sync=True)

    def __init__(self, **kwargs):
        super(PanelSync, self).__init__(**kwargs)
        self._click_handlers = widgets.CallbackDispatcher()
        self.on_msg(self._handle_income_msg)

    def on_click(self, callback, remove=False):
        self._click_handlers.register_callback(callback, remove=remove)

    def _handle_income_msg(self, _, content, buffers):
        if content.get('event', '') == 'click':
            self._click_handlers(self)

    def addChild(self, child):
        child.embedded = True
        self.items = [i for i in self.items] + [child]

    def setDirection(self, direction):
        self.parentStyle = {'flexDirection': direction}

    def registerToEvent(self, events, callback):
        GeppettoJupyterModelSync.events_controller.registerToEvent(
            events, callback)

    def display(self):
        self.send({"type": "display"})
