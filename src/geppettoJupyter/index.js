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

		// Restart kernel to delete any previous variable and start with a fresh instance
		IPython.notebook.restart_run_all({confirm: false})
	}

	 var load_ipython_extension = function () {
        if (IPython.notebook) {
            load_extension();
        }
        $([IPython.events]).on("notebook_loaded.Notebook", load_extension);
    };

	// Export the required load_ipython_extention
	return {
		load_ipython_extension: load_ipython_extension
	};
});