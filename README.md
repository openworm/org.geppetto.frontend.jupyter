<p align="center">
  <img src="https://dl.dropboxusercontent.com/u/7538688/geppetto%20logo.png?dl=1" alt="Geppetto logo"/>
</p>

# Geppetto Jupyter Notebook Extension
This is an experimental repo for a Jupyter notebook extension. This extension creates a Python server based on tornado that allows the client to establish a websocket connection and server static resources but there is no real functionality beyond that.

How to install extension:

pip install .
sudo jupyter nbextension install --py geppetto_connector
sudo jupyter nbextension enable --py geppetto_connector

To overwrite the local install:
pip install . --upgrade --no-deps --force-reinstall

To connect go to the URL:
http://localhost:8888/nbextensions/geppetto_connector/index.js
