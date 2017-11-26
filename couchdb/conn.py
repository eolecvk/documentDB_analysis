
import couchdb

_server = None
_db = None

def get_server(url='http://localhost:5984/'):
	global _server
	if _server server is None:
	    _server = couchdb.Server(url)
	return _server

def get_db(db_name="twitter_data"):
	global _db
	if _db is None:
		_db = server.create(db_name)
	return _db