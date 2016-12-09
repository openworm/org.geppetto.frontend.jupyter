import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Dict, Bool, Float, Integer)
from collections import defaultdict

from neuron import h
h.load_file("stdrun.hoc")

# Current variables
sync_values = defaultdict(list)
record_variables = defaultdict(list)
current_project = None
current_experiment = None
current_model = None

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
    _model_module = Unicode('geppettoWidgets').tag(sync=True)

    def __init__(self, **kwargs):
        super(PlotWidgetSync, self).__init__(**kwargs)

# EXPERIMENT
class ExperimentSync(widgets.Widget):
    _model_name = Unicode('ExperimentSync').tag(sync=True)
    _model_module = Unicode('geppettoWidgets').tag(sync=True)

    name = Unicode('').tag(sync=True)
    id = Unicode('').tag(sync=True)
    lastModified = Unicode('').tag(sync=True)
    state = Unicode('').tag(sync=True)

    def __init__(self, **kwargs):
        super(ExperimentSync, self).__init__(**kwargs)

# PROJECT
class ProjectSync(widgets.Widget):
    _model_name = Unicode('ProjectSync').tag(sync=True)
    _model_module = Unicode('geppettoWidgets').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)
    experiments = List(Instance(ExperimentSync)).tag(sync=True, **widgets.widget_serialization)

    def __init__(self, **kwargs):
        super(ProjectSync, self).__init__(**kwargs)

    def addExperiment(self, experiment):
        self.experiments = [i for i in self.experiments] + [experiment]

# STATE VARIABLE
class StateVariableSync(widgets.Widget):
    _model_name = Unicode('StateVariableSync').tag(sync=True)
    _model_module = Unicode('geppettoWidgets').tag(sync=True)

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
    _model_module = Unicode('geppettoWidgets').tag(sync=True)

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

# MODEL
class ModelSync(widgets.Widget):
    _model_name = Unicode('ModelSync').tag(sync=True)
    _model_module = Unicode('geppettoWidgets').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)
    stateVariables = List(Instance(StateVariableSync)).tag(sync=True, **widgets.widget_serialization)
    geometries = List(Instance(GeometrySync)).tag(sync=True, **widgets.widget_serialization)

    def __init__(self, **kwargs):
        super(ModelSync, self).__init__(**kwargs)

    def addStateVariable(self, stateVariable):
        self.stateVariables = [i for i in self.stateVariables] + [stateVariable]

    def addGeometries(self, geometries):
        #First resolve the sections
        self.geometries = [i for i in self.geometries] + geometries

# COMPONENT
class ComponentWidget(widgets.Widget):
    _model_name = Unicode('ComponentModel').tag(sync=True)
    _model_module = Unicode('geppettoWidgets').tag(sync=True)

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
        super(ComponentWidget, self).__init__(**kwargs)

        if 'value' in kwargs and kwargs["value"] is not None:
            sync_values[kwargs["value"]] = self

        self._click_handlers = widgets.CallbackDispatcher()
        self._change_handlers = widgets.CallbackDispatcher()
        self._blur_handlers = widgets.CallbackDispatcher()

        self.on_msg(self._handle_button_msg)

    def clickedCheckboxValue(targetComponent, triggeredComponent, args):
        if args[1]['data'] != None and float(args[1]['data']) != float(triggeredComponent.extraData['originalValue']):
            targetComponent.sync_value =  'true'
        else:        
            targetComponent.sync_value =  'false'
            
    def resetValueToOriginal(targetComponent, triggeredComponent, args):
        triggeredComponent.sync_value = 'false'
        exec("h." + targetComponent.value + "=" + str(targetComponent.extraData['originalValue']))
        #targetComponent.sync_value = str(targetComponent.extraData['originalValue'])
        
    def fireChangeCallbacks(self, *args, **kwargs):
        self.fireCallbacks(self.changeCallbacks, args)

    def fireClickCallbacks(self, *args, **kwargs):
        self.fireCallbacks(self.clickCallbacks, args)    

    def fireBlurCallbacks(self, *args, **kwargs):
        self.fireCallbacks(self.blurCallbacks, args)
        if self.value != None and args[1]['data'] != None:
            exec("h." + self.value + "=" + str(args[1]['data']))

    def fireCallbacks(self, cbs, args):
        if isinstance(cbs, list):
            for callback in cbs:
                exec(callback)
        else:
            cbs(self, args)

    def on_click(self, callbacks, remove=False):
        self.clickCallbacks = callbacks    
        self._click_handlers.register_callback(self.fireClickCallbacks, remove=remove)

    def on_change(self, callbacks, remove=False):
        self.changeCallbacks = callbacks    
        self._change_handlers.register_callback(self.fireChangeCallbacks, remove=remove)

    def on_blur(self, callbacks, remove=False):
        self.blurCallbacks = callbacks    
        self._blur_handlers.register_callback(self.fireBlurCallbacks, remove=remove)    

    def _handle_button_msg(self, _, content, buffers):
        if content.get('event', '') == 'click':
            self._click_handlers(self, content)
        elif content.get('event', '') == 'change':
            self._change_handlers(self, content)
        elif content.get('event', '') == 'blur':
            self._blur_handlers(self, content)

# PANEL
class PanelWidget(widgets.Widget):
    _model_name = Unicode('PanelModel').tag(sync=True)
    _model_module = Unicode('geppettoWidgets').tag(sync=True)

    widget_id = Unicode('').tag(sync=True)
    widget_name = Unicode('').tag(sync=True)

    items = List(Instance(widgets.Widget)).tag(sync=True, **widgets.widget_serialization)
    parentStyle = Dict({'flexDirection': 'column'}).tag(sync=True)
    embedded = Bool(False).tag(sync=True)
    positionX = Float(-1).tag(sync=True)
    positionY = Float(-1).tag(sync=True)

    def __init__(self, **kwargs):
        super(PanelWidget, self).__init__(**kwargs)
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
        self.parentStyle ={'flexDirection': direction}

    def display(self):
        self.send({"type": "display"})