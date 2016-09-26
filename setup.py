import setuptools
from glob import glob
import fnmatch
import os

data_files = []
for root, dirnames, filenames in os.walk('src/geppetto_connector/static/geppetto/css/'):
    for filename in fnmatch.filter(filenames, '*'):
        data_files.append(('share/jupyter/nbextensions' + root[3:], [os.path.join(root, filename)]))
for root, dirnames, filenames in os.walk('src/geppetto_connector/static/geppetto/less/'):
    for filename in fnmatch.filter(filenames, '*'):
        data_files.append(('share/jupyter/nbextensions' + root[3:], [os.path.join(root, filename)]))
for root, dirnames, filenames in os.walk('src/geppetto_connector/static/geppetto/images/'):
    for filename in fnmatch.filter(filenames, '*'):
        data_files.append(('share/jupyter/nbextensions' + root[3:], [os.path.join(root, filename)]))
for root, dirnames, filenames in os.walk('src/geppetto_connector/static/geppetto/js/'):
    for filename in fnmatch.filter(filenames, '*'):
        data_files.append(('share/jupyter/nbextensions' + root[3:], [os.path.join(root, filename)]))
        
data_files.append(('share/jupyter/nbextensions/geppetto_connector', glob('src/geppetto_connector/static/geppetto_connector/*.js')))

setuptools.setup(
    name="geppetto_connector",
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