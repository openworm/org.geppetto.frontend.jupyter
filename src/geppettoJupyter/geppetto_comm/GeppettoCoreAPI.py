import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Dict, Bool, Float)
from collections import defaultdict
from IPython.display import Javascript, display_javascript

from .GeppettoCore import ComponentWidget, PanelWidget, ProjectSync, ExperimentSync, ModelSync, StateVariableSync

from . import GeppettoCore

from neuron import h
h.load_file("stdrun.hoc")

lastId = {
    'project': 0,
    'experiment': 0,
    'model': 0,
    'stateVariable': 0,
    'component': 0,
    'id': 0
} 
def newId(prefix ='id'):
    global lastId
    lastId[prefix]+=1;
    return str(lastId[prefix])
    
    
#GUI API    
def addButton(name, actions = None, value = None, extraData = None):
    if value is not None:
        valueUnits = h.units(value)
        if valueUnits != '':
            name += " (" + valueUnits + ")"
            
    button = ComponentWidget(component_name='RAISEDBUTTON', widget_id=newId(), widget_name=name, extraData = extraData)
    if actions is not None:
        button.on_click(actions)
    
    return button

def addTextField(name, value = None):
    parameters = {'component_name':'TEXTFIELD', 'widget_id':newId(), 'widget_name' : name}
    
    if 'value' is not None:
        parameters['sync_value'] = str(eval("h."+ value))
        extraData = {'originalValue': str(eval("h."+value))}
        parameters['extraData'] = extraData
        parameters['value'] = value
    else:
        parameters['value'] = ''
    return ComponentWidget(**parameters)     

def addTextFieldAndButton(name, value = None, create_checkbox = False, actions = None):
    items = []
    items.append(addButton(name, actions = None, value = value))
    textField = addTextField(name, value)
    if create_checkbox == True:
        checkbox = addCheckbox("checkbox" + name)
        checkbox.on_change(textField.resetValueToOriginal)
        items.append(checkbox)
        textField.on_blur(checkbox.clickedCheckboxValue)
    items.append(textField)  
    panel = addPanel(name, items = items)
    panel.setDirection('row')
    return panel
        
def addPanel(name, items = [], widget_id=None, positionX=-1, positionY=-1):
    if widget_id is None: widget_id = newId()
    for item in items:
        item.embedded = True
    return PanelWidget(widget_id = widget_id, widget_name=name, items=items, positionX=positionX, positionY=positionY)

def addCheckbox(name, sync_value = 'false'):
    return ComponentWidget(component_name='CHECKBOX', widget_id=newId(), widget_name=name, sync_value = sync_value)

#MODEL API
def createProject(id = None, name = 'Untitled Project', experiments = []):
    #TODO Make a dict with next id per project and component
    if id is None: id = newId('project')
    if experiments == []:
        experiment = createExperiment()
        GeppettoCore.current_experiment = experiment
        experiments.append(experiment)
    GeppettoCore.current_model = createModel(id = id, name = name)    
    GeppettoCore.current_project = ProjectSync(id = id, name = name, experiments = experiments)

def createExperiment(id = None, name = 'Untitled Experiment', state = 'Design'):
    #TODO Make a dict with next id per project and component
    if id is None: id = newId('experiment')
    return ExperimentSync(id = id, name = name, state = state)

def createModel(id = None, name = 'Untitled Model', stateVariables = []):
    #TODO Make a dict with next id per project and component
    if id is None: id = newId('model')
    return ModelSync(id = id, name = name, stateVariables = stateVariables)

def createStateVariable(id = None, name = 'Untitled State Variable', units = 'Unknown', timeSeries = [], neuron_variable = None):
    #TODO Make a dict with next id per project and component
    if id is None: id = newId('stateVariable')
    stateVariableSync = StateVariableSync(id = id, name = name, units = units, timeSeries = timeSeries, neuron_variable = neuron_variable)
    GeppettoCore.current_model.addStateVariable(stateVariableSync)

#PLOT API
def plotVariable(name = None, variables = []):
    jsCommand = "window.parent.G.addWidget(0)"
    if name != None:
        jsCommand += ".setName('%s')" % name
    for variable in variables:
        jsCommand += ".plotData(window.parent.%s)" % variable   
    jso = Javascript(jsCommand)
    display_javascript(jso)

