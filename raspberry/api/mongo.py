from pymongo import MongoClient

def get_collection():
    client = MongoClient("db", 27017)

    return client["database"]["data"]
