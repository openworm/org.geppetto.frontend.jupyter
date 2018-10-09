"""
GeppettoJupyterSync.py
Component, Model, Project, Experiment, Event
"""
import logging
from collections import defaultdict
import ipywidgets as widgets
import json
from traitlets import (CUnicode, Unicode, Instance, List, Dict, Bool, Float, Int)


# This is a list of all the models that are synched between Python and Javascript
synched_models = defaultdict(list)
events_controller = None

context = None

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
                if isinstance(value, str):
                    value = "'" + value + "'"
                else:
                    value = str(value)
                logging.debug("Updating model with new value " + value)

                context_path = next(iter(context))
                if(context_path and context_path!=""):
                    logging.debug("self.model = " + context_path+"."+self.model)
                    exec(context_path+"."+self.model + "=" + value, context)
                else:
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

class EventsSync(widgets.Widget):
    _model_name = Unicode('EventsSync').tag(sync=True)
    _model_module = Unicode('jupyter_geppetto').tag(sync=True)
    _model_module_version = Unicode('~1.0.0')
    _events = {
        'Select': 'experiment:selection_changed',
        'Instances_created': "instances:created",
        'Global_message': 'Global_message'
    }
    _eventsCallbacks = {}

    def __init__(self, **kwargs):
        logging.debug("Event sync initialized")
        super(EventsSync, self).__init__(**kwargs)

        self.on_msg(self._handle_event)

    def _handle_event(self, _, content, buffers):
        logging.debug("Event received")
        if content.get('event', '') == self._events['Select']:
            logging.debug("Select Event triggered")
            if self._events['Select'] in self._eventsCallbacks:
                for callback in self._eventsCallbacks[self._events['Select']]:
                    try:
                        callback(content.get('data', ''),
                                content.get('geometryIdentifier', ''),
                                content.get('point', ''))
                    except Exception as e:
                        logging.exception(
                            "Unexpected error executing callback on select event triggered:")
                        raise
        elif content.get('event', '') == self._events['Instances_created']:
            logging.debug("Instances_created Event triggered")
            if self._events['Instances_created'] in self._eventsCallbacks:
                for callback in self._eventsCallbacks[self._events['Instances_created']]:
                    try:
                        callback(content.get('data', ''))
                    except Exception as e:
                        logging.exception(
                            "Unexpected error executing callback on instances_created event triggered:")
                        raise
        elif content.get('event', '') == self._events['Global_message']:
            logging.debug("Global message")
            if self._events['Global_message'] in self._eventsCallbacks:
                for callback in self._eventsCallbacks[self._events['Global_message']]:
                    try:
                        callback(content.get('id', ''), content.get('command', ''), content.get('parameters', ''))
                    except Exception as e:
                        logging.exception( "Unexpected error executing callback on Global_message event triggered:")
                        raise
        

    def register_to_event(self, events, callback):
        for event in events:
            if event not in self._eventsCallbacks:
                self._eventsCallbacks[event] = []
            self._eventsCallbacks[event].append(callback)
            logging.debug("Registring event " + str(event) +
                          " with callback " + str(callback))

    def unregister_to_event(self, events, callback):
        for event in events:
            self._eventsCallbacks[event].remove(callback)
            logging.debug("Unregistring event " + str(event) +
                          " with callback " + str(callback))

    def triggerEvent(self, event, options={}):
        self.send({"event": event, "options": options})

