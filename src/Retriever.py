import sys

import DBManager
from Ranker import Ranker

db = DBManager.instance('wordcount')

# function to rank by search option
def rank(option, keywords):
    all = db.getAll()

    ranker = Ranker(keywords)

    docs_scores = []


    for instance in all:
        score = dict()
        # print "{}".format(instance['url'])
        score['url'] = instance['url']
        score['cos'] = ranker.cosineSimilarity(instance['words'], instance['cos'])
        score['jac'] = ranker.jaccardSimilarity(instance['words'], instance['jaccard'])

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

    scores = rank(option, keywords)

    custom_print(option, scores)


if __name__ == "__main__":
    main()
