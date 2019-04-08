from scapy.all import *
from scapy.layers.inet import IP
import pandas as pd
import numpy as np
import sys
import socket
import os
import urllib

from networkFlow import NetFlow
# from requests import get


def getsrcdst(pkt):
    """Extract src and dst addresses"""
    srcport = ''
    dstport = ''
    if 'TCP' in pkt:
        srcport = pkt['TCP'].sport
        dstport = pkt['TCP'].dport
    if 'UDP' in pkt:
        srcport = pkt['UDP'].sport
        dstport = pkt['UDP'].dport

    if 'IP' in pkt:
        return pkt['IP'].src, srcport, pkt['IP'].dst, dstport
    if 'IPv6' in pkt:
        return pkt['IPv6'].src, srcport, pkt['IPv6'].dst, dstport
    if 'ARP' in pkt:
        return pkt['ARP'].psrc, srcport, pkt['ARP'].pdst, dstport
    raise TypeError()
def getProtocol(pkt):
    if 'TCP' in pkt:
        return 'TCP'
    elif 'UDP' in pkt:
        return 'UDP'
    # elif 'ICMP' in pkt:
    #     return 'ICMP'
    else:
        return 'other'


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localIP = s.getsockname()[0]
print("Local IP is : %s" % (s.getsockname()[0]))
s.close()

flows = []


def handlePacket(x):
    # Check if there is already an ongoing conversation with the remote host
    existing = False
    global flows
    global localIP
    (src, srcport, dst, dstport) = getsrcdst(x)
    transportProtocol = getProtocol(x)
    for flow in flows:
        if (src, srcport, dst, dstport, transportProtocol) == (flow.remoteIP, flow.remotePort, localIP, flow.localPort, flow.protocol):
            flow.addIncomingPacket(x)
            existing = True
            break
        elif (src, srcport, dst, dstport, transportProtocol) == (localIP, flow.localPort, flow.remoteIP, flow.remotePort, flow.protocol):
            flow.addOutgoingPacket(x)
            existing = True
            break
    if not existing:
        # Create a network flow with x inside and add to list
        if src == localIP:
            newFlow = NetFlow(srcport, dst, dstport, transportProtocol)
            newFlow.addOutgoingPacket(x)
            flows.append(newFlow)
        elif dst == localIP:
            newFlow = NetFlow(dstport, src, srcport, transportProtocol)
            newFlow.addIncomingPacket(x)
            flows.append(newFlow)
        else:
            x.show()


pkts = sniff(prn=lambda x: handlePacket(x), count=20)
# pkts.conversations()
# "show" function
for f in flows:
    print("\nNETWORK FLOW:\n")
    print("Conversation with %s" % f.remoteIP)
    print("~~~~Incoming~~~~")
    # f.incomingPackets.show()
    for pkt in f.incomingPackets:
        print("Source: %s, Dest: %s, Summary: %s" % (pkt[IP].src, pkt[IP].dst, pkt.summary()))
    print("~~~~Outgoing~~~~")
    for pkt in f.outgoingPackets:
        print("Source: %s, Dest: %s, Summary: %s" % (pkt[IP].src, pkt[IP].dst, pkt.summary()))

