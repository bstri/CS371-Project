from scapy.all import *
from time import time
class NetFlow:

    # def __init__(self, hostPort, remoteIP, remotePort, transferLayerProtocol):
    #     self.hostPort = hostPort
    #     self.remoteIP=remoteIP
    #     self.protocol=transferLayerProtocol
    def __init__(self):
        self.outgoingPackets=PacketList()
        self.incomingPackets=PacketList()

        #features go here
        self.outPPS=0
        self.inPPS=0
        self.outAvgPacketLength=0
        self.inAvgPacketLength=0
        self.outDataRate=0
        self.inDataRate=0

    def AddIncomingPacket(self, pkt):
        if not self.incomingPackets: 
            self.incomingStart = time()
        else:
            self.incomingEnd = time()
        self.incomingPackets.append(pkt)

    def AddOutgoingPacket(self, pkt):
        if not self.outgoingPackets: 
            self.outgoingStart = time()
        else:
            self.outgoingEnd = time()
        self.outgoingPackets.append(pkt)

    def GenerateFeatures(self):
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