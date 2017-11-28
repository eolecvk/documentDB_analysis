
import couchdb


_address_server = 'http://localhost:5984'
_address_db = 'http://localhost:5984/twitter_data'
_server = None
_db = None

def get_address_server():
    global _address_server
    if _address_server is None:
        _address_server = 'http://localhost:5984'
    return _address_server

def get_address_db():
    global _address_db
    if _address_db is None:
        _address_db = 'http://localhost:5984/twitter_data'
    return _address_db



