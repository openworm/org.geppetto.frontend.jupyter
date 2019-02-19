from notebook.base.handlers import IPythonHandler
from tornado.websocket import WebSocketHandler
import logging
from .settings import webapp_directory_default, template_path
from .webapi import get, RouteManager
import json
import codecs
import jupyter_geppetto.settings as settings


class GeppettoController:

    @get('/geppettoprojects')
    def getProjects(self, **kwargs):
        # TODO still no project handling here.
        return {}

    @get('/geppetto')
    def getProject(self, **kwargs):
        try:
            template = template_path
            return open(template).read()
        except Exception:
            logging.info('Error on Geppetto Server extension')
            raise


class GeppettoWebSocketHandler(WebSocketHandler):
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
        logging.debug('Open websocket')
        self.write_message(json.dumps(self.CLIENT_ID))
        # 2 -> Check user privileges
        self.write_message(json.dumps(self.PRIVILEGES))

    def on_message(self, message):

        payload = json.loads(message)
        assert 'type' in payload, 'Websocket message without type received: {}'.format(payload)

        logging.debug('Websocket message received: {}', payload['type'])
        # TODO only the geppetto_version message is handled by now
        if (payload['type'] == 'geppetto_version'):

            self.write_message(json.dumps({
                "requestID": payload['requestID'],
                "type": "geppetto_version",
                "data": json.dumps({
                        "geppetto_version": settings.geppetto_version
                })
            }))
        else:
            raise Exception('Message type not handled', payload['type'])

    # def on_close(self):
    #     self.write_message(json.dumps({
    #         'type': 'socket_closed',
    #         'data': ''
    #     }))


