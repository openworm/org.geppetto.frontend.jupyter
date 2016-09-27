<p align="center">
  <img src="https://dl.dropboxusercontent.com/u/7538688/geppetto%20logo.png?dl=1" alt="Geppetto logo"/>
</p>

# Geppetto Jupyter Notebook Extension
This is an experimental repo for a Jupyter notebook extension. This extension creates a Python server based on tornado that allows the client to establish a websocket connection and server static resources but there is no real functionality beyond that.

How to install extension:
```
git clone --recursive https://github.com/openworm/org.geppetto.frontend.jupyter.git
sudo pip install .
sudo jupyter nbextension install --py geppettoJupyter
sudo jupyter nbextension enable --py geppettoJupyter
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
c.NotebookApp.nbserver_extensions = {'geppetto_connector':True}
```
