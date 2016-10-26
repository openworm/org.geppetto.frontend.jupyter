define(['base/js/namespace', './GeppettoWidgets', 'base/js/events', 'nbextensions/jupyter-js-widgets/extension'], function (Jupyter, GeppettoWidgets, events, JupyterWidgets) {

	//'base/js/events',
	
	function load_ipython_extension(){
		document.addEventListener("DOMContentLoaded", function(event) {
			console.log('kake')
		})
		// Load css first
		var $stylesheet = $('<link/>')
			.attr({
				id: 'geppettoJupyter',
				rel: 'stylesheet',
				type: 'text/css',
				href: require.toUrl('/nbextensions/geppettoJupyter/geppettoJupyter.css')
			})
			.appendTo('head');


		$('#header').hide();

		IPython.keyboard_manager.command_shortcuts.add_shortcut('ctrl-`', function (event) {
			if (IPython.notebook.mode == 'command') {
				$('#header').toggle();
				return false;
			}
			return true;
		});

		setTimeout(function(){if (!Jupyter.notebook) {
	      events.on('notebook_loaded.Notebook', function(){Jupyter.notebook.get_cells()[0].execute();});
	    } else {
	    	Jupyter.notebook.get_cells()[0].execute();
	    }}, 1000);
	}
	
	// Export the required load_ipython_extention
	return {
	    load_ipython_extension: load_ipython_extension
	};
});