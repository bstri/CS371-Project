import pickle
# from io import StringIO
from sklearn.externals.six import StringIO
import pydot
from scapy.all import *
from sklearn import tree
import argparse
from helperFunctions import getLocalMachineIP
from makeTrainingData import handlePacket
from sklearn.datasets import load_iris
import pandas as pd

labelToActivityMap = ['Web Browsing', 'Video Streaming', 'Video Conferencing', 'File Downloading']

parser = argparse.ArgumentParser()
parser.add_argument('modelFile', help='file containing a serialized trained machine')

args = parser.parse_args()

clf = None
with open(args.modelFile, 'rb') as model:
    clf = pickle.load(model)

dirname = os.path.dirname(__file__)
# filename = os.path.join(dirname, '..', 'resources', 'graph.dot')
filename = 'C:/Users/Nelson Penn/PycharmProjects/CS371-Project/resources/graph.png'

with open(filename, 'wb') as file:
    dotFile = StringIO()
    tree.export_graphviz(clf, out_file=dotFile)
    graph = pydot.graph_from_dot_data(dotFile.getvalue())
    graph[0].write_png(filename )

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
# features = ['localPort', 'inAvgPacketLength', 'outDataRate']
# features = ['localPort', 'remotePort']
# features = ['localPort', 'outAvgPacketLength']


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
        pprint(vars(flow))
        df = pd.DataFrame(columns=columns_list)  # can probably move this out of the for loop
        df.loc[0] = flow.getFeaturesList()
        X = df[features]
        labels.add(labelToActivityMap[clf.predict(X)[0]])
    print(labels)
