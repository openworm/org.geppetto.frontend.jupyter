define('geppettoWidgets', function() {

var geppettoJupyterWidgets = window.parent.require('components/jupyter/GeppettoJupyter')

    return {
        PanelView: geppettoJupyterWidgets.PanelView,
        PanelModel: geppettoJupyterWidgets.PanelModel,
        ComponentView: geppettoJupyterWidgets.ComponentView,
        ComponentModel: geppettoJupyterWidgets.ComponentModel,
        StateVariableSync: geppettoJupyterWidgets.StateVariableSync,
        ModelSync: geppettoJupyterWidgets.ModelSync,
        ExperimentSync: geppettoJupyterWidgets.ExperimentSync,
        ProjectSync: geppettoJupyterWidgets.ProjectSync
    };
})