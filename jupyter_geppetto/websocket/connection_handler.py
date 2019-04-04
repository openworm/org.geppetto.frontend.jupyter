#!/usr/bin/env python
""" generated source for module ConnectionHandler """
from __future__ import print_function

import logging

from pygeppetto.managers.geppetto_manager import GeppettoManager
from pygeppetto.model.exceptions import GeppettoExecutionException
from pygeppetto.model.model_serializer import GeppettoSerializer
from pygeppetto.model.services.data_manager import DataManagerHelper

from .outbound_messages import OutboundMessages


#
class ConnectionHandler(object):
    """ generated source for class ConnectionHandler """
    simulationServerConfig = None
    websocketConnection = None
    geppettoManager = None

    #  the geppetto project active for this connection
    geppettoProject = None

    # 
    # 	 * @param websocketConnection
    # 	 * @param geppettoManager
    # 	 
    def __init__(self, websocketConnection, geppettoManager):
        """ generated source for method __init__ """
        self.websocketConnection = websocketConnection
        self.geppettoManager = GeppettoManager(geppettoManager)

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
                self.websocketConnection.sendMessage(requestID, OutboundMessages.ERROR_LOADING_PROJECT,
                                                     "Project not found")
            else:
                self.loadGeppettoProject(requestID, self.geppettoProject, experimentId)
        except Exception as e:
            self.websocketConnection.sendMessage(requestID, OutboundMessages.ERROR_LOADING_PROJECT, "")

    def loadGeppettoProject(requestID, geppettoProject, experimentId):
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
            self.websocketConnection.sendMessage(requestID, OutboundMessages.IMPORT_TYPE_RESOLVED,
                                                 GeppettoSerializer.serializeToJSON(geppettoModel, True))
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
            self.websocketConnection.sendMessage(requestID, OutboundMessages.IMPORT_VALUE_RESOLVED,
                                                 GeppettoSerializer.serializeToJSON(geppettoModel, True))
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

    def getGson(self):
        """ generated source for method getGson """
        import json
        return json

    # 
    # 	 * @param exception
    # 	 * @param errorMessage
    # 	 
    def error(self, exception, errorMessage):
        """ generated source for method error """
        exceptionMessage = ""
        if exception != None:
            exceptionMessage = exception.getMessage() if exception.getCause() == None else exception.__str__()
        #  Error error = new self.error(GeppettoErrorCodes.EXCEPTION, errorMessage, exceptionMessage, 0);
        logging.self.error(errorMessage, exception)
        #  websocketConnection.sendMessage(null, OutboundMessages.ERROR, getGson().toJson(error));

    # 
    # 	 * @param requestID
    # 	 * @param exception
    # 	 * @param errorMessage
    # 	 
    def info(self, requestID, message):
        """ generated source for method info """
        logging.info(message)
        self.websocketConnection.sendMessage(requestID, OutboundMessages.INFO_MESSAGE, self.getGson().toJson(message))

    #
    # 	 * @param geppettoProject
    # 	 * @throws GeppettoExecutionException
    # 	 
    def setConnectionProject(self, geppettoProject):
        """ generated source for method setConnectionProject """
        if self.geppettoProject != None:
            self.geppettoManager.closeProject(None, self.geppettoProject)
        self.geppettoProject = geppettoProject
