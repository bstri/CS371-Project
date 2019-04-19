from scapy.all import *
from sklearn import tree
import argparse
from helperFunctions import getLocalMachineIP
from makeTrainingData import handlePacket

clf = tree.DecisionTreeClassifier()  # Replace with reading in model from pickled object

while True:
    localIP = getLocalMachineIP()
    flows = []
    pkts = sniff(prn=lambda x: handlePacket(x), count=500)
    for f in flows:
        f.generateFeatures()
    flows.sort(key=lambda f: f.totalPackets, reverse=True)  # sort by descending number of total packets
    print(clf.predict(flows[0]))






