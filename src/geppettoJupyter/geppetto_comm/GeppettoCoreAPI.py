import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Dict, Bool, Float)
from collections import defaultdict
from IPython.display import Javascript, display_javascript
import logging

from .GeppettoJupyterModelSync import ProjectSync, ExperimentSync, ModelSync, StateVariableSync, GeometrySync, DerivedStateVariableSync
from .GeppettoJupyterWidgetSync import PlotWidgetSync, PopupWidgetSync
from . import GeppettoJupyterModelSync

lastId = {
    'project': 0,
    'experiment': 0,
    'model': 0,
    'stateVariable': 0,
    'derived_state_variable': 0,
    'component': 0,
    'id': 0,
    'geometry': 0
} 
def newId(prefix='id'):
    global lastId
    lastId[prefix]+=1
    return str(lastId[prefix])

def getId(id, prefix='id'):
    if id is None: id = newId(prefix)
    return removeSpecialCharacters(id)

def removeSpecialCharacters(string):
    return ''.join(c for c in string if c.isalnum())

#MODEL API
def createProject(id = None, name = 'Untitled Project', experiments = []):
    id = getId(id, 'project')
    if experiments == []:
        experiment = createExperiment()
        GeppettoJupyterModelSync.current_experiment = experiment
        experiments.append(experiment)
    GeppettoJupyterModelSync.current_model = createModel(id = name.replace(" ", ""), name = name)    
    GeppettoJupyterModelSync.current_project = ProjectSync(id = id, name = name, experiments = experiments)

def createExperiment(id = None, name = 'Untitled Experiment', status = 'DESIGN'):
    id = getId(id, 'experiment')
    return ExperimentSync(id = id, name = name, status = status)

def createGeometry(sec_name = 'Untitled Geometry', index = 0, position = [], distal = [], python_variable = None):
    id = getId(sec_name) + "_" + str(index)
    return GeometrySync(id = id, name = sec_name + " " + str(index),  bottomRadius = position[3]/2, positionX = position[0], positionY = position[1] , positionZ = position[2], topRadius = distal[3]/2, distalX = distal[0], distalY = distal[1], distalZ = distal[2], python_variable = python_variable)

def createModel(id = None, name = 'Untitled Model', stateVariables = []):
    id = getId(id, 'model')
    return ModelSync(id = id, name = name, stateVariables = stateVariables)

def createStateVariable(id = None, name = 'Untitled State Variable', units = 'Unknown', timeSeries = [], python_variable = None, geometries = []):
    id = getId(id, 'stateVariable')
    # Check this variable is not already in the model
    for stateVariable in GeppettoJupyterModelSync.current_model.stateVariables:
        if stateVariable.id == id:
            return stateVariable

    state_variable = StateVariableSync(id = id, name = name, units = units, timeSeries = timeSeries, python_variable = python_variable, geometries = geometries)
    GeppettoJupyterModelSync.current_model.addStateVariable(state_variable)
    return state_variable

def createDerivedStateVariable(id = None, name = 'Untitled State Variable', units = 'Unknown', timeSeries = [], inputs = [], normalizationFunction = None):
    id = getId(id, 'derivedStateVariable')
    # Check this variable is not already in the model
    for derived_state_variable in GeppettoJupyterModelSync.current_model.derived_state_variables:
        if derived_state_variable.id == id:
            return derived_state_variable
    return DerivedStateVariableSync(id = id, name = name, units = units, timeSeries = timeSeries, inputs_raw = inputs, normalizationFunction = normalizationFunction)

#PLOT API
def plotVariable(name = None, variables = [], position_x=-1, position_y=-1, width=-1,height=-1):
    return PlotWidgetSync(widget_id = 0, name = name, data = variables, position_x=position_x, position_y=position_y, width=width, height=height)

#POPUP API
def popupVariable(name = None, variables = [], position_x=-1, position_y=-1, width=-1,height=-1):
    return PopupWidgetSync(widget_id = 1, name = name, data = variables, position_x=position_x, position_y=position_y, width=width, height=height)