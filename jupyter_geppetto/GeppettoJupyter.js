define('jupyter_geppetto', function () {

    var GeppettoJupyterSync = window.parent.GEPPETTO.GeppettoJupyterSync;
    
    return {
        ComponentSync: GeppettoJupyterSync.ComponentSync,
    };
});