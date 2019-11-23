import sys

import DBManager
from Ranker import Ranker

import time
from nltk.stem import PorterStemmer

db = DBManager.instance('wordcount')
prdb = DBManager.instance('PRMatrix')

# function to rank by search option
def rank(option, keywords):
    if option != 'pr':
        all = db.getAll()

        ranker = Ranker(keywords)
        docs_scores = []

        otime = time.time()

        for instance in all:
            score = dict()

            wordlist = instance['words']

            score['url'] = instance['url']

            # TODO: change to switch option
            if option == 'cos':
                score[option] = ranker.cosineSimilarity(wordlist, instance[option])
            elif option == 'jac':
                score[option] = ranker.jaccardSimilarity(wordlist, instance[option])
            elif option == 'vae':
                score[option] = ranker.variationalAutoEncoder(wordlist, instance[option])
            else:
                break

            docs_scores.append(score)

        sorted_scores = sorted(docs_scores, key=lambda i:i[option], reverse=True)

        return (sorted_scores, time.time() - otime)

    else:
        all = prdb.getAll()
        docs_scores = []

        for instance in all:
            score = dict()
            score['url'] = instance['url']
            score[option] = instance['score']

            docs_scores.append(score)

        return (sorted(docs_scores, key=lambda i:i[option], reverse=True), 0.0)

def custom_print(option, scores):
    print "Search results: (score, url)"
    for instance in scores:
        print "{}, {}".format(instance[option], instance['url'])

    print " "


def terminate():
    print "Run option: python [path]/Retriever.py [control] [parameter]"
    print "Parameter list:"
    print "-option :"
    print "     cos: cosine similarity measure"
    print "     jac: jaccard similarity measure"
    print "     vae: variational auto encoder measure"
    print "     pr: page rank measure"

def main():
    argv = sys.argv
    # search if option exists
    if "-option" in argv:
        index = argv.index("-option")
        option = argv[index + 1]
        if option != 'cos' and option != 'jac' and option != 'vae' and option != 'pr':
            terminate()
    else:
        terminate()

    # find the keywords
    print "Type in the search keywords"
    keywords = raw_input().split()

    Porter = PorterStemmer()
    processedWords = []
    for word in keywords:
        processedWords.append(Porter.stem(word))

    scores, usedTime = rank(option, processedWords)

    custom_print(option, scores)

    print "The search takes {} ms".format(usedTime)

if __name__ == "__main__":
    main()
