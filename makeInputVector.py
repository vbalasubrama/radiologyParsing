from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import re
import csv
import operator
import openData
from sklearn import svm
from sklearn import metrics

list_of_impressions, list_of_pathologyIndexes = openData.openData()


bagOfWords = {}
rows = {}
bagOfWordsIndex = 0
listOfPathologies = []

i = 0
#Split the impressions based on the indices for pathology
for impresssionKey in list_of_impressions:

    list_of_sentences = sent_tokenize(list_of_impressions[impresssionKey])
    if impresssionKey in list_of_pathologyIndexes.keys():
        indexStartOfPathology, indexEndOfPathology = list_of_pathologyIndexes[impresssionKey][0]
        currentPathology = list_of_impressions[impresssionKey][indexStartOfPathology:indexEndOfPathology]
        currentPathology = re.sub("[^a-zA-Z0-9]", " ", currentPathology).lower().strip()
        listOfPathologies.append((i, impresssionKey,currentPathology))
        i += 1

    for currentSentence in list_of_sentences:
        currentSentence = re.sub("[^a-zA-Z0-9]", " ", currentSentence).lower()
        currentWordList = word_tokenize(currentSentence)
        for currentToken in currentWordList:
            if not bagOfWords.has_key(currentToken+'_0'):
                bagOfWords[currentToken + '_0'] = bagOfWordsIndex
                bagOfWordsIndex += 1
                bagOfWords[currentToken + '_1'] = bagOfWordsIndex
                bagOfWordsIndex += 1

# Save words and number mapping
bagOfWords_sorted = (sorted(bagOfWords.items(), key=operator.itemgetter(1)))
with open('./text/bagOfWords.csv', 'wb') as the_file:
    for key, value in bagOfWords_sorted:
            the_file.write(key+ ',' + str(value)+'\n')
# Save Pathology Phrases
with open('./text/pathologyPhrases.csv', 'wb') as the_file:
    for i, impresssionKey, pathologyText in listOfPathologies:
        the_file.write(str(i)+','+str(impresssionKey)+','+pathologyText+'\n')

del currentWordList
del currentToken
del currentSentence
del indexEndOfPathology
del indexStartOfPathology
del currentPathology
del pathologyText

bagOfWordsIndex += 1
for currentToken in rows.keys():
    rows[currentToken] = [0]*(bagOfWordsIndex)

with open('./text/impressionsWithSentences.csv', 'wb') as the_file:

    for impresssionKey in list_of_impressions:
        #Filter Impressions that have Pathology keywords
        currentImpression = list_of_impressions[impresssionKey]
        the_file.write("Impression " + str(impresssionKey) + ': \n')
        list_of_sentences = sent_tokenize(list_of_impressions[impresssionKey])
        j = 1
        for currentSentence in list_of_sentences:
            currentSentence = re.sub("[^a-zA-Z0-9]", " ", currentSentence).lower().strip()
            for i, impressionOfPathology, currentPathologyText in listOfPathologies:
                # Find pathology in a given sentence
                if currentSentence.find(currentPathologyText) >= 0:
                    if impressionOfPathology == impresssionKey:
                        y = 1
                    else:
                        y = -1
                    rows[(impresssionKey,j,i,y)] = [0] * len(bagOfWords.keys())
                    #Convert sentence to tokens
                    pathologyStartIndex = currentSentence.find(currentPathologyText)
                    pathologyEndIndex   = pathologyStartIndex + len(currentPathologyText)
                    currentIdentifierStrings  = [w + '_0' for w in word_tokenize(currentSentence[:pathologyStartIndex])]\
                                                + [w + '_1' for w in word_tokenize(currentSentence[pathologyEndIndex+1:])]
                    for identifierString in currentIdentifierStrings:
                        if identifierString in bagOfWords.keys():
                            rows[(impresssionKey,j,i,y)][bagOfWords[identifierString]] = 1

            the_file.write('Sentence ' + str(j) + ': ' + currentSentence.strip()+'\n')
            j += 1



writer = csv.writer(open('./text/vectors.csv', 'wb'))
for key, value in rows.items():
                writer.writerow([key, value])
# X = []
# Y = []
# for key in rows.keys():
#     X.append(rows[key])
#     Y.append(key[3])
# clf = svm.SVC()
#
#
# k_fold = 10
# subset_size = len(X) / k_fold
# for k in range(k_fold):
#     X_train = X[:k * subset_size] + X[(k + 1) * subset_size:]
#     X_test = X[k * subset_size:][:subset_size]
#     Y_train = Y[:k * subset_size] + Y[(k + 1) * subset_size:]
#     Y_test = Y[k * subset_size:][:subset_size]
#     clf.fit(X_train, Y_train)
#     Y_predicted = clf.predict(X_test)
#
# print "Classification report for %s" % clf
# print metrics.classification_report(Y_test, Y_predicted)



