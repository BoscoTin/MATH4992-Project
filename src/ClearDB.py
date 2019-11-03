import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)
db = client['MATH4992']

db.wordcount.drop()
db.PRMatrix.drop()
