import math

class Ranker:

    # given a dict() object of query, store it as private member
    def __init__(self, query):
        self.query = query

        queryLen = 0
        for key in query:
            queryLen += 1 # Take keyword length as 1

        self.queryLen = queryLen

    # calculate cossim of single document here
    def cosineSimilarity(self, wordcount, docLength):

        innerProduct = 0
        # calculate inner product, d_ik * q_k
        for key in self.query:
            innerProduct += wordcount[key] * self.query[key]

        # return cosine similarity
        return innerProduct / (docLength * math.sqrt(self.queryLen))

    # calculate jaccardsim of single document here
    def jaccardSimilarity(self, wordcount, docLength):

        innerProduct = 0
        # calculate inner product, d_ik * q_k
        for key in self.query:
            innerProduct += wordcount[key] * self.query[key]

        # return jaccard similarity
        return innerProduct / (docLength + self.queryLen + innerProduct)
