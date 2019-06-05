#!/usr/bin/env python
""" generated source for module WebsocketConnection """
from __future__ import print_function

import gzip
import json
import logging

from pyecore.valuecontainer import EList
from pygeppetto.constants import UserPrivileges
from pygeppetto.model.exceptions import GeppettoExecutionException, GeppettoInitializationException
from tornado.websocket import WebSocketHandler

# package: org.geppetto.frontend.controllers
#
#  * Class used to process Web Socket Connections. Messages sent from the connecting clients, web socket connections, are received in here.
#  *
#  * @author matteocantarelli
#  *
#
from . import inbound_messages as InboundMessages
from . import outbound_messages as OutboundMessages
from .connection_handler import ConnectionHandler, GeppettoHandlerTypedException
from .messaging import TransportMessageFactory
from .. import settings

in_out_msg_lookup = {
    InboundMessages.GEPPETTO_VERSION: OutboundMessages.GEPPETTO_VERSION,
    InboundMessages.RESOLVE_IMPORT_TYPE: OutboundMessages.IMPORT_TYPE_RESOLVED,
    InboundMessages.RESOLVE_IMPORT_VALUE: OutboundMessages.IMPORT_VALUE_RESOLVED
}


def lookup_return_msg_type(msg_type):
    if msg_type in in_out_msg_lookup:
        return in_out_msg_lookup[msg_type]
    raise RuntimeError("{} not defined into in_out_msg_lookup".format(msg_type))


class GeppettoWebSocketHandler(WebSocketHandler):
    connection_id = 0
    CLIENT_ID = 'Connection1'

    PRIVILEGES = json.dumps({
        "userName": "Python User",
        "loggedIn": True,
        "hasPersistence": False,
        "privileges": list(up.value for up in UserPrivileges)
    })

    def __init__(self, *args, **kwargs):
        WebSocketHandler.__init__(self, *args, **kwargs)
        self.geppettoHandler = ConnectionHandler(self)

    def open(self):
        # 1 -> Send the connection
        logging.info('Open websocket')
        self.__class__.connection_id += 1
        self.send_message(None, OutboundMessages.CLIENT_ID, self.CLIENT_ID)

        # 2 -> Check user privileges
        self.send_message(None, OutboundMessages.USER_PRIVILEGES, self.PRIVILEGES)

    def on_message(self, message):

        payload = json.loads(message)
        assert 'type' in payload, 'Websocket without type received: {}'.format(payload)

        logging.info('Websocket websocket received: {}'.format(payload['type']))

        experimentId = -1
        #  de-serialize JSON
        gmsg = payload
        requestID = gmsg['requestID']
        msg_data = None
        #  switch on messages type
        #  NOTE: each messages handler knows how to interpret the GeppettoMessage data field
        msg_type = gmsg['type'].lower()
        try:
            if msg_type == InboundMessages.GEPPETTO_VERSION:
                msg_data = self.geppettoHandler.getVersionNumber(requestID)

            elif msg_type == InboundMessages.RESOLVE_IMPORT_VALUE:
                receivedObject = json.loads(gmsg['data'])
                msg_data = self.geppettoHandler.resolveImportValue(requestID, receivedObject['projectId'],
                                                                   receivedObject['experimentId'],
                                                                   receivedObject['path'])

            elif msg_type == InboundMessages.RESOLVE_IMPORT_TYPE:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.resolveImportType(requestID, receivedObject.projectId,
                                                                  receivedObject.paths)
            elif msg_type == InboundMessages.LOAD_PROJECT_FROM_CONTENT:
                self.geppettoHandler.loadProjectFromContent(requestID, gmsg['data'])
            elif msg_type == InboundMessages.LOAD_PROJECT_FROM_URL:
                msg_data = self.geppettoHandler.loadProjectFromUrl(requestID, gmsg['data'])

            # TODO From here on, implementation is not complete
            elif msg_type == InboundMessages.USER_PRIVILEGES:
                msg_data = self.geppettoHandler.checkUserPrivileges(requestID)
            elif msg_type == InboundMessages.NEW_EXPERIMENT:
                parameters = gmsg['data']
                projectId = int(parameters.get("projectId"))
                msg_data = self.geppettoHandler.newExperiment(requestID, projectId)
            elif msg_type == InboundMessages.NEW_EXPERIMENT_BATCH:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.newExperimentBatch(requestID, receivedObject.projectId, receivedObject)
            elif msg_type == InboundMessages.CLONE_EXPERIMENT:
                parameters = gmsg['data']
                projectId = int(parameters.get("projectId"))
                experimentId = int(parameters.get("experimentId"))
                msg_data = self.geppettoHandler.cloneExperiment(requestID, projectId, experimentId)

            elif msg_type == InboundMessages.LOAD_PROJECT_FROM_ID:
                parameters = gmsg['data']
                if parameters.containsKey("experimentId"):
                    experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                self.geppettoHandler.loadProjectFromId(requestID, projectId, experimentId)

            elif msg_type == InboundMessages.PERSIST_PROJECT:
                parameters = gmsg['data']
                projectId = int(parameters.get("projectId"))
                msg_data = self.geppettoHandler.persistProject(requestID, projectId)
            elif msg_type == InboundMessages.MAKE_PROJECT_PUBLIC:
                parameters = gmsg['data']
                projectId = int(parameters.get("projectId"))
                isPublic = bool(parameters.get("isPublic"))
                msg_data = self.geppettoHandler.makeProjectPublic(requestID, projectId, isPublic)
            elif msg_type == InboundMessages.DOWNLOAD_PROJECT:
                parameters = gmsg['data']
                projectId = int(parameters.get("projectId"))
                msg_data = self.geppettoHandler.downloadProject(requestID, projectId)
            elif msg_type == InboundMessages.SAVE_PROJECT_PROPERTIES:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.saveProjectProperties(requestID, receivedObject.projectId,
                                                                      receivedObject.properties)
            elif msg_type == InboundMessages.SAVE_EXPERIMENT_PROPERTIES:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.saveExperimentProperties(requestID, receivedObject.projectId,
                                                                         receivedObject.experimentId,
                                                                         receivedObject.properties)
            elif msg_type == InboundMessages.LOAD_EXPERIMENT:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                msg_data = self.geppettoHandler.loadExperiment(requestID, experimentId, projectId)
            elif msg_type == InboundMessages.GET_SCRIPT:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.sendScriptData(requestID, receivedObject.projectId,
                                                               receivedObject.scriptURL,
                                                               self.websocketConnection)
            elif msg_type == InboundMessages.GET_DATA_SOURCE_RESULTS:
                url = None
                dataSourceName = None
                try:
                    parameters = gmsg['data']
                    url = parameters.get("url")
                    dataSourceName = parameters.get("data_source_name")
                    # TODO: use self.websocketConnection when it is implemented
                    msg_data = self.geppettoHandler.sendDataSourceResults(requestID, dataSourceName, url,
                                                                          'self.websocketConnection')
                except IOError as e:
                    self.send_message(requestID, OutboundMessages.ERROR_READING_SCRIPT, "")
            elif msg_type == InboundMessages.GET_EXPERIMENT_STATE:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.getExperimentState(requestID, receivedObject.experimentId,
                                                                   receivedObject.projectId,
                                                                   receivedObject.variables)
            elif msg_type == InboundMessages.DELETE_EXPERIMENT:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.deleteExperiment(requestID, receivedObject.experimentId,
                                                                 receivedObject.projectId)
            elif msg_type == InboundMessages.RUN_EXPERIMENT:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.runExperiment(requestID, receivedObject.experimentId,
                                                              receivedObject.projectId)
            elif msg_type == InboundMessages.SET_WATCHED_VARIABLES:
                receivedObject = gmsg['data']
                try:
                    msg_data = self.geppettoHandler.setWatchedVariables(requestID, receivedObject.variables,
                                                                        receivedObject.experimentId,
                                                                        receivedObject.projectId,
                                                                        receivedObject.watch)
                except GeppettoExecutionException as e:
                    self.send_message(requestID, OutboundMessages.ERROR_SETTING_WATCHED_VARIABLES, "")
                except GeppettoInitializationException as e:
                    self.send_message(requestID, OutboundMessages.ERROR_SETTING_WATCHED_VARIABLES, "")
            elif msg_type == InboundMessages.GET_SUPPORTED_OUTPUTS:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                instancePath = parameters.get("instancePath")
                msg_data = self.geppettoHandler.getSupportedOuputs(requestID, instancePath, experimentId, projectId)
            elif msg_type == InboundMessages.DOWNLOAD_MODEL:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                instancePath = parameters.get("instancePath")
                format = parameters.get("format")
                msg_data = self.geppettoHandler.downloadModel(requestID, instancePath, format, experimentId, projectId)
            elif msg_type == InboundMessages.SET_PARAMETERS:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.setParameters(requestID, receivedObject.modelParameters,
                                                              receivedObject.projectId,
                                                              receivedObject.experimentId)
            elif msg_type == InboundMessages.SET_EXPERIMENT_VIEW:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.setExperimentView(requestID, receivedObject.view,
                                                                  receivedObject.projectId,
                                                                  receivedObject.experimentId)
            elif msg_type == InboundMessages.LINK_DROPBOX:
                parameters = gmsg['data']
                key = parameters.get("key")
                msg_data = self.geppettoHandler.linkDropBox(requestID, key)
            elif msg_type == InboundMessages.GET_DROPBOX_TOKEN:
                # ReceivedObject receivedObject = new gmsg['data'], ReceivedObject.class);
                msg_data = self.geppettoHandler.getDropboxToken(requestID)
            elif msg_type == InboundMessages.UNLINK_DROPBOX:
                parameters = gmsg['data']
                key = parameters.get("key")
                msg_data = self.geppettoHandler.unLinkDropBox(requestID, key)
            elif msg_type == InboundMessages.UPLOAD_MODEL:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                format = parameters.get("format")
                aspectPath = parameters.get("aspectPath")
                msg_data = self.geppettoHandler.uploadModel(aspectPath, projectId, experimentId, format)
            elif msg_type == InboundMessages.UPLOAD_RESULTS:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                format = parameters.get("format")
                aspectPath = parameters.get("aspectPath")
                msg_data = self.geppettoHandler.uploadResults(aspectPath, projectId, experimentId, format)
            elif msg_type == InboundMessages.DOWNLOAD_RESULTS:
                parameters = gmsg['data']
                experimentId = int(parameters.get("experimentId"))
                projectId = int(parameters.get("projectId"))
                format = parameters.get("format")
                aspectPath = parameters.get("aspectPath")
                msg_data = self.geppettoHandler.downloadResults(requestID, aspectPath, projectId, experimentId, format)
            elif msg_type == InboundMessages.EXPERIMENT_STATUS:
                msg_data = self.geppettoHandler.checkExperimentStatus(requestID, gmsg['data'])
            elif msg_type == InboundMessages.FETCH_VARIABLE:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.fetchVariable(requestID, receivedObject.projectId,
                                                              receivedObject.dataSourceId,
                                                              receivedObject.variableId)

            elif msg_type == InboundMessages.RUN_QUERY:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.runQuery(requestID, receivedObject.projectId,
                                                         self.convertRunnableQueriesDataTransferModel(
                                                             receivedObject.runnableQueries))
            elif msg_type == InboundMessages.RUN_QUERY_COUNT:
                receivedObject = gmsg['data']
                msg_data = self.geppettoHandler.runQueryCount(requestID, receivedObject.projectId,
                                                              self.convertRunnableQueriesDataTransferModel(
                                                                  receivedObject.runnableQueries))
            else:
                pass

        except GeppettoHandlerTypedException as e:
            self.send_message(requestID, e.msg_type, e.payload.__dict__)
        except AttributeError as e:
            logging.error('Message type not handled:' + payload['type'])
            raise e

        if msg_data is not None:
            return_msg_type = lookup_return_msg_type(msg_type)
            self.send_message(requestID, return_msg_type, msg_data)

    def send_message(self, requestID, return_msg_type, msg_data):
        msg_data = TransportMessageFactory.getTransportMessage(requestID=requestID, type_=return_msg_type,
                                                               update=msg_data).__dict__
        # Here we go straight with compression and direct sending
        # In the Java backend we have a more complex configuration with enqueuing, size-based compression and more
        # See https://github.com/openworm/org.geppetto.frontend/blob/master/src/main/java/org/geppetto/frontend/messaging/DefaultMessageSender.java
        msg = json.dumps(msg_data)
        if settings.websocket.compression_enabled and len(msg) > settings.websocket.min_message_length_for_compression:
            self.write_message(gzip.compress(bytes(msg, 'utf-8')), binary=True)
        self.write_message(msg)

    def on_close(self):
        # self.write_message({
        #     'type': 'socket_closed',
        #     'data': ''
        # })
        # self.geppettoHandler.closeProject()
        logging.info("Closed Connection ...")

    # NOTE: no other websocket expected for now

    # 
    # 	 * @param runnableQueries
    # 	 * @return A list based on the EMF class. It's not possible to use directly the EMF class as Gson requires fields with public access modifiers which breaks EMF encapsulation
    # 	 

    def convertRunnableQueriesDataTransferModel(self, runnableQueries):
        """ generated source for method convertRunnableQueriesDataTransferModel """
        runnableQueriesEMF = EList('')
        from pygeppetto.model.datasources.datasources import RunnableQuery
        for dt in runnableQueries:
            rqEMF = RunnableQuery(targetVariablePath=dt.targetVariablePath, queryPath=dt.queryPath)
            runnableQueriesEMF.append(rqEMF)
        return runnableQueriesEMF
