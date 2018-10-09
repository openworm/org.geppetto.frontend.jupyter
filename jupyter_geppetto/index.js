define(['base/js/namespace', './GeppettoJupyter', 'base/js/events'], function (Jupyter, GeppettoJupyter, events) {

	function load_extension() {
		// Load css first
		var $stylesheet = $('<link/>')
			.attr({
				id: 'jupyter_geppetto',
				rel: 'stylesheet',
				type: 'text/css',
				href: require.toUrl('/nbextensions/jupyter_geppetto/geppettoJupyter.css')
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



		// Read attributes from url
		function getParameterByName(name) {
			name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
			var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
			results = regex.exec(window.parent.location.search);
			return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
		}
		module = getParameterByName('load_module');
		model = getParameterByName('load_model');

		window.parent.IPython = IPython;

		// If a Geppetto extension is defining a custom behavior to load the kernel we call it
		window.IPython.notebook.restart_kernel({ confirm: false }).then(function () {
			
			//import the GUI sync to use the Python Controlled Capabilities
			IPython.notebook.kernel.execute('from jupyter_geppetto import GeppettoJupyterSync');
			//initialize the Geppetto Python connector
			IPython.notebook.kernel.execute('from jupyter_geppetto import geppetto_init');
			
			window.parent.GEPPETTO.trigger('jupyter_geppetto_extension_ready')
		});
	}

	var load_ipython_extension = function () {
		if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
			console.log("Kernel ready")
            load_extension();
        } else {
			console.log("Waiting for kernel to be ready")
            events.on("notebook_loaded.Notebook", function () {
                load_extension();
            })
		}
    };
	
	return {
		load_ipython_extension: load_ipython_extension
	};
});