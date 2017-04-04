<p align="center">
  <img src="https://dl.dropboxusercontent.com/u/7538688/geppetto%20logo.png?dl=1" alt="Geppetto logo"/>
</p>

# Geppetto Jupyter Notebook Extension
This is an experimental repo for a Jupyter notebook extension. This extension extends Jupyter Python server based on tornado that allows the client to establish a websocket connection and server static resources.

How to install:
```
pip install jupyter_geppetto
jupyter nbextension enable --py --sys-prefix jupyter_geppetto
```

How to install extension from sources:
```
git clone --recursive https://github.com/openworm/org.geppetto.frontend.jupyter.git
pip install .
jupyter nbextension install --py jupyter_geppetto
jupyter nbextension enable --py jupyter_geppetto
```
To overwrite the local install:
```
pip install . --upgrade --no-deps --force-reinstall
```

To connect go to the URL:
http://localhost:8888/geppetto
assuming the default Jupyter configuration, otherwise change port accordingly.

Note if you get a 404 and you have a custom configuration of Jupyter notebook you will have to add the following to your jupyter_notebook_config.py:
```
c.NotebookApp.nbserver_extensions = {'jupyter_geppetto':True}
```
