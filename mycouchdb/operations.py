from urllib.parse import urljoin
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
    address_all_db = urljoin(address_server, '_all_dbs') 
    for name_db in requests.get(address_all_db).json():
        print("Delete DB: {name_db}".format(name_db=name_db))
        address_db = urljoin(address_server, name_db)
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
    doc_id = doc['_id']
    address_doc = "{address_db}/{doc_id}".format(address_db=address_db,
        doc_id=doc_id)
    r = requests.put(address_doc, json={'docs' : doc})
    return r.json()


def create_view(view_json, view_name):
    address_db = get_address_db()
    address_doc = "{address_db}/_design/tweets/_view/{view_name}".format(
        address_db=address_db,
        view_name=view_name)

    r = requests.post(address_doc, json={'docs' : view_json})
    return r.json()




def create_bulk(docs):
    """
    curl -d '{"keys":["bar","baz"]}' \
    -X POST db_address/_bulk_docs
    """
    address_db = get_address_db()
    address_docs = urljoin(address_db, '_bulk_docs')
    r = requests.post(address_docs, json={'docs' : docs})
    print("nb records created:", len(r.json()))
    return r.json()


# --retrieve
def retrieve(key):
    """
    curl $db_address/$key
    """
    address_db = get_address_db()
    address_doc = urljoin(address_db, key)
    r = requests.get(address_doc)
    return r.json()


def retrieve_bulk_v2(view_name):
    """
    curl -d '{"keys":["bar","baz"]}' \
    -X POST $db_address/_all_docs?include_docs=true
    """
    address_db = get_address_db()
    url = "{address_db}/_design/tweets/_view/{view_name}".format(
        address_db=address_db,
        view_name=view_name)
    print(url)
    r = requests.get(url)
    return r.json()


    # address_db = get_address_db()
    # address_temp_view = urljoin(address_db, "_temp_view")
    # headers = {'content-type' : 'application/json'}

    # r = requests.post(address_temp_view,
    #     json={'map' : mapfun},
    #     headers=headers)
    # print("nb records found:", r.json()['total_rows'])  
    # return r.json()



def retrieve_bulk(mapfun):
    """
    curl -d '{"keys":["bar","baz"]}' \
    -X POST $db_address/_all_docs?include_docs=true
    """
    address_db = get_address_db()
    address_temp_view = urljoin(address_db, "_temp_view")
    headers = {'content-type' : 'application/json'}

    r = requests.post(address_temp_view,
        json={'map' : mapfun},
        headers=headers)
    print("nb records found:", r.json()['total_rows'])  
    return r.json()
    #import couchdb
    #server = couchdb.Server()
    #db = server['twitter_data']
    #results = db.query(mapfun)
    #return list(results)



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


def update_bulk(mapfun=None, update={}):
    """
    curl -d '{
    "docs":[\
        {"key":"baz","name":"bazzel"}, \
        {"key":"bar","name":"barry"}   \
    ]}' \
    -X POST $address_db/_bulk_docs
    """

    # https://stackoverflow.com/questions/6983930/bulk-updating-a-couchdb-database-without-a-rev-value-per-document
    def update_docs(docs, update):
        docs_updated = []
        for doc in docs:
            doc_updated = doc
            for k, v in update.items():
                doc_updated[k] = v
                docs_updated.append(doc_updated)
        return docs_updated

    docs = retrieve_bulk(mapfun=mapfun)['rows']
    docs_updated = update_docs(docs, update)
    r = create_bulk(docs_updated)

    return r


def delete(key):
    address_db = get_address_db()
    address_doc = urljoin(address_db, key)
    r = requests.delete(address_doc)
    return r.json()


def delete_bulk(mapfun=None):
    """
    CF
    https://web.archive.org/web/20111030013313/...
    ...http://lenaherrmann.net/2009/12/22/...
    ...bulk-deletion-of-documents-in-couchdb
    """
    r = update_bulk(mapfun=mapfun, update={'_deleted' : True})
    return r


if __name__ == "__main__":
    
    pass