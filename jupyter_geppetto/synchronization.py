"""
synchronization.py
"""
import traceback

import logging
from jupyter_geppetto import jupyter_geppetto
import time
import threading
import importlib
import json


def startSynchronization(scope):
    timer = LoopTimer(0.3,scope)
    timer.start()
    while not timer.started:
        time.sleep(0.001)

class LoopTimer(threading.Thread):
    """
    a Timer that calls f every interval

    A thread that checks all the variables that we are synching between Python and Javascript and if 
    these variables have changed on the Python side will propagate the changes to Javascript

    TODO This code should move to a generic geppetto class since it's not NetPyNE specific
    """

    def __init__(self, interval, scope, fun=None):
        """
        @param interval: time in seconds between call to fun()
        @param fun: the function to call on timer update
        """
        self.started = False
        self.interval = interval
        self.scope = scope
        if fun == None:
            fun = self.process_events
        self.fun = fun
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        self.started = True
        while True:# from netpyne_ui import neuron_utils
            self.fun()
            time.sleep(self.interval)

    def process_events(self):
        try:
            for model, synched_component in list(jupyter_geppetto.synched_models.items()):
                modelValue=None
                if model != '':
                    try:
                        modelValue = eval(model, globals(), self.scope)
                        #logging.debug("Evaluating "+model+" = ")
                        #logging.debug(modelValue)
                        
                    except KeyError:
                        pass
                        #logging.debug("Error evaluating "+model+", don't worry, most likely the attribute is not set in the current model")

                if modelValue==None:
                    modelValue=""
                
                synched_component.value = json.dumps(modelValue)

        except Exception as exception:
            logging.exception(
                "Error on Sync Mechanism for non-sim environment thread")
            raise
