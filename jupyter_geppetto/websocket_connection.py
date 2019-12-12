#!/usr/bin/env python
""" generated source for module WebsocketConnection """
from __future__ import print_function

import gzip
import json
import logging

from jupyter_geppetto import settings
from pyecore.ecore import EList
from pygeppetto.api.message_handler import GeppettoMessageHandler
from tornado.websocket import WebSocketHandler


# package: org.geppetto.frontend.controllers
#
#  * Class used to process Web Socket Connections. Messages sent from the connecting clients, web socket connections, are received in here.
#  *
#  * @author matteocantarelli
#  *
#


class TornadoGeppettoWebSocketHandler(WebSocketHandler, GeppettoMessageHandler):

    def __init__(self, *args, **kwargs):
        WebSocketHandler.__init__(self, *args, **kwargs)
        GeppettoMessageHandler.__init__(self)

    def open(self):
        # 1 -> Send the connection
        logging.info('Open websocket')
        self.__class__.connection_id += 1

        self.sendClientId()

        # 2 -> Check user privileges
        self.sendPrivileges()

    def send_message_data(self, msg_data):
        msg = json.dumps(msg_data)
        if settings.websocket.compression_enabled and len(msg) > settings.websocket.min_message_length_for_compression:
            self.write_message(gzip.compress(bytes(msg, 'utf-8')), binary=True)
        self.write_message(msg)

    def on_message(self, message):
        self.handle_message(json.loads(message))

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
