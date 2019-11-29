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
import time

testRank = []
times = time.time()
# 1 to 100
for i in range(1, len(wordlist) + 1):
    for j in range(20):
        # do search with picking i keywords
        samples = random.sample(range(len(wordlist)), i)
        words = []
        for index in samples:
            words.append(wordlist[index])

        # get the rank here
        scores, etime = Retriever.rank(option, words)

        rank = 0
        for score in scores:
            if score['url'] == desiredPage:
                break
            rank += 1

        testRank.append( (i, rank + 1) )
        print "{}, {}".format(i, rank + 1)

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

# regression
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
quadratic = np.polyfit(x,y,2)
quad_trend = np.poly1d(quadratic)
cubic = np.polyfit(x,y,3)
cubic_trend = np.poly1d(cubic)

print slope
print intercept
print r_value
print p_value
print std_err
print ""
print "Done with {} times search".format( len(wordlist) * 20 )
#print "Time elapsed = {} s".format( (time.time() - times) / 1000 )

title = ""
if option == 'cos':
    title = "Cosine similarity"
elif option == 'jac':
    title = "Jaccard similarity"
elif option == 'vae':
    title = "Variational Auto Encoder"
elif option == 'pr':
    title = "Page Rank"

plt.title(title)
# plt.plot(x,y, '.', label="original data")
plt.plot(x, intercept + slope * x, 'r', label='linear regression')
plt.plot(x, quad_trend(x), 'g', label='quadratic fit')
plt.plot(x, cubic_trend(x), 'b', label='cubic fit')
plt.legend()
plt.show()
