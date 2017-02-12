define(['base/js/namespace', './GeppettoJupyter', 'base/js/events'], function (Jupyter, GeppettoJupyter, events) {

	function load_extension() {
		// Load css first
		var $stylesheet = $('<link/>')
			.attr({
				id: 'geppettoJupyter',
				rel: 'stylesheet',
				type: 'text/css',
				href: require.toUrl('/nbextensions/geppettoJupyter/geppettoJupyter.css')
			})
			.appendTo('head');

		// Hide the header
		$('#header').hide();

		// Add shortcut to hide/show header
		IPython.keyboard_manager.command_shortcuts.add_shortcut('ctrl-`', function (event) {
			if (IPython.notebook.mode == 'command') {
				$('#header').toggle();
				return false;
			}
			return true;
		});

		window.parent.loadModelInJupyter = function(module,model){

			// Close any previous panel
			window.parent.removeAllPanels();

			IPython.notebook.restart_kernel({confirm: false}).then(function() {

				// IPython.notebook.execute_all_cells();

				// Load Neuron Basic GUI
				var kernel = IPython.notebook.kernel;
				kernel.execute('import neuron_geppetto');
				kernel.execute('neuron_geppetto.init()');
				
				// Load Model
				if (module != undefined && module != "" && model != undefined  && model != ""){
					kernel.execute('from geppettoJupyter.geppetto_comm import GeppettoJupyterModelSync');
					kernel.execute('import importlib');
					kernel.execute('python_module = importlib.import_module("models.' + module +'")')
					kernel.execute('GeppettoJupyterModelSync.current_python_model = getattr( python_module, "' + model + '")()')
				}
			});
        }

		// Read attributes from url
		function getParameterByName(name) {
			name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
			var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
			results = regex.exec(window.parent.location.search);
			return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
		}
		module = getParameterByName('load_module');
		model = getParameterByName('load_model');

		// Restart server and load model if needed
		window.parent.loadModelInJupyter(module,model)

	}

	 var load_ipython_extension = function () {
        if (IPython.notebook) {
            load_extension();
        }
        $([IPython.events]).on("notebook_loaded.Notebook", load_extension);
    };

	// $([IPython.events]).on("notebook_loaded.Notebook", function () {
	// 	IPython.notebook.set_autosave_interval(0);
	// });

	// Export the required load_ipython_extention
	return {
		load_ipython_extension: load_ipython_extension
	};
});