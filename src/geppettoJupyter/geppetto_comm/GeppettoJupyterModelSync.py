from collections import defaultdict
import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Float)

# Current variables
record_variables = defaultdict(list)
current_project = None
current_experiment = None
current_model = None

class EventsSync(widgets.Widget):
    _model_name = Unicode('EventsSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)
    _events = {
        'Select': 'experiment:selection_changed'
    }
    _eventsCallbacks = {}

    def __init__(self, **kwargs):
        super(EventsSync, self).__init__(**kwargs)

        self.on_msg(self._handle_event)

    def _handle_event(self, _, content, buffers):
        if content.get('event', '') == self._events['Select']:
            self.log.warn("Event triggered")
            self.log.warn(self._events['Select'])
            self.log.warn(self._eventsCallbacks)
            for callback in self._eventsCallbacks[self._events['Select']]:
                self.log.warn("Executing method")
                self.log.warn(callback)
                try:
                    callback(content.get('data', ''))
                except Exception as e:
                    self.log.warn("Unexpected error:")
                    self.log.warn(str(e))
                    raise

    def registerToEvent(self, events, callback):
        #FIXME we should allow to add callback not only init
        for event in events:
            self._eventsCallbacks[event] = [callback]

events_controller = EventsSync()


class ExperimentSync(widgets.Widget):
    _model_name = Unicode('ExperimentSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    name = Unicode('').tag(sync=True)
    id = Unicode('').tag(sync=True)
    lastModified = Unicode('').tag(sync=True)
    state = Unicode('').tag(sync=True)

    def __init__(self, **kwargs):
        super(ExperimentSync, self).__init__(**kwargs)


class ProjectSync(widgets.Widget):
    _model_name = Unicode('ProjectSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)
    experiments = List(Instance(ExperimentSync)).tag(
        sync=True, **widgets.widget_serialization)

    def __init__(self, **kwargs):
        super(ProjectSync, self).__init__(**kwargs)

    def addExperiment(self, experiment):
        self.experiments = [i for i in self.experiments] + [experiment]


class StateVariableSync(widgets.Widget):
    _model_name = Unicode('StateVariableSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)
    units = Unicode('').tag(sync=True)
    timeSeries = List(Float).tag(sync=True)

    neuron_variable = None

    def __init__(self, **kwargs):
        super(StateVariableSync, self).__init__(**kwargs)

        # Add it to the syncvalues
        if 'neuron_variable' in kwargs and kwargs["neuron_variable"] is not None:
            record_variables[kwargs["neuron_variable"]] = self


class GeometrySync(widgets.Widget):
    _model_name = Unicode('GeometrySync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)

    bottomRadius = Float(-1).tag(sync=True)
    topRadius = Float(-1).tag(sync=True)
    positionX = Float(-1).tag(sync=True)
    positionY = Float(-1).tag(sync=True)
    positionZ = Float(-1).tag(sync=True)
    distalX = Float(-1).tag(sync=True)
    distalY = Float(-1).tag(sync=True)
    distalZ = Float(-1).tag(sync=True)

    def __init__(self, **kwargs):
        super(GeometrySync, self).__init__(**kwargs)


class ModelSync(widgets.Widget):
    _model_name = Unicode('ModelSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)
    stateVariables = List(Instance(StateVariableSync)).tag(
        sync=True, **widgets.widget_serialization)
    geometries = List(Instance(GeometrySync)).tag(
        sync=True, **widgets.widget_serialization)

    def __init__(self, **kwargs):
        super(ModelSync, self).__init__(**kwargs)

    def addStateVariable(self, stateVariable):
        self.stateVariables = [
            i for i in self.stateVariables] + [stateVariable]

    def addGeometries(self, geometries):
        self.geometries = [i for i in self.geometries] + geometries
