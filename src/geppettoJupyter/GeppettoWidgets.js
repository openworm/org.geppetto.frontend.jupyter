define('geppettoWidgets', function() {

var geppettoJupyterWidgets = window.parent.require('components/jupyter/GeppettoJupyter')

    return {
        PanelModel: geppettoJupyterWidgets.PanelModel,
        ComponentModel: geppettoJupyterWidgets.ComponentModel,
        StateVariableSync: geppettoJupyterWidgets.StateVariableSync,
        ModelSync: geppettoJupyterWidgets.ModelSync,
        ExperimentSync: geppettoJupyterWidgets.ExperimentSync,
        ProjectSync: geppettoJupyterWidgets.ProjectSync,
        WidgetSync: geppettoJupyterWidgets.WidgetSync,
        PlotWidgetSync: geppettoJupyterWidgets.PlotWidgetSync,
	PopupWidgetSync: geppettoJupyterWidgets.PopupWidgetSync
    };
})
