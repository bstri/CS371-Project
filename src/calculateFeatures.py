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
    if 'IP' in pkt:
        return pkt['IP'].src, pkt['IP'].dst
    if 'IPv6' in pkt:
        return pkt['IPv6'].src, pkt['IPv6'].dst
    if 'ARP' in pkt:
        return pkt['ARP'].psrc, pkt['ARP'].pdst
    raise TypeError()


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localIP = s.getsockname()[0]
print("Local IP is : %s" % (s.getsockname()[0]))
s.close()

flows = []


def sort_packet(x):
    # x.show()
    # print("Packet info")
    # print("has IP layer... %s" % {x.haslayer('IP')})
    # print("source ip... %s" % {x['IP'].src})
    # print("dest ip... %s" % {x['IP'].dst})
    # print x.sprintf("{IP:%IP.src%,%IP.dst%,}"
    #     "{TCP:%TCP.sport%,%TCP.dport%,}"
    #     "{UDP:%UDP.sport%,%UDP.dport%}")
    # print x.summary()
    # x.show()
    # Check if there is already an ongoing conversation with the remote host
    existing = False
    global flows
    global localIP
    (src, dst) = getsrcdst(x)
    for flow in flows:
        if src == flow.remoteIP:
            flow.incomingPackets.append(x)
            existing = True
            break
        elif dst == flow.remoteIP:
            flow.outgoingPackets.append(x)
            existing = True
            break
    if not existing:
        # Create a network flow with x inside and add to list
        # TODO: decide whether to separate TCP/UDP protocols for the same host
        newFlow = NetFlow()
        if src == localIP:
            newFlow.remoteIP = dst
            newFlow.outgoingPackets.append(x)
            flows.append(newFlow)
        elif dst == localIP:
            newFlow.remoteIP = src
            newFlow.incomingPackets.append(x)
            flows.append(newFlow)
        else:
            x.show()


pkts = sniff(prn=lambda x: sort_packet(x), count=20)
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

