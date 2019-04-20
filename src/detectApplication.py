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

features = ['inDataRate', 'outDataRate', 'inPPS', 'outPPS', 'inAvgPacketLength', 'outAvgPacketLength']
# features = ['localPort', 'remotePort', 'inDataRate', 'outDataRate', 'inPPS', 'outPPS', 'inAvgPacketLength', 'outAvgPacketLength']



while True:
    flows = []
    pkts = sniff(prn=lambda x: handlePacket(x, flows), count=500)
    for f in flows:
        f.generateFeatures()
    flows = [f for f in flows if f.totalPackets >= 100 and f.remotePort and f.localPort]
    if not flows:
        continue
    flows.sort(key=lambda f: f.totalPackets, reverse=True)  # sort by descending number of total packets
    # matrix = [[flow.getFeaturesList()[i] for i in [0, 2, 10, 11, 12, 13, 14, 15]] for flow in flows]
    # matrix = [[flow.getFeaturesList()[i] for i in [10, 11, 12, 13, 14, 15]] for flow in flows]
    # avg = [float(sum(col))/float(len(col)) for col in zip(*matrix)]
    # # df = pd.DataFrame(columns=columns_list)
    # df = pd.DataFrame(columns=features)
    # df.loc[0] = avg
    # X = df[features]
    # # print(X)
    # avgFlowResult = labelToActivityMap[clf.predict(X)[0]]
    df = pd.DataFrame(columns=columns_list)
    for i in range(len(flows)):
        df.loc[i] = flows[i].getFeaturesList()
    # df.loc[0] = flows[0].getFeaturesList()
    X = df[features]

    print(labelToActivityMap[i] for i in clf.predict(X))

