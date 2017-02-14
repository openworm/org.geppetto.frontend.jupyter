define('geppettoJupyter', function () {

    var geppettoJupyterModelSync = window.parent.require('components/geppetto-jupyter/GeppettoJupyterModelSync');
    var geppettoJupyterGUISync = window.parent.require('components/geppetto-jupyter/GeppettoJupyterGUISync');
    var geppettoJupyterWidgetSync = window.parent.require('components/geppetto-jupyter/GeppettoJupyterWidgetSync');

    return {
        PanelSync: geppettoJupyterGUISync.PanelSync,
        TextFieldSync: geppettoJupyterGUISync.TextFieldSync,
        CheckboxSync: geppettoJupyterGUISync.CheckboxSync,
        ButtonSync: geppettoJupyterGUISync.ButtonSync,
        LabelSync: geppettoJupyterGUISync.LabelSync,
        DropDownSync: geppettoJupyterGUISync.DropDownSync,

        StateVariableSync: geppettoJupyterModelSync.StateVariableSync,
        DerivedStateVariableSync: geppettoJupyterModelSync.DerivedStateVariableSync,
        ModelSync: geppettoJupyterModelSync.ModelSync,
        ExperimentSync: geppettoJupyterModelSync.ExperimentSync,
        ProjectSync: geppettoJupyterModelSync.ProjectSync,
        EventsSync: geppettoJupyterModelSync.EventsSync,

        WidgetSync: geppettoJupyterWidgetSync.WidgetSync,
        PlotWidgetSync: geppettoJupyterWidgetSync.PlotWidgetSync,
        PopupWidgetSync: geppettoJupyterWidgetSync.PopupWidgetSync
    };
});