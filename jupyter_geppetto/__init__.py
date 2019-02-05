import os.path
import json
import codecs
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import tornado.websocket
import tornado.web

import logging
from nbformat.v4.nbbase import new_notebook
import pkg_resources
import traceback
from jupyter_geppetto.utils import createNotebook

notebook_path = 'notebook.ipynb'


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


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    CLIENT_ID = {
        'type': 'client_id',
        'data': json.dumps({
            'clientID': 'Connection1'
        })
    }

    PRIVILEGES = {
        'type': 'user_privileges',
        'data': json.dumps({
            "user_privileges": json.dumps({
                "userName": "Python User",
                "loggedIn": True,
                "hasPersistence": False,
                "privileges": [
                    "READ_PROJECT",
                    "DOWNLOAD",
                    "DROPBOX_INTEGRATION",
                    "RUN_EXPERIMENT",
                    "WRITE_PROJECT"
                ]
            })
        })
    }

    def open(self):
        # 1 -> Send the connection
        self.write_message(json.dumps(self.CLIENT_ID))
        # 2 -> Check user privileges
        self.write_message(json.dumps(self.PRIVILEGES))

    def on_message(self, message):
        payload = json.loads(message)

        if (payload['type'] == 'geppetto_version'):

            self.write_message(json.dumps({
                "requestID": payload['requestID'],
                "type": "geppetto_version",
                "data": json.dumps({
                        "geppetto_version": "0.4.2"
                })
            }))

    # def on_close(self):
    #     self.write_message(json.dumps({
    #         'type': 'socket_closed',
    #         'data': ''
    #     }))


def _add_routes(nbapp, routes, host_pattern = '.*$'):
    for route in routes:
        nbapp.log.info('Adding http route {}'.format(route.path))
        nbapp.web_app.add_handlers(host_pattern, [(route.path, route.handler)])

def load_jupyter_server_extension(nbapp):

    try:
        nbapp.log.info("Starting Geppetto Jupyter extension")

        web_app = nbapp.web_app
        config = web_app.settings['config']

        if not os.path.isfile(notebook_path):
            nbapp.log.info("Creating notebook {}".format(notebook_path))
            createNotebook(notebook_path)
        else:
            nbapp.log.info("Using notebook {}".format(notebook_path))

        host_pattern = '.*$'
        # TODO implement a hook mechanism to get routes from outside
        from jupyter_geppetto.routes import routes

        if 'library' in config:
            modules = config['library'].split(',')
            for moduleName in modules:
                module = __import__(moduleName)
                nbapp.log.info('Initializing library module {}', moduleName)
                if hasattr(module, 'routes'):
                    nbapp.log.info('Adding routes from module {}', moduleName)
                    routes += module.routes

        _add_routes(nbapp, routes, host_pattern)

        websocket_pattern = url_path_join(
            web_app.settings['base_url'], '/org.geppetto.frontend/GeppettoServlet')
        web_app.add_handlers(
            host_pattern, [(websocket_pattern, WebSocketHandler)])

        nbapp.log.info("Geppetto Jupyter extension is running!")

    except Exception:
        nbapp.log.info('Error on Geppetto Server extension')
        traceback.print_exc()