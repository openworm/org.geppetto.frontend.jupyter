import setuptools
from glob import glob
import fnmatch
import os
from setuptools.command.install import install
import fileinput

#This block copies resources to the server (/usr/local/share/jupyter/nbextensions/)
data_files = []
data_files.append(('share/jupyter/nbextensions/geppettoJupyter', glob('src/geppettoJupyter/*.js')))
data_files.append(('share/jupyter/nbextensions/geppettoJupyter', glob('src/geppettoJupyter/*.css')))

setuptools.setup(
    name="geppettoJupyter",
    version="0.0.1",
    url="https://github.com/openworm/org.geppetto.frontend.jupyter",
    author="The Geppetto Development Team",
    description="Geppetto extension for Jupyter notebook",
    license= "MIT",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    data_files=data_files,
    include_package_data=True,
    install_requires = [
        'ipywidgets>=5.1.5',
        'jupyter>=1.0.0'
    ],
)