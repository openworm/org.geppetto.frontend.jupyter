import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Dict, Bool, Float)
from collections import defaultdict

from neuron import h
h.load_file("stdrun.hoc")

#UTILS
sync_values = defaultdict(list)

# EXPERIMENT
class ExperimentSync(widgets.Widget):
    # _model_name = Unicode('ExperimentSync').tag(sync=True)
    # _model_module = Unicode('geppettoWidgets').tag(sync=True)

    name = Unicode('').tag(sync=False)
    id = Unicode('').tag(sync=False)
    lastModified = Unicode('').tag(sync=False)
    state = Unicode('').tag(sync=False)

    def __init__(self, **kwargs):
        super(ExperimentSync, self).__init__(**kwargs)

# PROJECT
class ProjectSync(widgets.Widget):
    _model_name = Unicode('ProjectSync').tag(sync=True)
    _model_module = Unicode('geppettoWidgets').tag(sync=True)

    name = Unicode('').tag(sync=True)
    id = Unicode('').tag(sync=True)
    serialisedProject = Unicode('').tag(sync=True)

    experiments = List(Instance(ExperimentSync)).tag(sync=False)

    def __init__(self, **kwargs):
        super(ProjectSync, self).__init__(**kwargs)

    def addExperiment(self, experiment):
        self.experiments = [i for i in self.experiments] + [experiment]

    def to_JSON(self):
        print("ProjectSync serialising")
        self.serialisedModel = 'TAKA'

# STATE VARIABLE
class StateVariableSync(widgets.Widget):
    # _model_name = Unicode('StateVariableSync').tag(sync=True)
    # _model_module = Unicode('geppettoWidgets').tag(sync=True)

    name = Unicode('').tag(sync=False)
    id = Unicode('').tag(sync=False)
    units = Unicode('').tag(sync=False)
    timeSeries = List(Float).tag(sync=False)

    def __init__(self, **kwargs):
        super(StateVariableSync, self).__init__(**kwargs)
   

# MODEL
class ModelSync(widgets.Widget):
    _model_name = Unicode('ModelSync').tag(sync=True)
    _model_module = Unicode('geppettoWidgets').tag(sync=True)

    name = Unicode('').tag(sync=True)
    id = Unicode('').tag(sync=True)
    serialisedModel = Unicode('').tag(sync=True)

    stateVariables = List(Instance(StateVariableSync)).tag(sync=False)

    def __init__(self, **kwargs):
        super(ModelSync, self).__init__(**kwargs)
        
    def addStateVariable(self, stateVariable):
        self.stateVariables = [i for i in self.stateVariables] + [stateVariable]
    
    def to_JSON(self):
        print("ModelSync serialising")
        self.serialisedModel = 'TAKA'



# COMPONENT
class ComponentWidget(widgets.Widget):
    _view_name = Unicode('ComponentView').tag(sync=True)
    _view_module = Unicode('geppettoWidgets').tag(sync=True)
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
    _view_name = Unicode('PanelView').tag(sync=True)
    _view_module = Unicode('geppettoWidgets').tag(sync=True)
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