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
        
data_files.append(('share/jupyter/nbextensions/geppetto_connector', ['src/geppetto_connector/static/geppetto_connector/index.js']))
data_files.append(('share/jupyter/nbextensions/geppetto_connector', ['src/geppetto_connector/static/geppetto_connector/GeppettoWidgets.js']))

# print(data_files)

setuptools.setup(
    name="geppetto_connector",
    version='0.1.0',
    url="http://example.org",
    author="John Doe",
    description="Amazing nbextension",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    data_files=data_files,
    include_package_data=True,
)

#                  ('share/jupyter/nbextensions/geppetto_connector/geppetto/css',glob('src/geppetto_connector/static/geppetto/css/*.css')),
#                  ('share/jupyter/nbextensions/geppetto_connector/geppetto/less',glob('src/geppetto_connector/static/geppetto/less/*.less')),
#                  ('share/jupyter/nbextensions/geppetto_connector/geppetto/js',glob('src/geppetto_connector/static/geppetto/js/*.js')),
#                  ('share/jupyter/nbextensions/geppetto_connector/geppetto/js/vendor',glob('src/geppetto_connector/static/geppetto/js/vendor/*.js')),
#                  ('share/jupyter/nbextensions/geppetto_connector/geppetto/images',glob('src/geppetto_connector/static/geppetto/images/*.png'))
#                  ('share/jupyter/nbextensions/geppetto_connector/geppetto/css',cssmatches),
#                  ('share/jupyter/nbextensions/geppetto_connector/geppetto/less',lessmatches),
#                  ('share/jupyter/nbextensions/geppetto_connector/geppetto/js',jsmatches),
#                  ('share/jupyter/nbextensions/geppetto_connector/geppetto/images',imagesmatches)