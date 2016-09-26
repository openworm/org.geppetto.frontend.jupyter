define('geppettoWidgets', ["jupyter-js-widgets"], function(widgets) {

var geppettoJupyterWidgets = window.parent.require('components/GeppettoJupyterWidgets')

    return {
        PanelView: geppettoJupyterWidgets.PanelView,
        PanelModel: geppettoJupyterWidgets.PanelModel,
        ComponentView: geppettoJupyterWidgets.ComponentView,
        ComponentModel: geppettoJupyterWidgets.ComponentModel
    };
})