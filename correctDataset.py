import csv
import ast
from ast import literal_eval
from sklearn import svm
from sklearn import metrics


def openData():
    writer = open('./text/balancedVectors.csv', 'wb')
    writer = csv.writer(writer, delimiter='\t')

    with open('./text/vectors.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        i = iN = 0
        for index, vector  in reader:
            index = literal_eval(index)
            vector = literal_eval(vector)
            writer.writerow([index, vector])
            if index[3] == 1:
                writer.writerow([index, vector])
                writer.writerow([index, vector])
def checkData():
    with open('./text/balancedVectors.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        i = iN = 0
        for index, vector  in reader:
            index = literal_eval(index)
            if index[3] == 1:
                i += 1
            else:
                iN += 1
        print i, iN
    with open('./text/vectors.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        i = iN = 0
        for index, vector  in reader:
            index = literal_eval(index)
            if index[3] == 1:
                i += 1
            else:
                iN += 1
        print i, iN
def trainOnData():
    with open('./text/balancedVectors.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        X = []
        Y = []
        for index, vector  in reader:
            Y.append(literal_eval(index)[3])
            data_line = literal_eval(vector)
            X.append(data_line)
    # X = []
    # Y = []
    # for key in list_of_index:
    #     X.append(rows[key])
    #     Y.append(key[3])
    print "Training: "
    clf = svm.SVC()

    k_fold = 10
    subset_size = len(X) / k_fold
    for k in range(k_fold):
        X_train = X[:k * subset_size] + X[(k + 1) * subset_size:]
        X_test = X[k * subset_size:][:subset_size]
        Y_train = Y[:k * subset_size] + Y[(k + 1) * subset_size:]
        Y_test = Y[k * subset_size:][:subset_size]
        clf.fit(X_train, Y_train)
        Y_predicted = clf.predict(X_test)
    print "Classification report for %s" % clf
    print metrics.classification_report(Y_test, Y_predicted)
trainOnData()

