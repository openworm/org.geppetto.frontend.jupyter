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
host_pattern = '.*$'

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
                        "geppetto_version": "0.4.2" # FIXME the hardcoded version must be changed
                })
            }))

    # def on_close(self):
    #     self.write_message(json.dumps({
    #         'type': 'socket_closed',
    #         'data': ''
    #     }))


def _add_routes(nbapp, routes, host_pattern = '.*$', base_path='/'):


    for route in routes:
        nbapp.log.info('Adding http route {}'.format(route.path))
        route_path = url_path_join(base_path, route.path)
        nbapp.log.info('Complete route url: {}'.format(route_path))
        nbapp.web_app.add_handlers(host_pattern, [(route_path, route.handler)])


def initRoutes(nbapp, base_path):
    # TODO implement a hook mechanism to get routes from outside
    from jupyter_geppetto.routes import routes
    web_app = nbapp.web_app
    config = web_app.settings['config']
    if 'library' in config:
        modules = config['library'].split(',')
        for moduleName in modules:
            nbapp.log.info('Initializing library module {}'.format(moduleName))
            module = __import__(moduleName)

            if hasattr(module, 'routes'):
                nbapp.log.info('Adding routes from module {}'.format(moduleName))
                routes += module.routes

    _add_routes(nbapp, routes, host_pattern, base_path)

    websocket_pattern = url_path_join(
        base_path, '/org.geppetto.frontend/GeppettoServlet')
    nbapp.web_app.add_handlers(
        host_pattern, [(websocket_pattern, WebSocketHandler)])

def load_jupyter_server_extension(nbapp):

    try:
        nbapp.log.info("Starting Geppetto Jupyter extension")



        if not os.path.exists(notebook_path):
            nbapp.log.info("Creating notebook {}".format(notebook_path))
            createNotebook(notebook_path)
        else:
            nbapp.log.info("Using notebook {}".format(notebook_path))



        # base_url = 'base_url' if 'base_url' in config else config['base_url']
        # if base_url:
        #     nbapp.log.info('Found configured base url {}'.format(base_url))




        from tornado.routing import Matcher

        class BasePathRecognitionMatcher(Matcher):
            matched = False

            def __init__(self):
                self.paths = []

            def match(self, request):
                path = request.path
                nbapp.log.info('Trying to match path: {}'.format(path))

                if 'geppetto' != path.split('/')[-1][0:len('geppetto')]:
                    return None # We activate the path initialization only for the first geppetto home call


                base_path = path.split('/geppetto')[0]
                if not base_path or base_path[0] != '/':
                    base_path = '/' + base_path

                nbapp.log.info('Path found: {}'.format(path))
                if base_path in self.paths:
                    return None

                self.paths.append(base_path)
                nbapp.log.info('New context path found: {}. Relative routes will be added.'.format(base_path))
                initRoutes(nbapp, base_path)
                return {}


        class RetryHandler(tornado.web.RequestHandler):

            def get(self):
                self.redirect(self.request.path)

        nbapp.web_app.add_handlers(host_pattern, [(BasePathRecognitionMatcher(), RetryHandler)])
        initRoutes(nbapp, '/')




        nbapp.log.info("Geppetto Jupyter extension is running!")

    except Exception:
        nbapp.log.info('Error on Geppetto Server extension')
        traceback.print_exc()