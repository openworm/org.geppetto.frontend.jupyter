#!/usr/bin/env python
""" generated source for module ConnectionHandler """
from __future__ import print_function

import logging

from jupyter_geppetto import settings
from pygeppetto.constants import GeppettoErrorCodes
from pygeppetto.managers.geppetto_manager import GeppettoManager
from pygeppetto.model.exceptions import GeppettoExecutionException
from pygeppetto.model.model_serializer import GeppettoSerializer
from pygeppetto.model.services.data_manager import DataManagerHelper

from .outbound_messages import OutboundMessages


class GeppettoHandlerTypedException(Exception):
    def __init__(self, msg, msg_type=None, exc=None):
        Exception.__init__(self, msg)
        self.payload = msg
        self.exc = exc
        self.msg_type = msg_type


#
class GeppettoHandler(object):
    """ generated source for class ConnectionHandler """
    simulationServerConfig = None

    geppettoManager = None

    #  the geppetto project active for this connection
    geppettoProject = None

    # 
    # 	 * @param websocketConnection
    # 	 * @param geppettoManager
    # 	 
    def __init__(self):
        """ generated source for method __init__ """
        self.geppettoManager = GeppettoManager()  # TODO manage geppettoManager instance

    # 
    # 	 * @param requestID
    # 	 * @param projectId
    # 	 
    def loadProjectFromId(self, requestID, projectId, experimentId):
        """ generated source for method loadProjectFromId """
        dataManager = DataManagerHelper.getDataManager()
        try:
            geppettoProject = dataManager.getGeppettoProjectById(projectId)
            if self.geppettoProject == None:
                raise GeppettoHandlerTypedException(OutboundMessages.ERROR_LOADING_PROJECT,
                                                     "Project not found")
            else:
                self.loadGeppettoProject(requestID, self.geppettoProject, experimentId)
        except Exception as e:
            raise GeppettoHandlerTypedException(OutboundMessages.ERROR_LOADING_PROJECT, "")

    def loadGeppettoProject(self, requestID, geppettoProject, experimentId):
        raise NotImplemented()

    # 
    # 	 * @param requestID
    # 	 * @param projectId
    # 	 * @param experimentId
    # 	 * @param dataSourceServiceId
    # 	 * @param variableId
    # 	 * @throws GeppettoExecutionException
    # 	 
    def resolveImportType(self, requestID, projectId, typePaths):
        """ generated source for method resolveImportType """
        geppettoProject = self.retrieveGeppettoProject(projectId)
        try:
            geppettoModel = self.geppettoManager.resolve_import_type(typePaths, geppettoProject)
            return GeppettoSerializer.serializeToJSON(geppettoModel, True)
        except IOError as e:
            self.error(e, "Error importing type " + typePaths)
        except GeppettoExecutionException as e:
            self.error(e, "Error importing type " + typePaths)

    #
    # 	 * @param requestID
    # 	 * @param projectId
    # 	 * @param experimentId
    # 	 * @param path
    #
    def resolveImportValue(self, requestID, projectId, experimentId, path):
        """ generated source for method resolveImportValue """
        geppettoProject = self.retrieveGeppettoProject(projectId)
        experiment = self.retrieveExperiment(experimentId, geppettoProject)
        try:
            geppettoModel = self.geppettoManager.resolve_import_value(path, experiment, geppettoProject)
            return GeppettoSerializer.serializeToJSON(geppettoModel, True)
        except IOError as e:
            self.error(e, "Error importing value " + path)
        except GeppettoExecutionException as e:
            self.error(e, "Error importing value " + path)

    #
    # 	 * @param experimentID
    # 	 * @param geppettoProject
    # 	 * @return
    # 	 
    def retrieveExperiment(self, experimentID, geppettoProject):
        """ generated source for method retrieveExperiment """
        theExperiment = None
        #  Look for experiment that matches id passed
        for e in geppettoProject.getExperiments():
            if e.getId() == experimentID:
                #  The experiment is found
                theExperiment = e
                break
        return theExperiment

    # 
    # 	 * @param projectId
    # 	 * @return
    # 	 
    def retrieveGeppettoProject(self, projectId):
        """ generated source for method retrieveGeppettoProject """
        dataManager = DataManagerHelper.getDataManager()
        return dataManager.getGeppettoProjectById(projectId)


    # 
    # 	 * @param exception
    # 	 * @param errorMessage
    # 	 
    def error(self, exception: Exception, errorMessage):
        """ generated source for method error """
        exceptionMessage = ""
        if exception != None:
            exceptionMessage = str(exception)
        error = Error(GeppettoErrorCodes.EXCEPTION, errorMessage, exceptionMessage, 0)
        logging.error(errorMessage, exception)

        raise GeppettoHandlerTypedException(OutboundMessages.ERROR, error)

    # 
    # 	 * @param requestID
    # 	 * @param exception
    # 	 * @param errorMessage
    # 	 
    def info(self, requestID, message):
        """ generated source for method info """
        logging.info(message)
        raise GeppettoHandlerTypedException(OutboundMessages.INFO_MESSAGE, message)

    #
    # 	 * @param geppettoProject
    # 	 * @throws GeppettoExecutionException
    # 	 
    def setConnectionProject(self, geppettoProject):
        """ generated source for method setConnectionProject """
        if self.geppettoProject != None:
            self.geppettoManager.close_project(self.geppettoProject)
        self.geppettoProject = geppettoProject

    def getVersionNumber(self, requestID):
        return settings.geppetto_version


class Error(object):
    """ generated source for class Error """

    def __init__(self, errorCode, errorMessage, jsonExceptionMsg, id):
        """ generated source for method __init__ """
        self.error_code = errorCode.__str__()
        self.message = errorMessage
        self.exception = jsonExceptionMsg
        self.id = id
