import jupyter_geppetto.handlers as handlers

routes = []


class Route:
    def __init__(self, path, handler):
        self.path = path
        self.handler = handler


routes.append(Route("/geppetto", handlers.GeppettoHandler))
routes.append(Route("/geppettoprojects", handlers.GeppettoProjectsHandler))
routes.append(Route(r"/geppetto/(.*)", handlers.GeppettoStaticHandler))
routes.append(Route(r"/org.geppetto.frontend/geppetto/(.*)", handlers.GeppettoStaticHandler))


