import DBManager

db = DBManager.instance('wordcount')

instance = db.getAll()
record = db.findRecord({'url':'http://www.cse.ust.hk/'})

for object in instance:
    print object

print record
