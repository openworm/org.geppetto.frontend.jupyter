from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import os
import tornado.websocket
import tornado.web
import json

def _jupyter_server_extension_paths():
    return [{
        "module": "geppettoJupyter"
    }]

# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        # the path is relative to the `my_fancy_module` directory
        src="",
        # directory in the `nbextension/` namespace
        dest="geppettoJupyter",
        # _also_ in the `nbextension/` namespace
        require="geppettoJupyter/index")]

class GeppettoHandler(IPythonHandler):
    def get(self):
        template = os.path.join(os.path.dirname(__file__), 'geppetto/src/main/webapp/templates/dist/geppetto.vm')
        print(template)
        self.write(open(template).read())


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message({"type":"client_id","data":"{\"clientID\":\"Connection161\"}"})

    def on_message(self, message):
        jsonMessage = json.loads(message)
        if (jsonMessage['type'] == 'geppetto_version'):
            #Where do we get the geppetto version from?
            self.write_message({"requestID":jsonMessage['requestID'],"type":"geppetto_version","data":"{\"geppetto_version\":\"0.3.1\"}"});

    def on_close(self):
        pass

def load_jupyter_server_extension(nbapp):
    nbapp.log.info("Geppetto Jupyter extension is running!")

    web_app = nbapp.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/geppetto')
    web_app.add_handlers(host_pattern, [(route_pattern, GeppettoHandler)])

    websocket_pattern = url_path_join(web_app.settings['base_url'], '/org.geppetto.frontend/GeppettoServlet')
    web_app.add_handlers(host_pattern, [(websocket_pattern, WebSocketHandler)])

    web_app.add_handlers(host_pattern, [(r"/geppetto/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'geppetto/src/main/webapp/')})])
