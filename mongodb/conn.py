"""
Mongodb connection handler
"""
import pymongo
_mongoclient = None
_mongodb = None
_collection = None


def get_client(host="localhost", port=27017):
	global _mongoclient
	if _mongoclient is None:
		_mongoclient = pymongo.MongoClient(host, port)
	return _mongoclient

def get_db(db_name="twitter_data"):
	global _mongodb
	if _mongodb is None:
		client = get_client()
		_mongodb = client[db_name]
	return _mongodb

def get_collection(collection_name="tweets"):
    global _collection
    if _collection is None:
    	mongodb = get_db()
    	_collection = pymongo.collection.Collection(mongodb, collection_name)
    return _collection