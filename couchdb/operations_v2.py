import os
import simplejson as json
import requests
# r = requests.get('http://127.0.0.1:5984')
# print(r.status_code)#200
# print(r.headers['content-type'])#'application/json; charset=utf8'
# print(r.encoding)#'utf-8'
# print(r.text) #u'{"type":"User"...'


def put(db_address, tweet_str, tweet_id, v=0):
    """
    puts record tweet_str in db
    """

    r = requests.put(
        os.path.join(db_address, tweet_id),
        data=tweet_str)
    return r.json()


def create_bulk(db_address, docs, v=0):
    """
    curl -d '{"keys":["bar","baz"]}' \
    -X POST $db_address/_all_docs?include_docs=true
    """
    r = requests.post(
        os.path.join(db_address, '_bulk_docs'),
        json=docs)
    return r.json()


def retrieve_bulk(db_address, keys, v=0):
    """
    curl -d '{"keys":["bar","baz"]}' \
    -X POST $db_address/_all_docs?include_docs=true
    """
    r = requests.post(
        os.path.join(db_address, '_all_docs?include_docs=true'),
        json={'keys': keys})
    return r.json() 


def update_bulk(db_address, keys, v=0):
    pass


db_address="http://127.0.0.1:5984/tweets"
data_dir="/home/eolus/Desktop/DAUPHINE/DBA/dm_data"


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


tweets = []
for fname in os.listdir(data_dir):
    fpath = os.path.join(data_dir, fname)
    with open(fpath, 'r') as fp:
        new_tweet = json.load(fp)
        tweets.append(new_tweet)

response = create_bulk(db_address, tweets)
print(response)