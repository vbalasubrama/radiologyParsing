import csv
import ast


def openData():
    impressions = {}
    listOfIndexes = {}
    with open('./raw_text/new_impressions.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for index, text in reader:
            impressions[int(index)] = text

    with open('./raw_text/new_keywords_by_index.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for index, list in reader:
            list = ast.literal_eval(list)
            if list.has_key('Pathology'):
                listOfIndexes[int(index)] = list['Pathology']
    return impressions, listOfIndexes

