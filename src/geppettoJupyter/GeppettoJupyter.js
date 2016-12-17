define('geppettoJupyter', function () {

    var geppettoJupyterModelSync = window.parent.require('components/geppetto-jupyter/GeppettoJupyterModelSync');
    var geppettoJupyterGUISync = window.parent.require('components/geppetto-jupyter/GeppettoJupyterGUISync');
    var geppettoJupyterWidgetSync = window.parent.require('components/geppetto-jupyter/GeppettoJupyterWidgetSync');

    return {
        PanelSync: geppettoJupyterGUISync.PanelSync,
        ComponentSync: geppettoJupyterGUISync.ComponentSync,

        StateVariableSync: geppettoJupyterModelSync.StateVariableSync,
        GeometrySync: geppettoJupyterModelSync.GeometrySync,
        ModelSync: geppettoJupyterModelSync.ModelSync,
        ExperimentSync: geppettoJupyterModelSync.ExperimentSync,
        ProjectSync: geppettoJupyterModelSync.ProjectSync,
        EventsSync: geppettoJupyterModelSync.EventsSync,

        WidgetSync: geppettoJupyterWidgetSync.WidgetSync,
        PlotWidgetSync: geppettoJupyterWidgetSync.PlotWidgetSync
    };
});