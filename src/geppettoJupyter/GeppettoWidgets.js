define('geppettoWidgets', function () {

    var geppettoJupyterModelSync = window.parent.require('components/geppetto-jupyter/GeppettoJupyterModelSync');
    var geppettoJupyterGUISync = window.parent.require('components/geppetto-jupyter/GeppettoJupyterGUISync');
    var geppettoJupyterWidgetSync = window.parent.require('components/geppetto-jupyter/GeppettoJupyterWidgetSync');

    return {
        PanelModel: geppettoJupyterGUISync.PanelModel,
        ComponentModel: geppettoJupyterGUISync.ComponentModel,

        StateVariableSync: geppettoJupyterModelSync.StateVariableSync,
        GeometrySync: geppettoJupyterModelSync.GeometrySync,
        ModelSync: geppettoJupyterModelSync.ModelSync,
        ExperimentSync: geppettoJupyterModelSync.ExperimentSync,
        ProjectSync: geppettoJupyterModelSync.ProjectSync,

        WidgetSync: geppettoJupyterWidgetSync.WidgetSync,
        PlotWidgetSync: geppettoJupyterWidgetSync.PlotWidgetSync
    };
});