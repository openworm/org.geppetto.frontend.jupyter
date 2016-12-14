import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Dict, Bool, Float)
from collections import defaultdict
from IPython.display import Javascript, display_javascript

from .GeppettoJupyterGUISync import ComponentSync, PanelSync
from .GeppettoJupyterModelSync import ProjectSync, ExperimentSync, ModelSync, StateVariableSync
from .GeppettoJupyterWidgetSync import PlotWidgetSync
from . import GeppettoJupyterModelSync

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
    lastId[prefix]+=1
    return str(lastId[prefix])
    
#GUI API    
def addButton(name, actions = None, value = None, extraData = None):
    if value is not None:
        valueUnits = h.units(value)
        if valueUnits != '':
            name += " (" + valueUnits + ")"
            
    button = ComponentSync(component_name='RAISEDBUTTON', widget_id=newId(), widget_name=name, extraData = extraData)
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
    return ComponentSync(**parameters)     

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
    return PanelSync(widget_id = widget_id, widget_name=name, items=items, positionX=positionX, positionY=positionY)

def addCheckbox(name, sync_value = 'false'):
    return ComponentSync(component_name='CHECKBOX', widget_id=newId(), widget_name=name, sync_value = sync_value)

#MODEL API
def createProject(id = None, name = 'Untitled Project', experiments = []):
    if id is None: id = newId('project')
    if experiments == []:
        experiment = createExperiment()
        GeppettoJupyterModelSync.current_experiment = experiment
        experiments.append(experiment)
    GeppettoJupyterModelSync.current_model = createModel(id = name.replace(" ", ""), name = name)    
    GeppettoJupyterModelSync.current_project = ProjectSync(id = id, name = name, experiments = experiments)

def createExperiment(id = None, name = 'Untitled Experiment', state = 'Design'):
    if id is None: id = newId('experiment')
    return ExperimentSync(id = id, name = name, state = state)

def createModel(id = None, name = 'Untitled Model', stateVariables = []):
    if id is None: id = newId('model')
    return ModelSync(id = id, name = name, stateVariables = stateVariables)

def createStateVariable(id = None, name = 'Untitled State Variable', units = 'Unknown', timeSeries = [], neuron_variable = None):
    if id is None:
        id = newId('stateVariable')
    else:
        # Check this variable is not already in the model
        for stateVariable in GeppettoJupyterModelSync.current_model.stateVariables:
            if stateVariable.id == id:
                return

    GeppettoJupyterModelSync.current_model.addStateVariable(StateVariableSync(id = id, name = name, units = units, timeSeries = timeSeries, neuron_variable = neuron_variable))

def createGeometryVariables(geometries = []):
    GeppettoJupyterModelSync.current_model.addGeometries(geometries)



#PLOT API
def plotVariable(name = None, variables = []):
    PlotWidgetSync(widget_id = 0, name = name, data = variables)
