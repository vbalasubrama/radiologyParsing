import csv
import ast
from ast import literal_eval

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
checkData()

