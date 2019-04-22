import pandas as pd
import numpy as np
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score)
from sklearn.preprocessing import StandardScaler, LabelBinarizer, LabelEncoder
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn_pandas import DataFrameMapper, cross_val_score
from sklearn_pandas import DataFrameMapper
import argparse
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('csvFile', help='path to csv file containing training data')
parser.add_argument('-o', help='output file path for the trained machine', dest='outFile')

args = parser.parse_args()

df = pd.read_csv(args.csvFile, header=None)
pd.options.mode.chained_assignment = None  # remove annoying warnings

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
                'outAvgPacketLength',
                'label']
df.columns = columns_list

features = ['outDataRate', 'inAvgPacketLength']
# features = ['inDataRate', 'outDataRate', 'inPPS', 'outPPS', 'inAvgPacketLength', 'outAvgPacketLength']
# features = ['localPort', 'remotePort', 'inDataRate', 'outDataRate', 'inPPS', 'outPPS', 'inAvgPacketLength', 'outAvgPacketLength']
# features = ['localPort', 'inAvgPacketLength', 'outDataRate']
# features = ['localPort', 'remotePort']
# features = ['localPort', 'outAvgPacketLength']

X = df[features]
y = df['label']

acc_scores = 0
prec_scores = 0
recall_scores = 0
f1_scores = 0
for i in range(0, 10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50)

    if X_train.shape[0] > X_test.shape[0]:
        X_train.drop(X_train.index[0], axis=0, inplace=True)
        y_train.drop(y_train.index[0], axis=0, inplace=True)
    elif X_train.shape[0] < X_test.shape[0]:
        X_test.drop(X_test.index[0], axis=0, inplace=True)
        y_test.drop(y_test.index[0], axis=0, inplace=True)

    # Decision Trees
    clf = tree.DecisionTreeClassifier()

    # Neural network (MultiPerceptron Classifier)
    # clf = MLPClassifier()

    # SVM's
    #clf = SVC(gamma='auto')     #SVC USE THIS
    #clf = LinearSVC()  #Linear SVC

    # here you are supposed to calculate the evaluation
    # measures indicated in the project proposal (accuracy, F-score etc)
    clf.fit(X_train, y_train)
    result_acc = clf.score(X_test, y_test)  # accuracy score
    acc_scores += result_acc
    print('Accuracy Score: ' + str(result_acc))
    result_prec = precision_score(y_train, y_test, average='weighted')
    prec_scores += result_prec
    print('Precision Score: ' + str(result_prec))
    result_recall = recall_score(y_train, y_test, average='weighted')
    recall_scores += result_recall
    print('Recall Score: ' + str(result_recall))
    result_f1 = f1_score(y_train, y_test, average='weighted')
    f1_scores += result_f1
    print('F1 Score: ' + str(result_f1))
print('\nAvg accuracy - ' + str(acc_scores/10))
print('Avg precision - ' + str(prec_scores/10))
print('Avg recall - ' + str(recall_scores/10))
print('Avg f1 - ' + str(f1_scores/10))

finalDecisionTree = tree.DecisionTreeClassifier()
# serialize and store trained machine
if args.outFile:
    with open(args.outFile, 'wb') as f:
        finalDecisionTree.fit(X, y)
        pickle.dump(finalDecisionTree, f)
