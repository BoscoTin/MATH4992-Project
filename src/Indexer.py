import math
import DBManager

class Indexer:
    def __init__(self):
        self.wordcountdb = DBManager.instance('wordcount')

    # main program here
    def process(self, parentLink, words, childLinks):
        # count the number of words here
        wordCountMap = self.wordCount(words)

        # pre-calculate the stuffs that independent of query
        cossim = self.preprocessCosSim(wordCountMap)
        jaccardsim = self.preprocessJaccardSim(wordCountMap)
        vaesum = self.preprocessVAE(wordCountMap)

        self.wordcountdb.insert({
            'url': parentLink,
            'words': wordCountMap,
            'cos': cossim,
            'jac': jaccardsim,
            'vae': vaesum,
            'children': childLinks
        })

    # words is a dict()
    # return document length (vector length)
    def preprocessCosSim(self, words):
        sum = 0
        for key in words:
            sum += words[key]**2
        return math.sqrt(sum)

    # return document length (vector length)
    # cossim need to sqrt but here no need
    def preprocessJaccardSim(self, words):
        sum = 0
        for key in words:
            sum += words[key]**2
        return sum

    def preprocessVAE(self, words):
        sum = 0
        for key in words:
            sum += words[key]
        return sum


    # function to count the words and return a json array as
    # {
    #   [word]: word_count,
    #   [word]: word_count, ...
    # }
    def wordCount(self, words):
        map = dict()
        for word in words:
            if word not in map.keys():
                map[word] = 1
            else:
                map[word] += 1

        return map
