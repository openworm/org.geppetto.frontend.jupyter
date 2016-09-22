from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler

def _jupyter_server_extension_paths():
    return [{
        "module": "geppetto_connector"
    }]
    
# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        # the path is relative to the `my_fancy_module` directory
        src="static/geppetto_connector",
        # directory in the `nbextension/` namespace
        dest="geppetto_connector",
        # _also_ in the `nbextension/` namespace
        require="geppetto_connector/index")]
    
class HelloWorldHandler(IPythonHandler):
    def get(self):
        self.finish('Hello, world!')


def load_jupyter_server_extension(nbapp):
    nbapp.log.info("my module enabled!")
    
    web_app = nbapp.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/hello')
    web_app.add_handlers(host_pattern, [(route_pattern, HelloWorldHandler)])
    