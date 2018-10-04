import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Dict, Bool, Float)
from collections import defaultdict
from IPython.display import Javascript, display_javascript
import logging

from .GeppettoJupyterModelSync import ProjectSync, ExperimentSync, ModelSync
from . import GeppettoJupyterModelSync

lastId = {
    'project': 0,
    'experiment': 0,
    'model': 0,
    'component': 0,
    'id': 0,
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

def createModel(id = None, name = 'Untitled Model', stateVariables = []):
    id = getId(id, 'model')
    return ModelSync(id = id, name = name, stateVariables = stateVariables)