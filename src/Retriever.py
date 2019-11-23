import sys

import DBManager
from Ranker import Ranker

import time
from nltk.stem import PorterStemmer

db = DBManager.instance('wordcount')
prdb = DBManager.instance('PRMatrix')

# function to rank by search option
def rank(option, keywords):
    ranker = Ranker(keywords)

    # if option is not page rank and mix
    if option != 'pr' and 'mix' not in option:
        all = db.getAll()

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

    elif option == 'pr':
        all = prdb.getAll()
        docs_scores = []

        otime = time.time()

        for instance in all:
            score = dict()
            score['url'] = instance['url']
            record = db.findRecord({'url': score['url']})

            score[option] = ranker.pagerankSimilarity(record['words'], instance['score'])

            docs_scores.append(score)

        return (sorted(docs_scores, key=lambda i:i[option], reverse=True), time.time() - otime)

    elif option == 'mix':
        return ([], 0.0)




# here is for printing
def custom_print(option, scores):
    print "Search results: (score, url)"
    for instance in scores:
        print "{}, {}".format(instance[option], instance['url'])

    print " "
    print "Total webpages: {}".format(len(scores))


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
