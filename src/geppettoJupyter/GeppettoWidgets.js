define('geppettoWidgets', ["jupyter-js-widgets"], function(widgets) {

var geppettoJupyterWidgets = window.parent.require('components/jupyter/GeppettoJupyter')

    return {
        PanelView: geppettoJupyterWidgets.PanelView,
        PanelModel: geppettoJupyterWidgets.PanelModel,
        ComponentView: geppettoJupyterWidgets.ComponentView,
        ComponentModel: geppettoJupyterWidgets.ComponentModel,
        ModelSync: geppettoJupyterWidgets.ModelSync,
        ProjectSync: geppettoJupyterWidgets.ProjectSync
    };
})