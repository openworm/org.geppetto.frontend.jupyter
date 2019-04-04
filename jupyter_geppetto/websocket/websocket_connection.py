#!/usr/bin/env python
""" generated source for module WebsocketConnection """
from __future__ import print_function

import json
import logging

from pygeppetto.model.exceptions import GeppettoExecutionException, GeppettoInitializationException

from .connection_handler import ConnectionHandler
# package: org.geppetto.frontend.controllers
#
#  * Class used to process Web Socket Connections. Messages sent from the connecting clients, web socket connections, are received in here.
#  *
#  * @author matteocantarelli
#  *
#
from .inbound_messages import InboundMessages
from .messaging import DefaultMessageSenderFactory
from .outbound_messages import OutboundMessages


class WebsocketMessageHandler:
    """ generated source for class WebsocketMessageHandler """
    session = None
    websocketConnection = None

    def __init__(self, geppetto_manager):
        self.geppettoManager = geppetto_manager
        self.connectionHandler = ConnectionHandler(self, self.geppettoManager)

    def onOpen(self, session, config):
        """ generated source for method onOpen """
        self.userSession = session
        # Expanding binary messages buffer size
        # wsContainer = ContainerProvider.getWebSocketContainer()
        # wsContainer.setDefaultMaxBinaryMessageBufferSize(9999999)
        # wsContainer.setDefaultMaxTextMessageBufferSize(9999999)
        # self.userSession.setMaxTextMessageBufferSize(9999999)
        # self.userSession.setMaxBinaryMessageBufferSize(9999999)
        logging.info("Session Binary size >> " + self.userSession.getMaxBinaryMessageBufferSize())
        logging.info("Session Text size >> " + self.userSession.getMaxTextMessageBufferSize())
        self.messageSender = DefaultMessageSenderFactory.getMessageSender(self.userSession, self)
        #  User permissions are sent when socket is open
        self.connectionHandler.checkUserPrivileges(None)
        # self.connectionID = ConnectionsManager.getInstance().addConnection(self)
        self.sendMessage(None, OutboundMessages.CLIENT_ID, self.connectionID)
        logging.info("Open Connection ...")
        session.addMessageHandler(WebsocketMessageHandler(session, self))

    def onClose(self, session, closeReason):
        self.messageSender.shutdown()
        self.connectionHandler.closeProject()
        logging.info("Closed Connection ...")

    def onError(self, session, thr):
        """ generated source for method onError """
        logging.info("Error Connection ..." + " error: " + thr.getMessage())

    def broadcastSnapshot(self, data, session):
        """ generated source for method broadcastSnapshot """
        logging.info("broadcastBinary: " + data)
        session.getBasicRemote().sendBinary(data)

        #
        # 	 * @param requestID
        # 	 * @param type
        # 	 * @param messages
        #

    def sendMessage(self, requestID, type_, message):
        self.messageSender.sendMessage(requestID, type_, message)

        #
        # 	 * @param requestID
        # 	 * @param type
        # 	 * @param messages
        #

    def sendBinaryMessage(self, requestID, path):
        """ generated source for method sendBinaryMessage """
        self.messageSender.sendFile(path)

    def onMessage(self, message):
        """ generated source for method onMessage """
        msg = message.__str__()
        parameters = None
        experimentId = -1
        projectId = -1
        instancePath = None
        #  de-serialize JSON
        gmsg = json.dumps(msg)
        requestID = gmsg.requestID
        #  switch on messages type
        #  NOTE: each messages handler knows how to interpret the GeppettoMessage data field
        if gmsg.type_.upper() == InboundMessages.GEPPETTO_VERSION:
            self.connectionHandler.getVersionNumber(requestID)
        elif gmsg.type_.upper() == InboundMessages.USER_PRIVILEGES:
            self.connectionHandler.checkUserPrivileges(requestID)
        elif gmsg.type_.upper() == InboundMessages.NEW_EXPERIMENT:
            parameters = json.dumps(gmsg.data)
            projectId = int(parameters.get("projectId"))
            self.connectionHandler.newExperiment(requestID, projectId)
        elif gmsg.type_.upper() == InboundMessages.NEW_EXPERIMENT_BATCH:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.newExperimentBatch(requestID, receivedObject.projectId, receivedObject)
        elif gmsg.type_.upper() == InboundMessages.CLONE_EXPERIMENT:
            parameters = json.dumps(gmsg.data)
            projectId = int(parameters.get("projectId"))
            experimentId = int(parameters.get("experimentId"))
            self.connectionHandler.cloneExperiment(requestID, projectId, experimentId)
        elif gmsg.type_.upper() == InboundMessages.LOAD_PROJECT_FROM_URL:
            self.connectionHandler.loadProjectFromURL(requestID, gmsg.data)
            self.messageSender.reset()
        elif gmsg.type_.upper() == InboundMessages.LOAD_PROJECT_FROM_ID:
            parameters = json.dumps(gmsg.data)
            if parameters.containsKey("experimentId"):
                experimentId = int(parameters.get("experimentId"))
            projectId = int(parameters.get("projectId"))
            self.connectionHandler.loadProjectFromId(requestID, projectId, experimentId)
            self.messageSender.reset()
        elif gmsg.type_.upper() == InboundMessages.LOAD_PROJECT_FROM_CONTENT:
            self.connectionHandler.loadProjectFromContent(requestID, gmsg.data)
            self.messageSender.reset()
        elif gmsg.type_.upper() == InboundMessages.PERSIST_PROJECT:
            parameters = json.dumps(gmsg.data)
            projectId = int(parameters.get("projectId"))
            self.connectionHandler.persistProject(requestID, projectId)
        elif gmsg.type_.upper() == InboundMessages.MAKE_PROJECT_PUBLIC:
            parameters = json.dumps(gmsg.data)
            projectId = int(parameters.get("projectId"))
            isPublic = bool(parameters.get("isPublic"))
            self.connectionHandler.makeProjectPublic(requestID, projectId, isPublic)
        elif gmsg.type_.upper() == InboundMessages.DOWNLOAD_PROJECT:
            parameters = json.dumps(gmsg.data)
            projectId = int(parameters.get("projectId"))
            self.connectionHandler.downloadProject(requestID, projectId)
        elif gmsg.type_.upper() == InboundMessages.SAVE_PROJECT_PROPERTIES:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.saveProjectProperties(requestID, receivedObject.projectId, receivedObject.properties)
        elif gmsg.type_.upper() == InboundMessages.SAVE_EXPERIMENT_PROPERTIES:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.saveExperimentProperties(requestID, receivedObject.projectId,
                                                            receivedObject.experimentId, receivedObject.properties)
        elif gmsg.type_.upper() == InboundMessages.LOAD_EXPERIMENT:
            parameters = json.dumps(gmsg.data)
            experimentId = int(parameters.get("experimentId"))
            projectId = int(parameters.get("projectId"))
            self.connectionHandler.loadExperiment(requestID, experimentId, projectId)
        elif gmsg.type_.upper() == InboundMessages.GET_SCRIPT:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.sendScriptData(requestID, receivedObject.projectId, receivedObject.scriptURL,
                                                  self.websocketConnection)
        elif gmsg.type_.upper() == InboundMessages.GET_DATA_SOURCE_RESULTS:
            url = None
            dataSourceName = None
            try:
                parameters = json.dumps(gmsg.data)
                url = parameters.get("url")
                dataSourceName = parameters.get("data_source_name")
                self.connectionHandler.sendDataSourceResults(requestID, dataSourceName, url, self.websocketConnection)
            except IOError as e:
                self.sendMessage(requestID, OutboundMessages.ERROR_READING_SCRIPT, "")
        elif gmsg.type_.upper() == InboundMessages.GET_EXPERIMENT_STATE:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.getExperimentState(requestID, receivedObject.experimentId, receivedObject.projectId,
                                                      receivedObject.variables)
        elif gmsg.type_.upper() == InboundMessages.DELETE_EXPERIMENT:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.deleteExperiment(requestID, receivedObject.experimentId, receivedObject.projectId)
        elif gmsg.type_.upper() == InboundMessages.RUN_EXPERIMENT:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.runExperiment(requestID, receivedObject.experimentId, receivedObject.projectId)
        elif gmsg.type_.upper() == InboundMessages.SET_WATCHED_VARIABLES:
            receivedObject = json.dumps(gmsg.data)
            try:
                self.connectionHandler.setWatchedVariables(requestID, receivedObject.variables,
                                                           receivedObject.experimentId, receivedObject.projectId,
                                                           receivedObject.watch)
            except GeppettoExecutionException as e:
                self.sendMessage(requestID, OutboundMessages.ERROR_SETTING_WATCHED_VARIABLES, "")
            except GeppettoInitializationException as e:
                self.sendMessage(requestID, OutboundMessages.ERROR_SETTING_WATCHED_VARIABLES, "")
        elif gmsg.type_.upper() == InboundMessages.GET_SUPPORTED_OUTPUTS:
            parameters = json.dumps(gmsg.data)
            experimentId = int(parameters.get("experimentId"))
            projectId = int(parameters.get("projectId"))
            instancePath = parameters.get("instancePath")
            self.connectionHandler.getSupportedOuputs(requestID, instancePath, experimentId, projectId)
        elif gmsg.type_.upper() == InboundMessages.DOWNLOAD_MODEL:
            parameters = json.dumps(gmsg.data)
            experimentId = int(parameters.get("experimentId"))
            projectId = int(parameters.get("projectId"))
            instancePath = parameters.get("instancePath")
            format = parameters.get("format")
            self.connectionHandler.downloadModel(requestID, instancePath, format, experimentId, projectId)
        elif gmsg.type_.upper() == InboundMessages.SET_PARAMETERS:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.setParameters(requestID, receivedObject.modelParameters, receivedObject.projectId,
                                                 receivedObject.experimentId)
        elif gmsg.type_.upper() == InboundMessages.SET_EXPERIMENT_VIEW:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.setExperimentView(requestID, receivedObject.view, receivedObject.projectId,
                                                     receivedObject.experimentId)
        elif gmsg.type_.upper() == InboundMessages.LINK_DROPBOX:
            parameters = json.dumps(gmsg.data)
            key = parameters.get("key")
            self.connectionHandler.linkDropBox(requestID, key)
        elif gmsg.type_.upper() == InboundMessages.GET_DROPBOX_TOKEN:
            # ReceivedObject receivedObject = new json.dumps(gmsg.data, ReceivedObject.class);
            self.connectionHandler.getDropboxToken(requestID)
        elif gmsg.type_.upper() == InboundMessages.UNLINK_DROPBOX:
            parameters = json.dumps(gmsg.data)
            key = parameters.get("key")
            self.connectionHandler.unLinkDropBox(requestID, key)
        elif gmsg.type_.upper() == InboundMessages.UPLOAD_MODEL:
            parameters = json.dumps(gmsg.data)
            experimentId = int(parameters.get("experimentId"))
            projectId = int(parameters.get("projectId"))
            format = parameters.get("format")
            aspectPath = parameters.get("aspectPath")
            self.connectionHandler.uploadModel(aspectPath, projectId, experimentId, format)
        elif gmsg.type_.upper() == InboundMessages.UPLOAD_RESULTS:
            parameters = json.dumps(gmsg.data)
            experimentId = int(parameters.get("experimentId"))
            projectId = int(parameters.get("projectId"))
            format = parameters.get("format")
            aspectPath = parameters.get("aspectPath")
            self.connectionHandler.uploadResults(aspectPath, projectId, experimentId, format)
        elif gmsg.type_.upper() == InboundMessages.DOWNLOAD_RESULTS:
            parameters = json.dumps(gmsg.data)
            experimentId = int(parameters.get("experimentId"))
            projectId = int(parameters.get("projectId"))
            format = parameters.get("format")
            aspectPath = parameters.get("aspectPath")
            self.connectionHandler.downloadResults(requestID, aspectPath, projectId, experimentId, format)
        elif gmsg.type_.upper() == InboundMessages.EXPERIMENT_STATUS:
            self.connectionHandler.checkExperimentStatus(requestID, gmsg.data)
        elif gmsg.type_.upper() == InboundMessages.FETCH_VARIABLE:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.fetchVariable(requestID, receivedObject.projectId, receivedObject.dataSourceId,
                                                 receivedObject.variableId)
        elif gmsg.type_.upper() == InboundMessages.RESOLVE_IMPORT_TYPE:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.resolveImportType(requestID, receivedObject.projectId, receivedObject.paths)
        elif gmsg.type_.upper() == InboundMessages.RESOLVE_IMPORT_VALUE:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.resolveImportValue(requestID, receivedObject.projectId, receivedObject.experimentId,
                                                      receivedObject.path)
        elif gmsg.type_.upper() == InboundMessages.RUN_QUERY:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.runQuery(requestID, receivedObject.projectId,
                                            self.convertRunnableQueriesDataTransferModel(
                                                receivedObject.runnableQueries))
        elif gmsg.type_.upper() == InboundMessages.RUN_QUERY_COUNT:
            receivedObject = json.dumps(gmsg.data)
            self.connectionHandler.runQueryCount(requestID, receivedObject.projectId,
                                                 self.convertRunnableQueriesDataTransferModel(
                                                     receivedObject.runnableQueries))
        else:
            pass

    # NOTE: no other websocket expected for now

    # 
    # 	 * @param runnableQueries
    # 	 * @return A list based on the EMF class. It's not possible to use directly the EMF class as Gson requires fields with public access modifiers which breaks EMF encapsulation
    # 	 

    def convertRunnableQueriesDataTransferModel(self, runnableQueries):
        """ generated source for method convertRunnableQueriesDataTransferModel """
        runnableQueriesEMF = BasicEList()
        for dt in runnableQueries:
            rqEMF = DatasourcesFactory.eINSTANCE.createRunnableQuery()
            rqEMF.setQueryPath(dt.queryPath)
            rqEMF.setTargetVariablePath(dt.targetVariablePath)
            runnableQueriesEMF.add(rqEMF)
        return runnableQueriesEMF

        #
        # 	 * @return
        #

    def getConnectionID(self):
        """ generated source for method getConnectionID """
        return self.connectionID

        #
        # 	 * Handle events from the messages sender.
        # 	 *
        # 	 * If there's an error during messages transmission then terminate connection.
        # 	 *
        # 	 * @param event
        # 	 *            event from the messages sender.
        #

    def handleMessageSenderEvent(self, event):
        """ generated source for method handleMessageSenderEvent """
        if event.getType() == MessageSenderEvent.Type.MESSAGE_SEND_FAILED:
            self.messageSender.shutdown()
            self.messageSender.removeListener(self)
            ConnectionsManager.getInstance().removeConnection(self)


class ReceivedObject(object):
    """ generated source for class ReceivedObject """
    projectId = None
    experimentId = None
    variables = None
    watch = bool()
    modelParameters = None
    properties = None
    view = None


class GetScript(object):
    """ generated source for class GetScript """
    projectId = None
    scriptURL = None


class BatchExperiment(object):
    """ generated source for class BatchExperiment """
    projectId = None
    experiments = None


class NewExperiment(object):
    """ generated source for class NewExperiment """
    name = None
    watchedVariables = None
    modelParameters = None
    simulatorParameters = None
    duration = None
    timeStep = None
    simulator = None
    aspectPath = None


class GeppettoModelAPIParameters(object):
    """ generated source for class GeppettoModelAPIParameters """
    projectId = None
    experimentId = None
    dataSourceId = None
    paths = None
    path = None
    variableId = []
    runnableQueries = None


class RunnableQueryDT(object):
    """ generated source for class RunnableQueryDT """
    targetVariablePath = None
    queryPath = None


def getSession(self):
    """ generated source for method getSession """
    return self.userSession
