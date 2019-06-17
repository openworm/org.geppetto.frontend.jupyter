import logging

from ipykernel.jsonutil import json_clean
# from jupyter_client import session
from zmq.utils import jsonapi


def convertToJS(content):
    # return session.json_packer(content).decode("utf-8")
    # Old way: this needs to be deleted if the above line is enough
    return jsonapi.dumps(json_clean(content)).decode("utf-8")


def convertToPython(content):
    # return session.json_unpacker(content)
    # Old way: this needs to be deleted if the above line is enough
    return jsonapi.loads(content)


def exception_to_string(exc_info):
    import IPython.core.ultratb
    tb = IPython.core.ultratb.VerboseTB()
    return tb.text(*exc_info)


def getJSONError(message, exc_info):
    data = {}
    data['type'] = 'ERROR'
    data['websocket'] = message

    if isinstance(exc_info, str):
        details = exc_info
    else:
        details = exception_to_string(exc_info)
    data['details'] = details
    return data


def getJSONReply():
    data = {}
    data['type'] = 'OK'
    return data


def configure_logging():
    try:
        # Configure log
        logger = logging.getLogger()
        fhandler = logging.FileHandler(filename='app.log', mode='a')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s')
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
        logger.setLevel(logging.DEBUG)
        logging.debug('Log configured')
    except Exception as exception:
        logging.exception("Unexpected error while initializing Geppetto from Python:")
        logging.error(exception)


def createNotebook(filename):
    import nbformat as nbf
    from nbformat.v4.nbbase import new_notebook
    import codecs
    nb0 = new_notebook(cells=[], metadata={'language': 'python', })
    f = codecs.open(filename, encoding='utf-8', mode='w')
    nbf.write(nb0, f, 4)
    f.close()


import tornado
from tornado.routing import Matcher
from jupyter_geppetto.settings import host_pattern, geppetto_servlet_path_name
from jupyter_geppetto.websocket_connection import GeppettoMessageHandler


class GeppettoServletMatcher(Matcher):

    def match(self, request):
        if geppetto_servlet_path_name == request.path[-len(geppetto_servlet_path_name):]:
            return {}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def start_notebook_server(port=3456):
    app = tornado.web.Application([
        (r"/", MainHandler),
        (host_pattern, [(GeppettoServletMatcher(), GeppettoMessageHandler)])
    ])
    app.listen(port)
    # tornado.ioloop.IOLoop.current().start()
