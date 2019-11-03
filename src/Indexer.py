import math

class Indexer:
    # TODO: get database db here
    def __init__(self):
        self.wordcount = 0
        self.PRmatrix = 0


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

def process(parentLink, words, childLinks):
    indexer = Indexer()
    wordCountMap = indexer.wordCount(words)

    for word in wordCountMap:
        print "({}, {})".format(word, wordCountMap[word])

    cossim = indexer.preprocessCosSim(wordCountMap)
    jaccardsim = indexer.preprocessJaccardSim(wordCountMap)

    print cossim
    print jaccardsim
