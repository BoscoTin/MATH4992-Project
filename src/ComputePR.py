import numpy as np
from scipy.sparse import csc_matrix

import DBManager

MAX_ITERATIONS = 1000

wordcountdb = DBManager.instance('wordcount')
PRdb = DBManager.instance('PRMatrix')

def pageRank(G, s = .85, maxerr = .0001):
    """
    Computes the pagerank for each of the n states
    Parameters
    ----------
    G: matrix representing state transitions
       Gij is a binary value representing a transition from state i to j.
    s: probability of following a transition. 1-s probability of teleporting
       to another state.
    maxerr: if the sum of pageranks between iterations is bellow this we will
            have converged.
    """
    n = len(G)

    # transform G into markov matrix A
    A = csc_matrix(G,dtype=np.float)
    rsums = np.array(A.sum(1))[:,0]
    ri, ci = A.nonzero()
    A.data /= rsums[ri]

    # bool array of sink states
    sink = rsums==0

    # Compute pagerank r until we converge
    ro, r = np.zeros(n), np.ones(n)
    count = 0
    while count < MAX_ITERATIONS:
        print "Doing iteration {}".format(count)
    #while np.sum(np.abs(r-ro)) > maxerr:
        ro = r.copy()
        # calculate each pagerank at a time
        for i in xrange(0,n):
            # inlinks of state i
            Ai = np.array(A[:,i].todense())[:,0]
            # account for sink states
            Di = sink / float(n)
            # account for teleportation to state i
            Ei = np.ones(n) / float(n)

            r[i] = ro.dot( Ai*s + Di*s + Ei*(1-s) )

        count += 1

    # return normalized pagerank
    return r/float(sum(r))




if __name__=='__main__':
    # array storing links in database
    links = []
    all = wordcountdb.getAll()

    toDict = []

    # append all links
    for instance in all:
        element = dict()
        links.append(instance['url'])
        element['url'] = instance['url']
        element['children'] = instance['children']

        toDict.append(element)

    # sort
    links = sorted(links)
    sorted_all = sorted(toDict, key=lambda i:i['url'])

    PRArray = []
    for instance in sorted_all:
        linkToArray = np.zeros(len(links))
        children = instance['children']
        index = 0

        for link in children:
            try:
                index = links.index(link)
                linkToArray[index] = 1
            except ValueError:
                continue
        PRArray.append(linkToArray)

    for element in PRArray:
        print element

    num_results =  pageRank(PRArray,s=.86)
    i = 0
    while i < len(num_results):
        print "{}, {}".format(links[i], num_results[i])
        PRdb.insert({
            'url': links[i],
            'score': num_results[i]
        })
        i += 1
