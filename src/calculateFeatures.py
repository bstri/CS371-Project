from scapy.all import *
from scapy.layers.inet import IP
import pandas as pd
import numpy as np
import sys
import socket
import os
import urllib

from networkFlow import NetFlow
from requests import get
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localIP=s.getsockname()[0]
print("Local IP is : %s" % (s.getsockname()[0]))
s.close()
externalIP = get('https://api.ipify.org').text
print("External IP is : %s" % externalIP)

flows = []


def fields_extraction(x):
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
    global externalIP
    for flow in flows:
        if x.haslayer(IP):
            if x[IP].src == flow.remoteIP:
                flow.incomingPackets.append(x)
                existing = True
                break
            elif x[IP].dst == flow.remoteIP:
                flow.outgoingPackets.append(x)
                existing = True
                break
    if not existing:
        # Create a network flow with x inside and add to list
        # TODO: decide whether to separate TCP/UDP protocols for the same host
        newFlow = NetFlow()
        if x.haslayer(IP):
            if x[IP].src == localIP:
                newFlow.remoteIP = x[IP].dst
                newFlow.outgoingPackets.append(x)
            elif x[IP].dst == localIP:
                newFlow.remoteIP = x[IP].src
                newFlow.incomingPackets.append(x)
            else:
                x.show()
            flows.append(newFlow)


pkts = sniff(prn=lambda x: fields_extraction(x), count=20)
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
