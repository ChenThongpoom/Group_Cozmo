from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.event
collection = db.user 
a = 'boom'
b = 'gun'
print (collection.find_one({"name": (a)}))
    