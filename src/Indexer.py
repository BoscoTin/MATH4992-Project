import math

class Indexer:
    def preprocessCosSim(self, words):
        # words is a dict()
        # return document length (vector length)
        sum = 0
        for key in words:
            sum += words[key]**2
        return math.sqrt(sum)

    def preprocessJaccardSim(self, words):
        # return document length (vector length)
        # cossim need to sqrt but here no need
        sum = 0
        for key in words:
            sum += words[key]**2
        return sum


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
