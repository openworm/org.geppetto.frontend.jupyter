import './jupyter_geppetto';
import './geppettoJupyter.less';

function load_extension() {

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

	// Make Jupyter (aka IPython) available to Geppetto
	window.parent.IPython = IPython;

	// If a Geppetto extension is defining a custom behavior to load the kernel we call it
	IPython.notebook.restart_kernel({ confirm: false }).then(function () {
		
		//Import the GUI sync to use the Python Controlled Capabilities, logging, etc
		IPython.notebook.kernel.execute('from jupyter_geppetto import jupyter_geppetto, utils');

		// Load the project & activate the experiment
		var project = { id: 1, name: 'Project', experiments: [{ "id": 1, "name": 'Experiment', "status": 'DESIGN' }] }
		window.parent.GEPPETTO.Manager.loadProject(project, false);
		window.parent.GEPPETTO.Manager.loadExperiment(1, [], []);

		// Trigger event for the extension (ComponentInitialization) to run custom code
		window.parent.GEPPETTO.trigger('jupyter_geppetto_extension_ready')
	});
}

var load_ipython_extension = function () {
	if (IPython.notebook !== undefined && IPython.notebook._fully_loaded) {
		console.log("Kernel ready")
		load_extension();
	} else {
		console.log("Waiting for kernel to be ready")
		IPython.notebook.events.on("notebook_loaded.Notebook", function () {
			load_extension();
		})
	}
};

export {
	load_ipython_extension
};
