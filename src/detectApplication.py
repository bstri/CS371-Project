import pickle

from scapy.all import *
from sklearn import tree
import argparse
from helperFunctions import getLocalMachineIP
from makeTrainingData import handlePacket

labelToActivityMap = ['Web Browsing', 'Video Streaming', 'Video Conferencing', 'File Downloading']

parser = argparse.ArgumentParser()
parser.add_argument('modelFile', help='file containing a serialized trained machine')

args = parser.parse_args()

clf = None
with open(args.modelFile, 'rb') as model:
    clf = pickle.load(model)

while True:
    flows = []
    pkts = sniff(prn=lambda x: handlePacket(x, flows), count=250)
    if not flows:
        continue
    for f in flows:
        f.generateFeatures()
    flows.sort(key=lambda f: f.totalPackets, reverse=True)  # sort by descending number of total packets
    print(labelToActivityMap[clf.predict(flows[0])])
