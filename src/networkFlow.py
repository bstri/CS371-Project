from scapy.all import *
class netFlow:
    conversationWith=""
    protocol=""
    outgoingPackets=PacketList()
    incomingPackets=PacketList()
    #features go here
    outFPS=0
    inFPS=0
    outAvgFrameLength=0
    inAvgFrameLength=0
    outDataRate=0
    inDataRate=0
