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
		if(window.parent.customJupyterModelLoad!=undefined){
			window.IPython.notebook.restart_kernel({ confirm: false }).then(function () {
                IPython.notebook.kernel.execute('from zmq.utils import jsonapi')
                IPython.notebook.kernel.execute('from ipykernel.jsonutil import json_clean')
                
				window.parent.customJupyterModelLoad();
            });
		}
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