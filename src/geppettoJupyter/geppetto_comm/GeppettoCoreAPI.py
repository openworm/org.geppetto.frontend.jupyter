import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Dict, Bool, Float)
from collections import defaultdict
from IPython.display import Javascript, display_javascript

from .GeppettoJupyterGUISync import ComponentSync, PanelSync
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

def createGeometry(id = None, name = 'Untitled Geometry', bottomRadius = 0, positionX = 0, positionY = 0, positionZ = 0, topRadius = 0, distalX = 0, distalY = 0, distalZ = 0, python_variable = None):
    if id is None: id = newId('geometry')
    return GeometrySync(id = id, name = name,  bottomRadius = bottomRadius, positionX = positionX, positionY = positionY , positionZ = positionZ, topRadius = topRadius, distalX = distalX, distalY = distalY, distalZ = distalZ, python_variable = python_variable)

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