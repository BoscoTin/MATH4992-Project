import sys
import Retriever
import DBManager

# for scanning arguments
argv = sys.argv
if "-option" in argv:
    index = argv.index("-option")
    option = argv[index + 1]
    if option != 'cos' and option != 'jac' and option != 'vae' and option != 'pr':
        print "Option lists: cos jac vae pr"
        print "with tag -option"
        sys.exit()
else:
    print "Option lists: cos jac vae pr"
    print "with tag -option"
    sys.exit()


desiredPage = 'http://www.cse.ust.hk/'

# get all words from desired webpages
db = DBManager.instance('wordcount')
record = db.findRecord({'url': desiredPage})
wordlist = record['words'].keys()


# do testing, with each test 50 times
import random

testRank = []
# 1 to 100
for i in range(1, len(wordlist) + 1):
    for j in range(10):
        # do search with picking i keywords
        samples = random.sample(range(len(wordlist)), i)
        words = []
        for index in samples:
            words.append(wordlist[index])

        # get the rank here
        scores, time = Retriever.rank(option, words)

        rank = 0
        for score in scores:
            if score['url'] == desiredPage:
                break
            rank += 1

        testRank.append( (i, rank + 1) )

# linear regression
import numpy as np
import scipy
import matplotlib.pyplot as plt

x = []
y = []
for tuple in testRank:
    x.append(tuple[0])
    y.append(tuple[1])

x = np.array(x)
y = np.array(y)


slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)

print slope
print intercept
print r_value
print p_value
print std_err

plt.plot(x,y, '.', label="original data")
plt.plot(x, intercept + slope * x, 'r', label='fitted line')
plt.legend()
plt.show()
