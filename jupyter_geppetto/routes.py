from jupyter_geppetto import handlers
from jupyter_geppetto.webapi import Route
routes = []



def get(fn, path):
    '''Annotation for get paths'''
    fn.path = path


routes.append(Route("/geppetto", handlers.GeppettoHandler))
routes.append(Route("/geppettoprojects", handlers.GeppettoProjectsHandler))
routes.append(Route(r"/geppetto/(.*)", handlers.GeppettoStaticHandler))
routes.append(Route(r"/org.geppetto.frontend/geppetto/(.*)", handlers.GeppettoStaticHandler))


