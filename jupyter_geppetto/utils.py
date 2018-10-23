import logging
from zmq.utils import jsonapi
from ipykernel.jsonutil import json_clean
import json

def convertToJS(content):
    return jsonapi.dumps(json_clean(content)).decode("utf-8")

def convertToPython(content):
    return jsonapi.loads(content)

def getJSONError(message, details):
    data = {}
    data['type'] = 'ERROR'
    data['message'] = message
    data['details'] = details
    return json.dumps(data)

def getJSONReply():
    data = {}
    data['type'] = 'OK'
    return json.dumps(data)

def configure_logging():
    try:
        # Configure log
        logger = logging.getLogger()
        fhandler = logging.FileHandler(filename='netpyne-ui.log', mode='a')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
        logger.setLevel(logging.DEBUG)
        logging.debug('Log configured')
    except Exception as exception:
        logging.exception("Unexpected error while initializing Geppetto from Python:")
        logging.error(exception)