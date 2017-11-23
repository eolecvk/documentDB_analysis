"""
Mongodb connection handler
"""
import pymongo
_mongodb = None

def get_db(db="tweet_database", host="localhost", port=27017):
	global _mongodb
	if _mongodb is None:
		client = pymongo.MongoClient(host, port)
		_mongodb = client['db']
	return _mongodb