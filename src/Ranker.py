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
            if key in wordcount:
                innerProduct += wordcount[key]

        # return cosine similarity
        if docLength != 0:
            return innerProduct / (docLength * math.sqrt(self.queryLen))
        else:
            return 0.0

    # calculate jaccardsim of single document here
    def jaccardSimilarity(self, wordcount, docLength):

        ip = 0.0
        # calculate inner product, d_ik * q_k
        for key in self.query:
            if key in wordcount:
                ip += wordcount[key]

        # return jaccard similarity
        return (ip / (docLength + self.queryLen + ip))

     # calculate VAE of single document here
    def variationalAutoEncoder(self, wordcount, docLength):
        innerProduct = 0.0
        # calculate inner product, d_ik * q_k
        for key in self.query:
            if key in wordcount:
                innerProduct += wordcount[key] * 1

        # return VAE similarity
        if docLength != 0:
            return innerProduct / docLength  # rC1 / nC1
        else:
            return 0.0
