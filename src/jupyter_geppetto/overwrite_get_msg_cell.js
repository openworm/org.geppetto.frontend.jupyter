// Jupyter Extension: allows to execute commands from the shell which open a graphical interface
// In general, Jupyter allows to execute commands from a shell connected to an existing jupyter instances
// however when these commands open a gui, an output cell is required in order to print the output of this result.
// This extension changes that behaviour so that if no cell is found (i.e. when the command is executed from the shell)
// we will use the last cell on the python console to print the output
define(["notebook/js/notebook"], function (notebook) {
	"use strict";
	function load() {
		var notebookPrototype = notebook.Notebook.prototype;
		var original_get_msg_cell = notebookPrototype.get_msg_cell;
		notebook.Notebook.prototype.get_msg_cell = function (msg_id) {
			var output = original_get_msg_cell.apply(this, [msg_id]);
			if (output == null) {
				output = this.get_cell(this.ncells() - 1)
			}
			return output;
		};
	}

	return {
		load_ipython_extension: load
	};
});