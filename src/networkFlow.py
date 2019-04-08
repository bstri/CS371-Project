from scapy.all import *
from time import time


class NetFlow:

    def __init__(self, localPort, remoteIP, remotePort, transferLayerProtocol):
        self.localPort = localPort
        self.remoteIP = remoteIP
        self.remotePort = remotePort
        self.protocol = transferLayerProtocol

        self.outgoingPackets = PacketList()
        self.incomingPackets = PacketList()
        self.incomingStart = None
        self.incomingEnd = None
        self.outgoingStart = None
        self.outgoingEnd = None
        
        # features go here
        self.outTotalData = 0
        self.inTotalData = 0
        self.totalData = 0
        self.outPPS = 0
        self.inPPS = 0
        self.outAvgPacketLength = 0
        self.inAvgPacketLength = 0
        self.outDataRate = 0
        self.inDataRate = 0

    def addIncomingPacket(self, pkt):
        if not self.incomingPackets: 
            self.incomingStart = time()
        else:
            self.incomingEnd = time()
        self.incomingPackets.append(pkt)

    def addOutgoingPacket(self, pkt):
        if not self.outgoingPackets: 
            self.outgoingStart = time()
        else:
            self.outgoingEnd = time()
        self.outgoingPackets.append(pkt)

    def generateFeatures(self):
        if len(self.outgoingPackets) >= 1:
            outgoingTotalData = sum(map(lambda x: len(x), self.outgoingPackets))
            self.outTotalData = outgoingTotalData
            self.outAvgPacketLength = outgoingTotalData / len(self.outgoingPackets)
            if len(self.outgoingPackets) >= 2:
                outgoingTime = self.outgoingEnd - self.outgoingStart
                self.outDataRate = outgoingTotalData / outgoingTime
                self.outPPS = len(self.outgoingPackets) / outgoingTime
        if len(self.incomingPackets) >= 1:
            incomingTotalData = sum(map(lambda x: len(x), self.incomingPackets))
            self.inTotalData = incomingTotalData
            self.inAvgPacketLength = incomingTotalData / len(self.incomingPackets)
            if len(self.incomingPackets) >= 2:
                incomingTime = self.incomingEnd - self.incomingStart
                self.inDataRate = incomingTotalData / incomingTime
                self.inPPS = len(self.incomingPackets) / incomingTime

        self.totalData = incomingTotalData + outgoingTotalData

    def getCommaSeparatedFeatures(self):
        return "{},{},{},{},{},{},{},{},{},{},{},{}".format(self.localPort, self.remotePort, self.protocol, self.inTotalData, self.inDataRate, self.inPPS, self.inAvgPacketLength, self.outTotalData, self.outDataRate, self.outPPS, self.outAvgPacketLength, self.totalData)
    
