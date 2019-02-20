'''
Settings for the module. Change right after importing, if needed.
'''
import glob
import os

# The path of the geppetto client. Relative path is from the application root
geppetto_webapp_file = 'GEPPETTO.Backend.js'

# The path of the template. It should be relative to the webapp path
template_path = 'build/geppetto.vm'
# The path of the Jupyter notebook file
notebook_path = 'notebook.ipynb'
# Server host pattern
host_pattern = '.*$'

webapp_root_paths = ['/geppetto']

home_page = '/geppetto'

geppetto_servlet_path_name = 'GeppettoServlet'

geppetto_version = "0.4.2" # FIXME the hardcoded version must be changed

debug = True
