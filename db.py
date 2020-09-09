
from creds import creds
from pymongo import MongoClient

dbClient = MongoClient(f"mongodb+srv://{creds.get('dbUser')}:{creds.get('dbPass')}@cluster0.xzpda.mongodb.net/flex?retryWrites=true&w=majority")
db = dbClient.flex

def getUser(username):
    return db.users.find_one({"username": username})
