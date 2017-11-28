from urllib.parse import urljoin
import simplejson as json
import requests

from mycouchdb.conn import get_address_server
from mycouchdb.conn import get_address_db

# Database create/delete
def create_db():
    """
    curl -X PUT db_address
    """
    address_db = get_address_db()
    r = requests.put(address_db)
    #server = get_server()
    #db = get_db()
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
    address_all_db = '/'.join([address_server, '_all_dbs']) 
    for name_db in requests.get(address_all_db).json():
        print("Delete DB: {name_db}".format(name_db=name_db))
        address_db = '/'.join([address_server, name_db])
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



def create_bulk(docs):
    """
    curl -d '{"keys":["bar","baz"]}' \
    -X POST db_address/_bulk_docs
    """
    address_db = get_address_db()
    address_docs = '/'.join([address_db, '_bulk_docs'])
    r = requests.post(address_docs, json={'docs' : docs})
    print("nb records created:", len(r.json()))
    return r.json()


# --retrieve
def retrieve(key):
    """
    curl $db_address/$key
    """
    address_db = get_address_db()
    address_doc = '/'.join([address_db, key])
    r = requests.get(address_doc)
    return r.json()


def create_view(view_json):
    address_db = get_address_db()
    url = '/'.join([address_db,"_design/tweets"])
    r = requests.put(url, json=view_json)
    print(r.json())
    return r.json()


def retrieve_all_views():
    """
    curl -X \
    GET '{db}/_all_docs?startkey="_design/"&endkey="_design0"&include_docs=true'
    """
    address_db = get_address_db()
    url = '{}/_all_docs?startkey="_design/"&endkey="_design0"&include_docs=true'.format(address_db)
    r = requests.get(url)
    designs = r.json()['rows']
    return designs


def update_view(view_json):
    designs = retrieve_all_views()
    for design in designs:
        if design['id'] == view_json["_id"]:
            view_json['_rev'] = design['value']['rev']
            break
    r = create_view(view_json)
    return r


def query(view_name):
    address_db = get_address_db()
    url="{}/_design/tweets/_view/{}".format(address_db, view_name)
    r = requests.get(url)
    records = r.json()['rows']
    print("nb matches: {}".format(len(records)))
    return records


def query_temp_view(mapfun):
    """
    curl -d '{"keys":["bar","baz"]}' \
    -X POST $db_address/_all_docs?include_docs=true
    """
    address_db = get_address_db()
    address_temp_view = '/'.join([address_db, "_temp_view"])
    headers = {'content-type' : 'application/json'}

    r = requests.post(address_temp_view,
        json={'map' : mapfun},
        headers=headers)
    print("nb records found:", r.json()['total_rows'])  
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
    r_post = requests.post(address_doc, json={'docs' : doc})
    return r_post.json()


def update_bulk(view_name, mapfun=None, update={}):
    """
    curl -d '{
    "docs":[\
        {"key":"baz","name":"bazzel"}, \
        {"key":"bar","name":"barry"}   \
    ]}' \
    -X POST $address_db/_bulk_docs
    """

    # https://stackoverflow.com/questions/6983930/
    # bulk-updating-a-couchdb-database-without-a-rev-value-per-document
    def update_docs(docs, update):
        docs_updated = []
        for doc in docs:
            doc_updated = doc
            for k, v in update.items():
                doc_updated[k] = v
                docs_updated.append(doc_updated)
        return docs_updated

    #docs = retrieve_bulk(mapfun=mapfun)['rows']
    docs = query(view_name=view_name)
    docs_updated = update_docs(docs, update)
    r = create_bulk(docs_updated)
    return r


def delete(key):
    address_db = get_address_db()
    address_doc = '/'.join([address_db, key])
    r = requests.delete(address_doc)
    return r.json()


def delete_bulk(view_name="not_popular"):
    """
    CF
    https://web.archive.org/web/20111030013313/...
    ...http://lenaherrmann.net/2009/12/22/...
    ...bulk-deletion-of-documents-in-couchdb
    """
    r = update_bulk(view_name=view_name, update={'_deleted' : True})
    return r


if __name__ == "__main__":
    
    pass