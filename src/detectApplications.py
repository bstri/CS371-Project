import pickle
from io import StringIO

from scapy.all import *
from sklearn import tree
import argparse
from helperFunctions import getLocalMachineIP
from makeTrainingData import handlePacket
from operator import itemgetter
import pandas as pd

labelToActivityMap = ['Web Browsing', 'Video Streaming', 'Video Conferencing', 'File Downloading']

parser = argparse.ArgumentParser()
parser.add_argument('modelFile', help='file containing a serialized trained machine')

args = parser.parse_args()

clf = None
with open(args.modelFile, 'rb') as model:
    clf = pickle.load(model)

columns_list = ['localPort',
                'remoteIP',
                'remotePort',
                'protocol',
                'totalPackets',
                'incomingPackets',
                'outgoingPackets',
                'totalData',
                'inTotalData',
                'outTotalData',
                'inDataRate',
                'outDataRate',
                'inPPS',
                'outPPS',
                'inAvgPacketLength',
                'outAvgPacketLength']

# features = ['localPort', 'remotePort', 'inDataRate', 'outDataRate', 'inPPS', 'outPPS', 'inAvgPacketLength', 'outAvgPacketLength']
# features = ['localPort', 'inAvgPacketLength', 'outDataRate']
# features = ['localPort', 'remotePort']
features = ['localPort', 'outAvgPacketLength']


from pprint import pprint
while True:
    flows = []
    pkts = sniff(prn=lambda x: handlePacket(x, flows), count=1000, timeout=3)
    for f in flows:
        f.generateFeatures()
    flows = [f for f in flows if f.totalPackets >= 60]
    if not flows:
        continue
    flows.sort(key=lambda f: f.totalPackets, reverse=True)  # sort by descending number of total packets
    labels = set()
    for flow in flows:
        # pprint(vars(flow))
        df = pd.DataFrame(columns=columns_list) # can probably move this out of the for loop
        df.loc[0] = flow.getFeaturesList()
        X = df[features]
        labels.add(labelToActivityMap[clf.predict(X)[0]])
    print(labels)
