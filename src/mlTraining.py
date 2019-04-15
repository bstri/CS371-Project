import pandas as pd
import numpy as np
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn import tree
from sklearn_pandas import DataFrameMapper

df = pd.read_csv("data.csv", header=None)
# You might not need this next line if you do not care about losing information about flow_id etc. All you actually need to
# feed your machine learning model are features and output label.
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
categorical_columns_list = ['localPort',
                            'remoteIP',
                            'remotePort',
                            'protocol']
continuous_columns_list = ['totalPackets',
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
df.columns = columns_list
dfm = DataFrameMapper(
    [(continuous_col, StandardScaler()) for continuous_col in continuous_columns_list] +
    [(categorical_col, LabelBinarizer()) for categorical_col in categorical_columns_list]
)
features = ['proto', 'feature_1', 'feature_2', 'feature_3', 'feature_4', 'feature_5']

X = df[features]
y = df['label']

acc_scores = 0
for i in range(0, 10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    #Decision Trees
    clf = tree.DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    # Neural network (MultiPerceptron Classifier)
    # clf = MLPClassifier()
    # clf.fit(X_train, y_train)

    #SVM's
    # clf = SVC(gamma='auto')     #SVC USE THIS
    # clf = LinearSVC()  #Linear SVC
    # clf.fit(X_train, y_train)


    #here you are supposed to calculate the evaluation measures indicated in the project proposal (accuracy, F-score etc)
    result = clf.score(X_test, y_test)  #accuracy score