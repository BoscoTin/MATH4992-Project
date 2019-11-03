import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)
db = client['MATH4992']

class DBManager:
    def __init__(self, collection):
        self.collection = collection

    def insert(self, data):
        collection = db[self.collection]
        collection.insert_one(data)

    def findRecord(self, parameter):
        collection = db[self.collection]
        return collection.find_one(parameter)

    def getTotal(self):
        collection = db[self.collection]
        return collection.find().count()

    def getAll(self):
        collection = db[self.collection]
        return collection.find()

    def update(self, condition, data):
        collection = db[self.collection]
        record = collection.find_one(condition)
        for key in data:
            record[key] = data[key]
        return self.collection.update(condition, record)



def instance(collection):
    db = DBManager(collection)
    return db
