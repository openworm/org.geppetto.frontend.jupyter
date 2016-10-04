define(["notebook/js/notebook"], function (notebook) {
  "use strict";
  function load () {
	  var notebookPrototype = notebook.Notebook.prototype;
	  var original_get_msg_cell = notebookPrototype.get_msg_cell;
	  notebook.Notebook.prototype.get_msg_cell = function (msg_id) {
		  var output = original_get_msg_cell.apply(this, [msg_id]);
		  if (output == null){
			  output = notebookPrototype.get_cell(notebookPrototype.ncells()-1)
		  }
		  return output;
	  };
  }

  return {
    load_ipython_extension: load
  };
});