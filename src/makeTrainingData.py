from scapy.all import *
from scapy.layers.inet import IP
import pandas as pd
import numpy as np
import sys
import os
from networkFlow import NetFlow
from helperFunctions import getProtocol
from helperFunctions import getsrcdst
from helperFunctions import getLocalMachineIP
import argparse

# labels 0-3 correspond to these csv files
labelToCSV = ['webBrowsing.csv', 'videoStreaming.csv', 'videoConferencing.csv', 'fileDownloading.csv']

parser = argparse.ArgumentParser()
parser.add_argument('label', help='label to assign to this data', type=int)

args = parser.parse_args()
label = args.label

localIP = getLocalMachineIP()
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


pkts = sniff(prn=lambda x: handlePacket(x), count=1500)
# pkts.conversations()

for f in flows:
    f.generateFeatures()
    # print("Conversation with %s" % f.remoteIP)
    # print("~~~~Incoming~~~~")
    # for pkt in f.incomingPackets:
    #     print("Source: %s, Dest: %s, Summary: %s" % (pkt[IP].src, pkt[IP].dst, pkt.summary()))
    # print("~~~~Outgoing~~~~")
    # for pkt in f.outgoingPackets:
    #     print("Source: %s, Dest: %s, Summary: %s" % (pkt[IP].src, pkt[IP].dst, pkt.summary()))

flows.sort(key = lambda f: f.totalPackets, reverse = True) # sort by descending number of total packets

dirPath = os.path.dirname(os.path.realpath(__file__))
with open('{}/../trainingData/{}'.format(dirPath, labelToCSV[label]), 'a') as f:
    for flow in flows:
        f.write(flow.getCommaSeparatedFeatures() + ',{}\n'.format(label))

# with open('output.csv', 'w') as o:
    # o.write("\n".join(list(map(lambda f: f.getCommaSeparatedFeatures(), flows))))
