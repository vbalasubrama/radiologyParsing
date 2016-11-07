from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import re
import csv
import operator
import openData


def read_phrases():
    pathologyPhrase = {}
    with open('./text/pathologyPhrases.csv', 'r') as phrasesFile:
        reader = csv.reader(phrasesFile, delimiter=',')
        for index, impression_number, phrase in reader:
            pathologyPhrase[(int(index), int(impression_number))] = phrase
    return pathologyPhrase


def read_wordBag():
    bagOfWords = {}
    with open('./text/bagOfWords.csv', 'r') as wordsFile:
        reader = csv.reader(wordsFile, delimiter=',')
        for word,index  in reader:
            bagOfWords[word]= int(index)
    return bagOfWords


list_of_impressions = openData.openData()[0]
list_of_Words = read_wordBag()
list_of_PathologyPhrases = read_phrases()
print ("Done")
solution = {}
for impression_key in list_of_impressions.keys():
    try:
        impression = list_of_impressions[impression_key]
        list_of_sentences = sent_tokenize(impression)
    except TypeError:
        print (impression)
        break
    sentenceInImpression = 0
    for currentSentence in list_of_sentences:
        sentenceInImpression += 1
        currentSentence = re.sub("[^a-zA-Z0-9]", " ", currentSentence).lower().strip()
        for phrase_key in list_of_PathologyPhrases.keys():
            phrase = list_of_PathologyPhrases[phrase_key]
            pathologyNumber = phrase_key[0]
            originalImpression = phrase_key[1]
            try:
                if phrase in currentSentence:
                    try:
                        preSentence, postSentence = currentSentence.split(phrase)
                    except ValueError:
                        print(currentSentence.split(phrase))
                        continue
                    preSentence  = [w + '_0' for w in word_tokenize(preSentence)]
                    postSentence = [w + '_1' for w in word_tokenize(postSentence)]
                    data_row = [0] * len(list_of_Words)

                    for word in preSentence + postSentence:
                        if word in list_of_Words.keys():
                            data_row[list_of_Words[word]] = 1
                        else:
                            continue
                    if originalImpression == impression_key:
                        y = 1
                    else:
                        y = -1
                    otherWordsInSentence = len((preSentence)) + len((postSentence))
                    solution[(impression_key,sentenceInImpression,pathologyNumber,y,otherWordsInSentence, data_row.count(1))] = data_row
            except TypeError:
                print("Error:\n", phrase,'\n',currentSentence)
                continue

target = open('./solutions/vectors.csv', 'w')
for key, value in solution.items():
    target.write(str(key)+'\t'+ str(value)+'\n')