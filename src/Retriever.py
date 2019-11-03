import DBManager
from Ranker import Ranker

db = DBManager.instance('wordcount')

total = db.getTotal()

print total

all = db.getAll()

ranker = Ranker(['machine', 'learning'])

docs_scores = []


for instance in all:
    score = dict()
    # print "{}".format(instance['url'])
    score['url'] = instance['url']
    score['cossim'] = ranker.cosineSimilarity(instance['words'], instance['cos'])
    score['jaccard'] = ranker.jaccardSimilarity(instance['words'], instance['jaccard'])

    docs_scores.append(score)


sorted_scores = sorted(docs_scores, key=lambda i:i['cossim'], reverse=T)

for instance in sorted_scores:
    print instance['url']
