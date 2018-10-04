define('jupyter_geppetto', function () {

    var jupyter_geppettoModelSync = window.parent.GEPPETTO.GeppettoJupyterModelSync;
    var jupyter_geppettoGUISync = window.parent.GEPPETTO.GeppettoJupyterGUISync;

    return {
        ComponentSync: jupyter_geppettoGUISync.ComponentSync,
        ModelSync: jupyter_geppettoModelSync.ModelSync,
        ExperimentSync: jupyter_geppettoModelSync.ExperimentSync,
        ProjectSync: jupyter_geppettoModelSync.ProjectSync,
        EventsSync: jupyter_geppettoModelSync.EventsSync,
    };
});