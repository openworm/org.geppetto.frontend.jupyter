"""
GeppettoJupyterGUISync.py
Component (textfield, button, checkbox, etc...) and Panel Sync 
"""
import logging
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

    def __init__(self, **kwargs):
        super(ComponentSync, self).__init__(**kwargs)

        logging.debug('initialising component')

        if 'value' in kwargs and kwargs["value"] is not None and kwargs["value"] != '':
            sync_values[kwargs["value"]] = self

        self._click_handlers = widgets.CallbackDispatcher()
        self._change_handlers = widgets.CallbackDispatcher()
        self._blur_handlers = widgets.CallbackDispatcher()

        self.on_msg(self._handle_button_msg)

    def on_click(self, callback, remove=False):
        self._click_handlers.register_callback(callback, remove=remove)

    def on_change(self, callback, remove=False):
        self._change_handlers.register_callback(callback, remove=remove)

    def on_blur(self, callback, remove=False):
        self._blur_handlers.register_callback(callback, remove=remove)

    def _handle_button_msg(self, _, content, buffers):
        try:
            if content.get('event', '') == 'click':
                self._click_handlers(self, content)
            elif content.get('event', '') == 'change':
                self._change_handlers(self, content)
            elif content.get('event', '') == 'blur':
                self._blur_handlers(self, content)

        except Exception as exception:
            logging.exception(
                "Unexpected error executing callback for component:")
            raise

    def __str__(self):
        return "Component Sync => " + "Widget Id: " + self.widget_id + ", Widget Name: " + self.widget_name + ", Embedded: " + str(self.embedded) + ", Component Name: " + self.component_name + ", Sync Value: " + self.sync_value + ", Value: " + str(self.value) + ", Extra Data: " + self.extraData

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
