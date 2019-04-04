# TODO implement DefaultMessageSender
class DefaultMessageSender(object):
    """ generated source for class DefaultMessageSender """

    def __init__(self):
        """ generated source for method __init__ """
        self.listeners = []

    def shutdown(self):
        raise NotImplemented()

    def pause(self):
        raise NotImplemented()

    def resume(self):
        raise NotImplemented()

    def reset(self):
        raise NotImplemented()

    def sendMessage(self, requestID, messageType, update):
        raise NotImplemented()

    def sendFile(self, path):
        raise NotImplemented()

    def addListener(self, listener):
        self.listeners.append(listener)


class DefaultMessageSenderFactory(object):
    """ generated source for class DefaultMessageSenderFactory """
    queuingEnabled = False
    maxQueueSize = 5
    discardMessagesIfQueueFull = True
    compressionEnabled = False
    minMessageLengthForCompression = 20000
    queuedMessageTypes = None

    def getMessageSender(self, wsOutbound, listener):
        """ generated source for method getMessageSender """
        messageSender = DefaultMessageSender()
        messageSender.addListener(listener)
        # messageSender.setQueuingEnabled(self.queuingEnabled)
        # messageSender.setMaxQueueSize(self.maxQueueSize)
        # messageSender.setDiscardMessagesIfQueueFull(self.discardMessagesIfQueueFull)
        # messageSender.setCompressionEnabled(self.compressionEnabled)
        # messageSender.setMinMessageLengthForCompression(self.minMessageLengthForCompression)
        # messageSender.setQueuedMessageTypes(self.queuedMessageTypes)
        # messageSender.initialize(wsOutbound)
        return messageSender

    def isQueuedMessageType(self, messageType):
        """ generated source for method isQueuedMessageType """
        return self.queuedMessageTypes != None and self.queuedMessageTypes.contains(messageType)

    def isCompressionEnabled(self):
        """ generated source for method isCompressionEnabled """
        return self.compressionEnabled

    def setCompressionEnabled(self, compressionEnabled):
        """ generated source for method setCompressionEnabled """
        self.compressionEnabled = compressionEnabled

    def isQueuingEnabled(self):
        """ generated source for method isQueuingEnabled """
        return self.queuingEnabled

    def setQueuingEnabled(self, queuingEnabled):
        """ generated source for method setQueuingEnabled """
        self.queuingEnabled = queuingEnabled

    def getMaxQueueSize(self):
        """ generated source for method getMaxQueueSize """
        return self.maxQueueSize

    def setMaxQueueSize(self, maxQueueSize):
        """ generated source for method setMaxQueueSize """
        self.maxQueueSize = maxQueueSize

    def getDiscardMessagesIfQueueFull(self):
        """ generated source for method getDiscardMessagesIfQueueFull """
        return self.discardMessagesIfQueueFull

    def setDiscardMessagesIfQueueFull(self, discardMessagesIfQueueFull):
        """ generated source for method setDiscardMessagesIfQueueFull """
        self.discardMessagesIfQueueFull = discardMessagesIfQueueFull

    def getMinMessageLengthForCompression(self):
        """ generated source for method getMinMessageLengthForCompression """
        return self.minMessageLengthForCompression

    def setMinMessageLengthForCompression(self, minMessageLengthForCompression):
        """ generated source for method setMinMessageLengthForCompression """
        self.minMessageLengthForCompression = minMessageLengthForCompression

    def getQueuedMessageTypes(self):
        """ generated source for method getQueuedMessageTypes """
        return self.queuedMessageTypes

    def setQueuedMessageTypes(self, queuedMessageTypes):
        """ generated source for method setQueuedMessageTypes """
        self.queuedMessageTypes = queuedMessageTypes
