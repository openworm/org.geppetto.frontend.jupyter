'''
Settings for the module. Change right after importing, if needed.
'''

# The path of the geppetto client. Relative path is from the application root
webapp_directory_default = './webapp/'
# The path of the template. It should be relative to the webapp path
template_path = webapp_directory_default + 'build/geppetto.vm'
# The path of the Jupyter notebook file
notebook_path = 'notebook.ipynb'
# Server host pattern
host_pattern = '.*$'

webapp_root_path = 'geppetto'

geppetto_version = "0.4.2" # FIXME the hardcoded version must be changed

debug = True
