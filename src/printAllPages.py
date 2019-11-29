import DBManager
db = DBManager.instance('wordcount')

all = db.getAll()

links = []

for instance in all:
    print instance['url']
    print instance['cos']
    print instance['jac']
    print instance['vae']
    print instance['pr']

#sortedLinks = sorted(links)

#for link in sortedLinks:
#    print link
