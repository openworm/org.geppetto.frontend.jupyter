import setuptools
from glob import glob
import fnmatch
import os

#This block copies resources to the server (/usr/local/share/jupyter/nbextensions/)
data_files = []
for root, dirnames, filenames in os.walk('src/geppettoJupyter/geppetto/css/'):
    for filename in fnmatch.filter(filenames, '*'):
        data_files.append(('share/jupyter/nbextensions' + root[3:], [os.path.join(root, filename)]))
for root, dirnames, filenames in os.walk('src/geppettoJupyter/geppetto/less/'):
    for filename in fnmatch.filter(filenames, '*'):
        data_files.append(('share/jupyter/nbextensions' + root[3:], [os.path.join(root, filename)]))
for root, dirnames, filenames in os.walk('src/geppettoJupyter/geppetto/images/'):
    for filename in fnmatch.filter(filenames, '*'):
        data_files.append(('share/jupyter/nbextensions' + root[3:], [os.path.join(root, filename)]))
for root, dirnames, filenames in os.walk('src/geppettoJupyter/geppetto/js/'):
    for filename in fnmatch.filter(filenames, '*'):
        data_files.append(('share/jupyter/nbextensions' + root[3:], [os.path.join(root, filename)]))

data_files.append(('share/jupyter/nbextensions/geppettoJupyter', glob('src/geppettoJupyter/*.js')))

#raise AttributeError(data_files) For debug purposes

setuptools.setup(
    name="geppettoJupyter",
    version='0.1.0',
    url="http://geppetto.org",
    author="Adrian Quintana",
    description="Geppetto",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    data_files=data_files,
    include_package_data=True,
)
