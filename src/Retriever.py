import sys

import DBManager
from Ranker import Ranker

from nltk.stem import PorterStemmer

db = DBManager.instance('wordcount')

# function to rank by search option
def rank(option, keywords):
    all = db.getAll()

    ranker = Ranker(keywords)

    docs_scores = []


    for instance in all:
        score = dict()

        wordlist = instance['words']

        score['url'] = instance['url']
        score['cos'] = ranker.cosineSimilarity(wordlist, instance['cos'])
        score['jac'] = ranker.jaccardSimilarity(wordlist, instance['jaccard'])
        score['vae'] = ranker.variationalAutoEncoder(wordlist, instance['vae'])

        docs_scores.append(score)

    sorted_scores = sorted(docs_scores, key=lambda i:i[option], reverse=True)

    return sorted_scores


def custom_print(option, scores):
    for instance in scores:
        print "{}, {}".format(instance[option], instance['url'])



def terminate():
    print "Run option: python [path]/Retriever.py [control] [parameter]"
    print "Parameter list:"
    print "-option :"
    print "     cos: cosine similarity measure"
    print "     jac: jaccard similarity measure"
    print "     vae: variational auto encoder measure"


def main():
    argv = sys.argv
    # search if option exists
    if "-option" in argv:
        index = argv.index("-option")
        option = argv[index + 1]
        if option != 'cos' and option != 'jac' and option != 'vae':
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

    scores = rank(option, processedWords)

    custom_print(option, scores)


if __name__ == "__main__":
    main()
