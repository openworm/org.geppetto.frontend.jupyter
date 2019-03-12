from jupyter_geppetto import settings
from notebook.utils import url_path_join
import logging
import os
class PathService:
    webapp_directory = './webapp/'

    @classmethod
    def get_webapp_directory(cls):
        if not os.path.exists(cls.webapp_directory):
            import glob
            discovered_paths = glob.glob('*/' + settings.geppetto_webapp_file)
            if discovered_paths:
                cls.webapp_directory = os.path.dirname([0])
                logging.info('Webapp directory discovered: {}'.format(cls.webapp_directory))
            else:
                logging.error('Cannot determine webapp directory. PathService won\'t work')
        return cls.webapp_directory

    @classmethod
    def get_webapp_resource(cls, path):
        return url_path_join(cls.get_webapp_directory(), path)
