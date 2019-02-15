from notebook.base.handlers import IPythonHandler
import tornado
import tornado.web
import os
import logging

webapp_path = './webapp/'
template_path = webapp_path + 'build/geppetto.vm'


class GeppettoHandler(IPythonHandler):

    def get(self, *args):
        try:
            template = template_path
            self.write(open(template).read())
        except Exception:
            logging.info('Error on Geppetto Server extension')
            raise


class GeppettoProjectsHandler(IPythonHandler):

    def get(self):
        self.write({})


class GeppettoStaticHandler(tornado.web.StaticFileHandler):
    '''Serves the Geppetto web application'''
    
    def initialize(self):
        if not os.path.exists(webapp_path):
            raise Exception("Webapp path not recognized: {}. Check configuration on file {}".format(
                            webapp_path, os.path.dirname(os.path.realpath(__file__))))
        # self.log.debug("Initializing static resources from {}".format(webapp_path))
        tornado.web.StaticFileHandler.initialize(self, webapp_path)
