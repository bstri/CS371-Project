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

        # features go here
        self.outPPS = 0
        self.inPPS = 0
        self.outAvgPacketLength = 0
        self.inAvgPacketLength = 0
        self.outDataRate = 0
        self.inDataRate = 0
        self.incomingStart = None
        self.incomingEnd = None
        self.outgoingStart = None
        self.outgoingEnd = None

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
        outgoingTime = self.outgoingEnd - self.outgoingStart
        outgoingTotalData = sum(map(lambda x: len(x), self.outgoingPackets))
        self.outDataRate = outgoingTotalData / outgoingTime
        self.outPPS = len(self.outgoingPackets) / outgoingTime
        self.outAvgPacketLength = outgoingTotalData / len(self.outgoingPackets)

        incomingTime = self.incomingEnd - self.incomingStart
        incomingTotalData = sum(map(lambda x: len(x), self.incomingPackets))
        self.inDataRate = incomingTotalData / incomingTime
        self.inPPS = len(self.incomingPackets) / incomingTime
        self.inAvgPacketLength = incomingTotalData / len(self.incomingPackets)