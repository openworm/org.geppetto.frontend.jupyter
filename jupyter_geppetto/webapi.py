from notebook.base.handlers import IPythonHandler
from tornado.web import RequestHandler
class JupyterGeppettoHandler(RequestHandler):
    pass

class Route:
    def __init__(self, path, handler):
        self.path = path
        self.handler = handler