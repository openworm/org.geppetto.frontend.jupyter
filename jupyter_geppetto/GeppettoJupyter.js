define('jupyter_geppetto', function () {

    var GeppettoJupyterSync = window.parent.GEPPETTO.GeppettoJupyterSync;
    
    return {
        ComponentSync: GeppettoJupyterSync.ComponentSync,
        ModelSync: GeppettoJupyterSync.ModelSync,
        ExperimentSync: GeppettoJupyterSync.ExperimentSync,
        ProjectSync: GeppettoJupyterSync.ProjectSync,
        EventsSync: GeppettoJupyterSync.EventsSync,
    };
});