from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import os
import tornado.websocket
import tornado.web
import json

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
        dest="geppetto_connector")]
    
class HelloWorldHandler(IPythonHandler):
    def get(self):
        #self.write(self.render_template('./static/geppetto/templates/dist/geppetto.vm'))
        self.write(open(os.path.join(os.path.dirname(__file__), 'static/geppetto/templates/dist/geppetto.vm')).read())

     
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
    nbapp.log.info("my module enabled!")
    
    web_app = nbapp.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/hello')
    web_app.add_handlers(host_pattern, [(route_pattern, HelloWorldHandler)])
    
    websocket_pattern = url_path_join(web_app.settings['base_url'], '/GeppettoServlet')
    web_app.add_handlers(host_pattern, [(websocket_pattern, WebSocketHandler)])
    
    web_app.add_handlers(host_pattern, [(r"/geppetto/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'static/geppetto/')})])
    
    