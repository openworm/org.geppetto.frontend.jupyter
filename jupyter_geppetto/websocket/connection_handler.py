#!/usr/bin/env python
""" generated source for module ConnectionHandler """
from __future__ import print_function

import json
import logging

from jupyter_geppetto import settings
from pygeppetto.constants import GeppettoErrorCodes
from pygeppetto.managers.geppetto_manager import GeppettoManager
from pygeppetto.model.exceptions import GeppettoExecutionException
from pygeppetto.model.model_serializer import GeppettoSerializer
from pygeppetto.services.data_manager import DataManagerHelper

from . import outbound_messages as OutboundMessages


class GeppettoHandlerTypedException(Exception):
    def __init__(self, msg, msg_type=None, exc=None):
        Exception.__init__(self, msg)
        self.payload = msg
        self.exc = exc
        self.msg_type = msg_type


# See https://github.com/openworm/org.geppetto.frontend/blob/development/src/main/java/org/geppetto/frontend/controllers/ConnectionHandler.java#L867
class ConnectionHandler(object):
    """ generated source for class ConnectionHandler """
    simulationServerConfig = None

    geppettoManager = GeppettoManager()  # TODO manage geppettoManager instance

    def __init__(self, websocket_connection):
        self.websocket_connection = websocket_connection

    def loadProjectFromUrl(self, requestID, urlString):
        dataManager = DataManagerHelper.getDataManager()

        geppettoProject = dataManager.get_project_from_url(urlString)

        if geppettoProject == None:
            raise GeppettoHandlerTypedException(OutboundMessages.ERROR_LOADING_PROJECT,
                                                "Project not found")
        else:
            return self.loadGeppettoProject(requestID, geppettoProject, -1)

    def loadProjectFromContent(self, requestID, projectContentJSON):
        dataManager = DataManagerHelper.getDataManager()

        geppettoProject = dataManager.getProjectFromJson(projectContentJSON)
        self.loadGeppettoProject(requestID, geppettoProject, -1)

    def loadGeppettoProject(self, requestID, geppettoProject, experimentId):

        try:
            readOnly = geppettoProject.volatile  # TODO implement logic related to user projects which are not readonly

            self.geppettoManager.load_project(geppettoProject)
            # Here the project is loaded: a runtime project is created with its model

            geppettoProject.geppettoModel = {
                'id': geppettoProject.geppettoModel.id,
                'type': 'MODEL'
            }  # There is something odd here: we are  sending the project without the model, although the model is there. It's the same in Java anyway, we are just having a PersistedData placeholder there. Why not serialize the model together with the project?

            project_message_update = json.dumps({
                'persisted': not geppettoProject.volatile,
                'project': geppettoProject.__dict__,
                'isReadOnly': readOnly
            })
            self.websocket_connection.send_message(requestID, OutboundMessages.PROJECT_LOADED, project_message_update)

            runtime_project = self.geppettoManager.get_runtime_project(geppettoProject)

            geppettoModelJSON = GeppettoSerializer.serialize(
                runtime_project.model, False).decode('UTF-8')
            self.websocket_connection.send_message(requestID, OutboundMessages.GEPPETTO_MODEL_LOADED, geppettoModelJSON)

            GeppettoSerializer.serialize(
                runtime_project.model, True)  # This is setting synched to true on the model objects

            # TODO handle experiment
        except Exception as e:
            self.error(e, "Could not load geppetto project")

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

    def resolveImportValue(self, requestID, projectId, experimentId, path):
        """ generated source for method resolveImportValue """
        geppettoProject = self.retrieveGeppettoProject(projectId)
        experiment = self.retrieveExperiment(experimentId, geppettoProject)
        try:
            geppettoModel = self.geppettoManager.resolve_import_value(path, geppettoProject, experiment)
            return GeppettoSerializer.serialize(geppettoModel, True).decode('utf-8')
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
