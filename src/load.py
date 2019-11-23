import DBManager

db = DBManager.instance('wordcount')

instance = db.findRecord({'url': 'http://www.cse.ust.hk'})

for word in instance['words']:
    print word
