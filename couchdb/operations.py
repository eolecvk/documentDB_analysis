import os
import simplejson as json
import requests
# r = requests.get('http://127.0.0.1:5984')
# print(r.status_code)#200
# print(r.headers['content-type'])#'application/json; charset=utf8'
# print(r.encoding)#'utf-8'
# print(r.text) #u'{"type":"User"...'

from couchdb.conn import get_address_server
from couchdb.conn import get_address_db


# Database create/delete
def create_db():
    """
    curl -X PUT db_address
    """
    address_db = get_address_db()
    r = requests.put(address_db)
    return r.json()


def delete_db():
    """
    curl -X DELETE db_address
    """
    address_db = get_address_db()
    r = requests.delete(address_db)
    return r.json()


def delete_all_db():
    address_server = get_address_server()
    address_all_db = os.path.join(address_server, '_all_dbs') 
    for name_db in requests.get(address_all_db).json():
        print("Delete DB: {name_db}".format(name_db=name_db))
        address_db = os.path.join(address_server, name_db)
        r = delete_db(address_db)
        print(r)




# Basic operations (CRUD)
# --create
def create(doc):
    """
    curl –X PUT db_address doc_id \
    -d '{"keys":["bar","baz"]}'
    """
    address_db = get_address_db()
    doc_id = doc['id_str']
    address_doc = os.path.join(address_db, doc_id)
    r = requests.put(address_doc, json=doc)
    return r.json()

def create_bulk(docs):
    """
    curl -d '{"keys":["bar","baz"]}' \
    -X POST db_address/_bulk_docs
    """
    address_db = get_address_db()
    address_docs = os.path.join(address_db, '_bulk_docs')
    r = requests.post(address_docs, json=docs)
    return r.json()

# --retrieve
def retrieve(key):
    """
    curl $db_address/$key
    """
    address_db = get_address_db()
    address_doc = os.path.join(address_db, key)
    r = requests.get(address_doc)
    return r.json()

def retrieve_bulk(keys, mapfun):
    """
    curl -d '{"keys":["bar","baz"]}' \
    -X POST $db_address/_all_docs?include_docs=true
    """
    address_db = get_address_db()

    if keys is not None:
        address_docs = os.path.join(address_db, '_all_docs?include_docs=true')
        r = requests.post(address_docs, json={'keys': keys})
    elif mapfun is not None:
        address_temp_view = os.join.path(address_db, "_temp_view")
        r = requests.post(address_temp_view, mapfun)
    return r.json()



# --update
def update(doc):
    """
    curl -X PUT $address_doc \
    -d '{ "field" : "value", "_rev" : "revision id" }
    """
    address_db = get_address_db()
    key = doc['id']
    r_get = retrieve(address_db, key)
    r_get_json = r_get.json()
    doc['_rev'] = r_get_json['_rev']
    r_post = requests.post(address_doc, json=doc)
    return r_post.json()


def update_bulk(docs):
    """
    curl -d '{
    "docs":[\
        {"key":"baz","name":"bazzel"}, \
        {"key":"bar","name":"barry"}   \
    ]}' \
    -X POST $address_db/_bulk_docs
    """
    # https://stackoverflow.com/questions/6983930/bulk-updating-a-couchdb-database-without-a-rev-value-per-document
    address_db = get_address_db()
    address_docs = os.path.join(address_db, "_bulk_docs")
    r_post = requests.post(address_docs, json={'docs' : docs})
    return r_post.json()


def delete(key):
    address_db = get_address_db()
    address_doc = os.path.join(address_db, key)
    r = requests.delete(address_doc)
    return r.json()


def delete_bulk(keys):
    """
    CF
    https://web.archive.org/web/20111030013313/...
    ...http://lenaherrmann.net/2009/12/22/...
    ...bulk-deletion-of-documents-in-couchdb
    """
    def add_deletion_attr(doc):
        doc['_deleted'] = True
        return doc
    #--end of subroutine
    r = retrieve_bulk(keys)
    docs = [ add_deletion_attr(doc) for doc in r['rows'] ]
    update_bulk(docs)


if __name__ == "__main__":

    # Connection configs
    data_dir="/home/eolus/Desktop/DAUPHINE/DBA/dm_data"
    address_server = "http://127.0.0.1:5984"
    name_db = "tweets"
    address_db = os.path.join(address_server, name_db)

    # Load dataset
    #from utils import load_dataset
    #dataset = load_dataset(data_dir)
    
    r = delete_all_db(address_server)
    print(r)

# for fname in os.listdir(data_dir):
#     fpath = os.path.join(data_dir, fname)
#     with open(fpath, 'r') as fp:
#         tweet_dict = json.load(fp)
#     tweet_str = json.dumps(tweet_dict)
#     tweet_id = tweet_dict['id']
#     try:
#         put(db_address, tweet_str, tweet_id)
#     except Exception as e:
#         print(e)

# /HTTP_Bulk_Document_API
# https://wiki.apache.org/couchdb/HTTP_Bulk_Document_API

# keys = [
# '930436288011841536',
# '930425596747841537'
# ]
# response = retrieve(db_address, keys, v=0)


# print(len(response['rows']))
# #for row in response['rows']:
# #    print(row['id'])


# tweets = []
# for fname in os.listdir(data_dir):
#     fpath = os.path.join(data_dir, fname)
#     with open(fpath, 'r') as fp:
#         new_tweet = json.load(fp)
#         tweets.append(new_tweet)

# response = create_bulk(db_address, tweets)
# print(response)