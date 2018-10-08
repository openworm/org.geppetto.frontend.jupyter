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
from tornado.routing import PathMatches
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
        # id=self.get_argument("id", None)
        # id = "jupyter_geppetto"
        id = "netpyne_ui"
        if id:
            # Create initial ipynb if it doesn't exist
            if not os.path.isfile('notebook.ipynb'):
                nb0 = new_notebook(cells=[],
                                metadata={'language': 'python',})
                f = codecs.open('notebook.ipynb', encoding='utf-8', mode='w')
                nbf.write(nb0, f, 4)
                f.close()

            
            path = 'geppetto/src/main/webapp/build/geppetto.vm'  # always use slash
            # template = pkg_resources.resource_filename('jupyter_geppetto', path)
            template = pkg_resources.resource_filename(id, path)
            # template = os.path.join(os.path.dirname(__file__), 'geppetto/src/main/webapp/build/geppetto.vm')
            self.write(open(template).read())
        else:
            self.log.warning('Package to load missing in the url')
            self.write('Package to load missing in the url')


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
            self.write_message({"requestID": jsonMessage[
                               'requestID'], "type": "geppetto_version", "data": "{\"geppetto_version\":\"0.4.1\"}"})

    def on_close(self):
        pass


def load_jupyter_server_extension(nbapp):
    try:
        
        nbapp.log.info("Geppetto Jupyter extension is running!")

        path = 'geppetto/src/main/webapp/'  # always use slash
        # template2 = pkg_resources.resource_filename('jupyter_geppetto', path)
        template2 = pkg_resources.resource_filename('netpyne_ui', path)

        web_app = nbapp.web_app
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

        # web_app.add_handlers(host_pattern, [(r"/geppetto/(.*)", tornado.web.StaticFileHandler, {
        #                     'path': os.path.join(os.path.dirname(__file__), 'geppetto/src/main/webapp/')})])
        web_app.add_handlers(host_pattern, [(r"/geppetto/(.*)", tornado.web.StaticFileHandler, {
                             'path': template2})])
        
        # web_app.add_handlers(host_pattern, [(r"/org.geppetto.frontend/geppetto/(.*)", tornado.web.StaticFileHandler, {
        #     'path': os.path.join(os.path.dirname(__file__), 'geppetto/src/main/webapp/')})])
        web_app.add_handlers(host_pattern, [(r"/org.geppetto.frontend/geppetto/(.*)", tornado.web.StaticFileHandler, {
            'path': template2})])
    except Exception:
        nbapp.log.info('Error on Geppetto Server extension')
        traceback.print_exc()
