import setuptools
from glob import glob

#This block copies resources to the server (/usr/local/share/jupyter/nbextensions/)
data_files = []
data_files.append(('share/jupyter/nbextensions/geppettoJupyter', glob('src/geppettoJupyter/geppetto/src/main/webapp/build/*.js')))
data_files.append(('share/jupyter/nbextensions/geppettoJupyter', glob('src/geppettoJupyter/geppetto/src/main/webapp/build/*.vm')))
data_files.append(('share/jupyter/nbextensions/geppettoJupyter', glob('src/geppettoJupyter/geppetto/src/main/webapp/build/fonts/*')))

data_files.append(('share/jupyter/nbextensions/geppettoJupyter', glob('src/geppettoJupyter/geppettoJupyter.css')))
data_files.append(('share/jupyter/nbextensions/geppettoJupyter', glob('src/geppettoJupyter/GeppettoJupyter.js')))
data_files.append(('share/jupyter/nbextensions/geppettoJupyter', glob('src/geppettoJupyter/index.js')))
data_files.append(('share/jupyter/nbextensions/geppettoJupyter', glob('src/geppettoJupyter/overwrite_get_msg_cell.js')))

setuptools.setup(
    name="jupyter_geppetto",
    version="0.3.9",
    url="https://github.com/openworm/org.geppetto.frontend.jupyter",
    author="The Geppetto Development Team",
    author_email="info@geppetto.org",
    description="Geppetto extension for Jupyter notebook",
    license="MIT",
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    data_files=data_files,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    install_requires=[
        'ipython>=4.0.0,<6.0.0',
        'jupyter_client>=4.0.0,<5.0.0',
        'notebook>=4.0.0,<5.0.0',
        'nbconvert>=4.0.0, <5.0.0',
        'ipywidgets>=5.1.5, <6.0'
    ],
)
