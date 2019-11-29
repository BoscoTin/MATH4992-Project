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

    all = db.getAll()

    docs_scores = []

    otime = time.time()

    if option != 'mix':
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
            elif option == 'pr':
                score[option] = ranker.pagerankSimilarity(wordlist, instance[option], instance['total'])
            else:
                break

            docs_scores.append(score)
    else:
        coss = []
        jacs = []
        vaes = []
        prs = []

        for instance in all:
            wordlist = instance['words']
            for opt in ['cos', 'jac', 'vae', 'pr']:
                score = dict()
                score['url'] = instance['url']
                if opt == 'cos':
                    score['score'] = ranker.cosineSimilarity(wordlist, instance[opt])
                    coss.append(score)
                elif opt == 'jac':
                    score['score'] = ranker.jaccardSimilarity(wordlist, instance[opt])
                    jacs.append(score)
                elif opt == 'vae':
                    score['score'] = ranker.variationalAutoEncoder(wordlist, instance[opt])
                    vaes.append(score)
                elif opt == 'pr':
                    score['score'] = ranker.pagerankSimilarity(wordlist, instance[opt], instance['total'])
                    prs.append(score)
                else:
                    break

        sorted_cos = sorted(coss, key=lambda i:i['score'], reverse=True)
        sorted_jac = sorted(jacs, key=lambda i:i['score'], reverse=True)
        sorted_vae = sorted(vaes, key=lambda i:i['score'], reverse=True)
        sorted_pr = sorted(prs, key=lambda i:i['score'], reverse=True)


        # normalize
        for instance in sorted_cos:
            instance['score'] = instance['score'] / sorted_cos[0]['score']
        for instance in sorted_jac:
            instance['score'] = instance['score'] / sorted_jac[0]['score']
        for instance in sorted_vae:
            instance['score'] = instance['score'] / sorted_vae[0]['score']

        # mix scores
        for instance in sorted_pr:
            score = dict()
            score['url'] = instance['url']
            prscore = instance['score'] / sorted_pr[0]['score']
            score[option] = ranker.mixSimilarity(instance['url'], prscore, sorted_cos, sorted_jac, sorted_vae)
            docs_scores.append(score)

    sorted_scores = sorted(docs_scores, key=lambda i:i[option], reverse=True)

    return (sorted_scores, time.time() - otime)



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
    sys.exit()


def main():
    argv = sys.argv
    # search if option exists
    if "-option" in argv:
        index = argv.index("-option")
        option = argv[index + 1]
        options = ['cos', 'jac', 'vae', 'pr', 'mix']
        if option not in options:
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
        print Porter.stem(word)

    scores, usedTime = rank(option, processedWords)

    custom_print(option, scores)

    print "The search takes {} ms".format(usedTime)

if __name__ == "__main__":
    main()
