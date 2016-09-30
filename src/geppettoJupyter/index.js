define(['base/js/namespace', './GeppettoWidgets'], function (Jupyter, GeppettoWidgets) {
//	require('./GeppettoWidgets')	
	
	function load_ipython_extension(){
		// Load css first
		var $stylesheet = $('<link/>')
			.attr({
				id: 'geppettoJupyter',
				rel: 'stylesheet',
				type: 'text/css',
				href: require.toUrl('/nbextensions/geppettoJupyter/geppettoJupyter.css')
			})
			.appendTo('head');
		
		Jupyter.keyboard_manager.command_shortcuts.add_shortcut('ctrl-`', function (event) {
	        if (IPython.notebook.mode == 'command') {
	            $('#header').toggle();
	            return false;
	        }
	        return true;
	    });
		
//		var oldClass = Jupyter.notebook; // Copy original before overwriting
//		Jupyter.notebook = function () {
//		    // Apply the original constructor on this object
//		    oldClass.apply(this, arguments);
//
//		    // Now overwrite the target function after construction
//		    this.get_msg_cell = function () { alert("Overwritten"); };
//		};
//		Jupyter.notebook.prototype = oldClass.prototype; // Same prototype
		
		function override(object, methodName, callback) {
		  object[methodName] = callback(object[methodName])
		};
		
		override(Jupyter.notebook, 'prototype.get_msg_cell', function(original) {
			  return function(msg_id) {
			    var returnValue = original.apply(this, arguments)
			    console.log('Maricona ta')
			    return returnValue
			  }
			})
	}
	
	// Export the required load_ipython_extention
	return {
	    load_ipython_extension: load_ipython_extension
	};
});

//Notebook.prototype.get_msg_cell = function (msg_id) {
//    var msgCell = codecell.CodeCell.msg_cells[msg_id] || null;
//    if (msgCell == null){
//        msgCell = IPython.notebook.get_cell(IPython.notebook.ncells()-1)
//    }
//    return msgCell;
//};
//
//Notebook.prototype.get_msg_cell = function (msg_id) {
//    return codecell.CodeCell.msg_cells[msg_id] || null;
//};
//
//Jupyter.notebook

