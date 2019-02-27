import os.path
import json
import codecs
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import tornado.websocket
import tornado.web
import nbformat as nbf
import logging
from nbformat.v4.nbbase import new_notebook
import pkg_resources
import traceback


def _jupyter_server_extension_paths():
    
    return [{
        "module": "jupyter_geppetto"
    }]

def _jupyter_nbextension_paths():
    
    return [dict(
        section="notebook",
        # the path is relative to the `jupyter_geppetto` directory
        src="",
        # directory in the `nbextension/` namespace
        dest="jupyter_geppetto",
        # _also_ in the `nbextension/` namespace
        require="jupyter_geppetto/index")]


class GeppettoHandler(IPythonHandler):

    def get(self):
        try:
            config = self.application.settings['config']
            if 'library' in config:
                # Create initial ipynb if it doesn't exist
                if not os.path.isfile('notebook.ipynb'):
                    nb0 = new_notebook(cells=[],
                                    metadata={'language': 'python',})
                    f = codecs.open('notebook.ipynb', encoding='utf-8', mode='w')
                    nbf.write(nb0, f, 4)
                    f.close()

                template = pkg_resources.resource_filename(config['library'], '../geppetto-hnn/build/geppetto.vm')
                self.write(open(template).read())
            else:
                self.log.warning('Package to load missing in the url')
                self.write('Package to load missing in the url')
        except Exception:
            self.log.info('Error on Geppetto Server extension')
            traceback.print_exc()      

class GeppettoProjectsHandler(IPythonHandler):

    def get(self):
        self.write({})

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        # 1 -> Send the connection
        self.write_message(
            {"type": "client_id", "data": "{\"clientID\":\"Connection1\"}"})
        # 2 -> Check user privileges
        self.write_message(
            {"type": "user_privileges", "data": "{\"user_privileges\": \"{\\\"userName\\\":\\\"Python User\\\",\\\"loggedIn\\\":true,\\\"hasPersistence\\\":false,\\\"privileges\\\":[\\\"READ_PROJECT\\\",\\\"DOWNLOAD\\\",\\\"DROPBOX_INTEGRATION\\\", \\\"RUN_EXPERIMENT\\\", \\\"WRITE_PROJECT\\\"]}\"}"})

    def on_message(self, message):
        jsonMessage = json.loads(message)
        if (jsonMessage['type'] == 'geppetto_version'):
            # Where do we get the geppetto version from?
            self.write_message({"requestID": jsonMessage['requestID'], "type": "geppetto_version", "data": "{\"geppetto_version\":\"0.4.1\"}"})

    def on_close(self):
        pass

def load_jupyter_server_extension(nbapp):
    
    try:
        nbapp.log.info("Geppetto Jupyter extension is running!")

        web_app = nbapp.web_app
        config = web_app.settings['config']

        host_pattern = '.*$'
        route_pattern = url_path_join(web_app.settings['base_url'], '/geppetto')
        web_app.add_handlers(host_pattern, [(route_pattern, GeppettoHandler)])

        route_pattern_geppetto_projects = url_path_join(
            web_app.settings['base_url'], '/geppettoprojects')
        web_app.add_handlers(
            host_pattern, [(route_pattern_geppetto_projects, GeppettoProjectsHandler)])

        websocket_pattern = url_path_join(
            web_app.settings['base_url'], '/org.geppetto.frontend/GeppettoServlet')
        web_app.add_handlers(host_pattern, [(websocket_pattern, WebSocketHandler)])

        if 'library' in config:
            nbapp.log.info("Geppetto Jupyter extension loading library: " + str(config['library']))
            template = pkg_resources.resource_filename(config['library'], 'geppetto/src/main/webapp/') # always use slash

            resources_pattern = url_path_join(web_app.settings['base_url'], r"/org.geppetto.frontend/geppetto/(.*)")
            web_app.add_handlers(host_pattern, [(resources_pattern, tornado.web.StaticFileHandler, {'path': template})])

            resources_pattern2 = url_path_join(web_app.settings['base_url'], r"../geppetto-hnn/(.*)")
            web_app.add_handlers(host_pattern, [(resources_pattern2, tornado.web.StaticFileHandler, {'path': template})])
        else:
            nbapp.log.warning('Package to load missing in the url')
            raise Exception
    
    except Exception:
        nbapp.log.info('Error on Geppetto Server extension')
        traceback.print_exc()