import DBManager
db = DBManager.instance('wordcount')

all = db.getAll()

links = []

for instance in all:
    links.append(instance['url'])

sortedLinks = sorted(links)

for link in sortedLinks:
    print link
