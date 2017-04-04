"""
GeppettoJupyterGUISync.py
Component (textfield, button, checkbox, etc...) and Panel Sync 
"""
import logging
from collections import defaultdict
import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Dict, Bool, Float, Int)

from jupyter_geppetto.geppetto_comm import GeppettoJupyterModelSync

# Current variables
sync_values = defaultdict(list)


class ComponentSync(widgets.Widget):
    widget_id = Unicode('').tag(sync=True)
    widget_name = Unicode('').tag(sync=True)
    embedded = Bool(True).tag(sync=True)

    sync_value = Unicode().tag(sync=True)
    value = None
    extraData = None

    def __init__(self, **kwargs):
        super(ComponentSync, self).__init__(**kwargs)

        if 'value' in kwargs and kwargs["value"] is not None and kwargs["value"] != '':
            sync_values[kwargs["value"]] = self

        self._change_handlers = widgets.CallbackDispatcher()
        self._blur_handlers = widgets.CallbackDispatcher()

        self.on_msg(self._handle_component_msg)

    def on_change(self, callback, remove=False):
        self._change_handlers.register_callback(callback, remove=remove)

    def on_blur(self, callback, remove=False):
        self._blur_handlers.register_callback(callback, remove=remove)

    def _handle_component_msg(self, _, content, buffers):
        if content.get('event', '') == 'change':
            self._change_handlers(self, content)
        elif content.get('event', '') == 'blur':
            self._blur_handlers(self, content)

    def __str__(self):
        return "Component Sync => " + "Widget Id: " + self.widget_id + ", Widget Name: " + self.widget_name + ", Embedded: " + str(self.embedded) + ", Sync Value: " + self.sync_value + ", Value: " + str(self.value) + ", Extra Data: " + self.extraData


class TextFieldSync(ComponentSync):
    _model_name = Unicode('TextFieldSync').tag(sync=True)
    _model_module = Unicode('jupyter_geppetto').tag(sync=True)

    read_only = Bool(False).tag(sync=True)

    def __init__(self, **kwargs):
        super(TextFieldSync, self).__init__(**kwargs)


class CheckboxSync(ComponentSync):
    _model_name = Unicode('CheckboxSync').tag(sync=True)
    _model_module = Unicode('jupyter_geppetto').tag(sync=True)

    def __init__(self, **kwargs):
        super(CheckboxSync, self).__init__(**kwargs)


class ButtonSync(ComponentSync):
    _model_name = Unicode('ButtonSync').tag(sync=True)
    _model_module = Unicode('jupyter_geppetto').tag(sync=True)

    def __init__(self, **kwargs):
        super(ButtonSync, self).__init__(**kwargs)
        self._click_handlers = widgets.CallbackDispatcher()
        self.on_msg(self._handle_button_msg)

    def on_click(self, callback, remove=False):
        self._click_handlers.register_callback(callback, remove=remove)

    def _handle_button_msg(self, _, content, buffers):
        super(ButtonSync, self)._handle_component_msg(_, content, buffers)
        if content.get('event', '') == 'click':
            self._click_handlers(self, content)

class LabelSync(ComponentSync):
    _model_name = Unicode('LabelSync').tag(sync=True)
    _model_module = Unicode('jupyter_geppetto').tag(sync=True)

    def __init__(self, **kwargs):
        super(LabelSync, self).__init__(**kwargs)

class DropDownSync(ComponentSync):
    _model_name = Unicode('DropDownSync').tag(sync=True)
    _model_module = Unicode('jupyter_geppetto').tag(sync=True)

    items = List(Dict).tag(sync=True)

    def __init__(self, **kwargs):
        super(DropDownSync, self).__init__(**kwargs)

    def add_child(self, child):
        self.items = [i for i in self.items] + [child]

class PanelSync(ComponentSync):
    _model_name = Unicode('PanelSync').tag(sync=True)
    _model_module = Unicode('jupyter_geppetto').tag(sync=True)

    items = List(Instance(widgets.Widget)).tag(
        sync=True, **widgets.widget_serialization)
    parentStyle = Dict({'flexDirection': 'column'}).tag(sync=True)
    position_x = Int(-1).tag(sync=True)
    position_y = Int(-1).tag(sync=True)
    width = Int(-1).tag(sync=True)
    height = Int(-1).tag(sync=True)
    properties = Dict({'closable':True}).tag(sync=True)

    def __init__(self, **kwargs):
        super(PanelSync, self).__init__(**kwargs)
        self._close_handlers = widgets.CallbackDispatcher()
        self.on_msg(self._handle_panel_msg)

    def on_close(self, callback, remove=False):
        self._close_handlers.register_callback(callback, remove=remove)

    def _handle_panel_msg(self, _, content, buffers):
        super(PanelSync, self)._handle_component_msg(_, content, buffers)
        if content.get('event', '') == 'close':
            self._close_handlers(self, content)


    def add_child(self, child):
        child.embedded = True
        self.items = [i for i in self.items] + [child]

    def setDirection(self, direction):
        self.parentStyle = {'flexDirection': direction}

    def register_to_event(self, events, callback):
        GeppettoJupyterModelSync.events_controller.register_to_event(
            events, callback)

    def unregister_to_event(self, events, callback):
        GeppettoJupyterModelSync.events_controller.unregister_to_event(
            events, callback)

    def display(self):
        self.send({"type": "display"})

    def shake(self):
        self.send({"type": "shake"})
