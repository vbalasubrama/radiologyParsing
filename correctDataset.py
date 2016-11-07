import csv
import ast
from ast import literal_eval
from sklearn import svm
from sklearn import metrics
import math
# from itertools import chain, izip

def openData():
    writer = open('./solutions/balancedVectors.csv', 'w')
    solution_neg_1 = []
    solution_1 = []
    solution = []
    with open('./solutions/vectors.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        i = iN = 0
        try:
            for index, vector  in reader:
                index = literal_eval(index)
                vector = literal_eval(vector)
                if index[3] == 1:
                    solution_1.append((index, vector))
                    solution_1.append((index, vector))
                    solution_1.append((index, vector))
                else:
                    solution_neg_1.append((index, vector))

        except ValueError:
            exit()
    for x in range(max(len(solution_1),len(solution_neg_1))):
        try:
            if x >= len(solution_1):
                solution.append(solution_neg_1[x])
            else:
                solution.append(solution_neg_1[x])
                solution.append(solution_1[x])
        except IndexError:
            print (x)
    for index, vector in solution:
        writer.write(str(index) + '\t' + str(vector) + '\n')


def checkData():
    with open('./solutions/balancedVectors.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        i = iN = 0
        for index, vector  in reader:
            index = literal_eval(index)
            if index[3] == 1:
                i += 1
            else:
                iN += 1
    with open('./solutions/vectors.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        i = iN = 0
        for index, vector  in reader:
            index = literal_eval(index)
            if index[3] == 1:
                i += 1
            else:
                iN += 1
def trainOnData():
    with open('./text/balancedVectors.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        X = []
        Y = []
        for index, vector  in reader:
                Y.append(literal_eval(index)[3])
                data_line = literal_eval(vector)
                X.append(data_line)
    clf = svm.SVC()

    k_fold = 10
    subset_size = math.floor(len(X) / k_fold)
    for k in range(k_fold):
        X_train = X[:k * subset_size] + X[(k + 1) * subset_size:]
        X_test = X[k * subset_size:][:subset_size]
        Y_train = Y[:k * subset_size] + Y[(k + 1) * subset_size:]
        Y_test = Y[k * subset_size:][:subset_size]
        clf.fit(X_train, Y_train)
        Y_predicted = clf.predict(X_test)
    print ("Classification report for %s" % clf)
    print (metrics.classification_report(Y_test, Y_predicted))
trainOnData()

