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
jupyter nbextension install --py jupyter_geppetto
jupyter nbextension enable --py jupyter_geppetto
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

# Web api

# Synchronization
This feature allows to synchronize backend and frontend objects.
It's implemented through a [IPython/Jupyter widget](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20Basics.html).
On the JS side, the connection is achieved through the PythonControlledCapability of the [Geppetto client](https://github.com/openworm/geppetto-client/).

 
## Usage
```python
from jupyter_geppetto import synchronization
class MyClass:
    def a(self):
        ...
    def b(self):
        ...
synchronization.startSynchronization(MyClass().__dict__)

```
