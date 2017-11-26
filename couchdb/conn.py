
_adress_server = 'http://localhost:5984/'
_address_db = 'http://localhost:5984/twitter_data'

def get_address_server():
    global _adress_server
    if _adress_server is None:
        _adress_server = 'http://localhost:5984/'
    return _adress_server

def get_address_db():
    global _address_db
    if _address_db is None:
        _address_db = 'http://localhost:5984/twitter_data'
    return _address_db