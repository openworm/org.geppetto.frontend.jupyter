'''
Settings for the module. Change right after importing, if needed.
'''

# The path of the geppetto client. Relative path is from the application root
geppetto_webapp_file = 'ComponentsInitialization.js'

# The path of the template. It should be relative to the webapp path
template_path = 'build/geppetto.vm'
# The path of the Jupyter notebook file
notebook_path = 'notebook.ipynb'
# Server host pattern
host_pattern = '.*$'

webapp_root_paths = ['/geppetto']

home_page = '/geppetto'

geppetto_servlet_path_name = 'GeppettoServlet'

geppetto_version = "0.4.2"  # FIXME the hardcoded version must be changed

debug = False


class websocket:
    compression_enabled = False
    min_message_length_for_compression = 200


class Resources:
    ERROR_LOADING_PROJECT_MESSAGE = "Invalid project file. Double check the information you have entered and try again."

    ERROR_DOWNLOADING_MODEL = "Format not supported"

    UNSUPPORTED_OPERATION = "This deployment of Geppetto doesn't support this operation. Contact info@geppetto.org for more information."

    VOLATILE_PROJECT = "The operation cannot be executed on a volatile project. If you wish to persist the project press the star icon at the top."
