define(['base/js/namespace', './GeppettoWidgets', 'base/js/events'], function (Jupyter, GeppettoWidgets, events) {

	function load_ipython_extension() {
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

		// Execute first cell.
		// Due to a bug on jupyter, we have to wait for a second so that everything is loaded properly
		setTimeout(function () {
			if (!Jupyter.notebook) {
				events.on('notebook_loaded.Notebook', function () { Jupyter.notebook.get_cells()[0].execute(); });
			} else {
				Jupyter.notebook.get_cells()[0].execute();
			}
		}, 1000);
	}

	// Export the required load_ipython_extention
	return {
		load_ipython_extension: load_ipython_extension
	};
});