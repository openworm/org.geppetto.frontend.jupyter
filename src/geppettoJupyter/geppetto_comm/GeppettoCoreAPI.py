import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Dict, Bool, Float)
from collections import defaultdict
from IPython.display import Javascript, display_javascript

from .GeppettoJupyterModelSync import ProjectSync, ExperimentSync, ModelSync, StateVariableSync, GeometrySync
from .GeppettoJupyterWidgetSync import PlotWidgetSync, PopupWidgetSync
from . import GeppettoJupyterModelSync

lastId = {
    'project': 0,
    'experiment': 0,
    'model': 0,
    'stateVariable': 0,
    'component': 0,
    'id': 0,
    'geometry': 0
} 
def newId(prefix ='id'):
    global lastId
    lastId[prefix]+=1
    return str(lastId[prefix])

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

def createGeometry(sec_name = 'Untitled Geometry', index = 0, position = [], distal = [], python_variable = None):
    return GeometrySync(id = sec_name + "_" + str(index), name = sec_name + " " + str(index),  bottomRadius = position[3], positionX = position[0], positionY = position[1] , positionZ = position[2], topRadius = distal[3], distalX = distal[0], distalY = distal[1], distalZ = distal[2], python_variable = python_variable)

def createModel(id = None, name = 'Untitled Model', stateVariables = []):
    if id is None: id = newId('model')
    return ModelSync(id = id, name = name, stateVariables = stateVariables)

def createStateVariable(id = None, name = 'Untitled State Variable', units = 'Unknown', timeSeries = [], python_variable = None):
    if id is None: id = newId('stateVariable')
    # Check this variable is not already in the model
    for stateVariable in GeppettoJupyterModelSync.current_model.stateVariables:
        if stateVariable.id == id:
            return
    GeppettoJupyterModelSync.current_model.addStateVariable(StateVariableSync(id = id, name = name, units = units, timeSeries = timeSeries, python_variable = python_variable))

#PLOT API
def plotVariable(name = None, variables = []):
    return PlotWidgetSync(widget_id = 0, name = name, data = variables)

#POPUP API
def popupVariable(name = None, variables = []):
    return PopupWidgetSync(widget_id = 1, name = name, data = variables)