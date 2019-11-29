import math

import operator as op
from functools import reduce
from decimal import Decimal

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

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
            return Decimal(innerProduct / (docLength * math.sqrt(self.queryLen)))
        else:
            return Decimal(0.0)

    # calculate jaccardsim of single document here
    def jaccardSimilarity(self, wordcount, docLength):

        ip = 0.0
        # calculate inner product, d_ik * q_k
        for key in self.query:
            if key in wordcount:
                ip += wordcount[key]

        # return jaccard similarity
        return Decimal(ip / (docLength + self.queryLen + ip))

     # calculate VAE of single document here
    def variationalAutoEncoder(self, wordcount, docLength):
        innerProduct = 0.0
        # calculate inner product, d_ik * q_k
        for key in self.query:
            if key in wordcount:
                innerProduct += wordcount[key] * 1

        # return VAE similarity
        if docLength != 0:
            return Decimal(innerProduct / docLength)  # rC1 / nC1
        else:
            return Decimal(0.0)

    # calculate PR similarity based on keywords
    def pagerankSimilarity(self, wordcount, score, total):
        contains = 0
        for key in self.query:
            if key in wordcount.keys():
                contains += 1

        return (
            Decimal(score) * Decimal( math.exp(contains) )
        )

    # mix with pr
    def mixSimilarity(self, url, prscore, coss, jacs, vaes):
        score = prscore

        for i in coss:
            if i['url'] == url:
                score = score + i['score']
                break

        # for i in jacs:
        #     if i['url'] == url:
        #         score = score + i['score']
        #         break
        #
        # for i in vaes:
        #     if i['url'] == url:
        #         score = score + i['score']
        #         break

        return score
