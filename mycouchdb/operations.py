import os
import simplejson as json
import requests
# r = requests.get('http://127.0.0.1:5984')
# print(r.status_code)#200
# print(r.headers['content-type'])#'application/json; charset=utf8'
# print(r.encoding)#'utf-8'
# print(r.text) #u'{"type":"User"...'

from mycouchdb.conn import get_address_server
from mycouchdb.conn import get_address_db
from mycouchdb.conn import get_server
from mycouchdb.conn import get_db

# Database create/delete
def create_db():
    """
    curl -X PUT db_address
    """
    address_db = get_address_db()
    r = requests.put(address_db)
    server = get_server()
    db = get_db()
    return r.json()


def delete_db(address_db=None):
    """
    curl -X DELETE db_address
    """
    if address_db is None:
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
# def create(doc):
#     """
#     curl –X PUT db_address doc_id \
#     -d '{"keys":["bar","baz"]}'
#     """
#     address_db = get_address_db()
#     doc_id = doc['id_str']
#     address_doc = os.path.join(address_db, doc_id)
#     r = requests.put(address_doc, json={'docs' : docs})
#     return r.json()

def create_bulk(docs):
    """
    curl -d '{"keys":["bar","baz"]}' \
    -X POST db_address/_bulk_docs
    """
    address_db = get_address_db()
    address_docs = os.path.join(address_db, '_bulk_docs')
    r = requests.post(address_docs, json={'docs' : docs})
    return r.json()


# --retrieve
# def retrieve(key):
#     """
#     curl $db_address/$key
#     """
#     address_db = get_address_db()
#     address_doc = os.path.join(address_db, key)
#     r = requests.get(address_doc)
#     return r.json()



def retrieve_bulk(mapfun):
    """
    curl -d '{"keys":["bar","baz"]}' \
    -X POST $db_address/_all_docs?include_docs=true
    """
    # address_db = get_address_db()
    # address_temp_view = os.path.join(address_db, "_temp_view")
    # headers = {'content-type' : 'application/json'}

    # r = requests.post(address_temp_view,
    #     json={'map' : mapfun},
    #     headers=headers)    
    # return r.json()
    import couchdb
    server = couchdb.Server()
    db = server['twitter_data']
    results = db.query(mapfun)
    return list(results)



# --update
def update(doc):
    """
    curl -X PUT $address_doc \
    -d '{ "field" : "value", "_rev" : "revision id" }
    """
    # address_db = get_address_db()
    # key = doc['id']
    # r_get = retrieve(address_db, key)
    # r_get_json = r_get.json()
    # doc['_rev'] = r_get_json['_rev']
    # r_post = requests.post(address_doc, json={'docs' : doc})
    # return r_post.json()


def update_bulk(docs=[], mapfun=None, update={}):
    """
    curl -d '{
    "docs":[\
        {"key":"baz","name":"bazzel"}, \
        {"key":"bar","name":"barry"}   \
    ]}' \
    -X POST $address_db/_bulk_docs
    """
    assert (
        (docs != [] or (mapfun is not None and update != {})) and not
        (docs != [] and mapfun is not None)),(
        """"Set keys or a map function (but not both)
        mapfun={},
        update={}
        """.format(mapfun, json.dumps(update, indent=2)))
    # https://stackoverflow.com/questions/6983930/bulk-updating-a-couchdb-database-without-a-rev-value-per-document
    
    # Get docs and update them manually
    if mapfun is not None and update is not {}:

        docs = retrieve_bulk(mapfun=mapfun)
        docs_updated = []
        for doc in docs:
            doc_updated = doc
            for k, v in update.items():
                doc_updated[k] = v
            docs_updated.append(doc_updated)

    # Insert docs in db
    address_db = get_address_db()
    address_docs = os.path.join(address_db, "_bulk_docs")
    r_post = requests.post(address_docs, json={'docs' : docs})
    return r_post.json()


def delete(key):
    address_db = get_address_db()
    address_doc = os.path.join(address_db, key)
    r = requests.delete(address_doc)
    return r.json()


def delete_bulk(mapfun=None):
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

    r = retrieve_bulk(mapfun=mapfun)
    docs = [ add_deletion_attr(doc) for doc in r ]

    if len(docs) != 0:
        r = update_bulk(docs=docs)
        return r
    return


if __name__ == "__main__":
    pass