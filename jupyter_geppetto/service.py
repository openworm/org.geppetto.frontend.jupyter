from jupyter_geppetto import settings
from notebook.utils import url_path_join
import logging

class PathService:
    webapp_directory = ''

    @classmethod
    def get_webapp_directory(cls):
        if not cls.webapp_directory:
            import glob, os
            cls.webapp_directory = os.path.dirname(glob.glob('*/' + settings.geppetto_webapp_file)[0])
            logging.info('Webapp directory discovered: {}'.format(cls.webapp_directory))
        return cls.webapp_directory

    @classmethod
    def get_webapp_resource(cls, path):
        return url_path_join(cls.get_webapp_directory(), path)
