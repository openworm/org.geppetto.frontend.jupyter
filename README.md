<p align="center">
  <img src="https://dl.dropboxusercontent.com/u/7538688/geppetto%20logo.png?dl=1" alt="Geppetto logo"/>
</p>

# Geppetto Jupyter Notebook Extension
This is an experimental repo for a Jupyter notebook extension. This extension extends Jupyter Python server based on tornado that allows the client to establish a websocket connection and server static resources.

How to install:
```bash
pip install jupyter_geppetto
jupyter nbextension enable --py --sys-prefix jupyter_geppetto
```

How to install extension from sources:
```bash
git clone --recursive https://github.com/openworm/org.geppetto.frontend.jupyter.git
pip install .

jupyter nbextension install --py --symlink --sys-prefix jupyter_geppetto
jupyter nbextension enable --py jupyter_geppetto
jupyter serverextension enable --py jupyter_geppetto
```
To overwrite the local install:
```bash
pip install . --upgrade --no-deps --force-reinstall
```

To connect go to the URL:
http://localhost:8888/geppetto
assuming the default Jupyter configuration, otherwise change the port accordingly.

Note if you get a 404 and you have a custom configuration of Jupyter notebook you will have to add the following to your jupyter_notebook_config.py:
```
c.NotebookApp.nbserver_extensions = {'jupyter_geppetto':True}
```

After the extension is installed the Jupyter notebook must be run with the parameter --library, which specifies the 
Python libraries to be loaded together with the extension:
```bash
exec jupyter notebook --NotebookApp.default_url=/geppetto --NotebookApp.token='' --library=nwb_explore
```


# Development 
## Web api
Allows to add own custom routes and handlers from inside the application.
The dependencies must be added from within the libraries specified in the parameter --library

In the file root of your module (__init__.py of your package), call the RouteManager methods to add your custom routes:
```python
from jupyter_geppetto.webapi import RouteManager

RouteManager.add_controller(MyController) # Add a controller (preferred way for http requests)
RouteManager.add_route('/my/path', MyTornadoHandler) # for more custom control
```

A controller class is a standard class with webapi annotations on methods.
Methods return the response as a string.

Example:
```python
from jupyter_geppetto.webapi import get, post

class MyController:

    @get('/my/simple/path')
    def simple_action(self):
        return "My response payload" # Simple text response

    @get('/myresource/(.*)')
    def action_with_url_param(self, param):
        import json
        return json.dumps({'param':param}) # JSON response
    
    @get('/myresource')
    def action_with_query_string_params(self, param1, param2=None):
        '''Handles 
            /myresource?param1=something&param2=somethingelse
            /myresource?param1=something
        '''
        return ...   
    
    @get('/myresource')
    def alt_action_with_query_string_params(self, **kwargs):
        '''Handles any query string parameter'''
        return ...   
        
    @get('/myresource/(.*)')
    def action_with_url_and_query_string_params(self, param, param1, param2):
        '''Handles /myresource?param1=comething&param2=somethingelse'''
        return ... 
        
    @post('/myresource')
    def simple_post_action(self, payload, param1, param2):
        '''Handles /myresource and body param1=something&param2=somethingelse'''
        return ... 
```
## Synchronization
This feature allows to synchronize backend and frontend objects.
It's implemented through a [IPython/Jupyter widget](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20Basics.html).
On the JS side, the connection is achieved through the PythonControlledCapability of the [Geppetto client](https://github.com/openworm/geppetto-client/).

 
### Usage
```python
from jupyter_geppetto import synchronization
class MyClass:
    def a(self):
        ...
    def b(self):
        ...
synchronization.startSynchronization(MyClass().__dict__)

```
