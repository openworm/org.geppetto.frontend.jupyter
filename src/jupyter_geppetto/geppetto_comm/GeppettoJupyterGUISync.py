"""
GeppettoJupyterGUISync.py
Component (textfield, button, checkbox, etc...) and Panel Sync 
"""
import logging
from collections import defaultdict
import ipywidgets as widgets
import json
from traitlets import (CUnicode, Unicode, Instance, List, Dict, Bool, Float, Int)

from jupyter_geppetto.geppetto_comm import GeppettoJupyterModelSync

# This is a list of all the models that are synched between Python and Javascript
synched_models = defaultdict(list)

def remove_component_sync(componentType, model):
    component_to_remove = None
    for existingModel, synched_component in list(synched_models.items()):
        if existingModel == model:
            component_to_remove = model
            break
    if(component_to_remove):
        synched_models[component_to_remove].disconnect()
        del synched_models[component_to_remove]

class ComponentSync(widgets.Widget):
    componentType = Unicode('componentType').tag(sync=True)
    model = Unicode('').tag(sync=True)
    id = Unicode('').tag(sync=True)
    value = CUnicode().tag(sync=True)

    widget_name = Unicode('').tag(sync=True)
    embedded = Bool(True).tag(sync=True)
    _model_name = Unicode('ComponentSync').tag(sync=True)
    _model_module = Unicode('jupyter_geppetto').tag(sync=True)
    
    read_only = Bool(False).tag(sync=True)
    extraData = None

    def __init__(self, **kwargs):
        super(ComponentSync, self).__init__(**kwargs)

        if 'model' in kwargs and kwargs["model"] is not None and kwargs["model"] != '':
            synched_models[kwargs["model"]] = self

        self._value_handler = widgets.CallbackDispatcher()
        #the method updateModel is executed in response to the sync_value event
        self._value_handler.register_callback(self.updateModel)

        self.on_msg(self._handle_component_msg)

    def _handle_component_msg(self, _, content, buffers):
        if content.get('event', '') == 'sync_value':
            self._value_handler(self, content)

    
    def updateModel(self, *args):
        if self.model != None and self.model != '' and args[1]['value'] != None:
            try:
                value = json.loads(args[1]['value'])
                if isinstance(value, (str, unicode)):
                    value = "'" + value + "'"
                else:
                    value = str(value)
                logging.debug("Updating model with new value " + value)
                if(args[1]['requirement']):
                    exec(args[1]['requirement'])    
                
                logging.debug("self.model = " + self.model)
                exec(self.model + "=" + value)
            except Exception as identifier:
                logging.exception("Error updating model")

    def connect(self):
        logging.debug("ComponentSync connecting to " + self.model)
        self.send({"type": "connect"})
    
    def disconnect(self):
        logging.debug("ComponentSync disconnecting from " + self.model)
        self.send({"type": "disconnect"})
        self._value_handler.register_callback(self.updateModel, remove=True)
        self.on_msg(self._handle_component_msg, remove=True)


    def __str__(self):
        return "Component Sync => Widget Name: " + self.widget_name + ", Embedded: " + str(self.embedded) + ", Sync Value: " + self.value + ", Model: " + str(self.model) + ", Extra Data: " + self.extraData


class TextFieldSync(ComponentSync):
    _model_name = Unicode('TextFieldSync').tag(sync=True)
    _model_module = Unicode('jupyter_geppetto').tag(sync=True)

    read_only = Bool(False).tag(sync=True)

    def __init__(self, **kwargs):
        super(TextFieldSync, self).__init__(**kwargs)

    def sync(self):
        self.send({"type": "sync"})


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
