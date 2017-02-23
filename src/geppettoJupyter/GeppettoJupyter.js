define('geppettoJupyter', function () {

    var geppettoJupyterModelSync = window.parent.GEPPETTO.GeppettoJupyterModelSync;
    var geppettoJupyterGUISync = window.parent.GEPPETTO.GeppettoJupyterGUISync;
    var geppettoJupyterWidgetSync = window.parent.GEPPETTO.GeppettoJupyterWidgetSync;

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