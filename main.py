"""
test functions for CRUD operations
"""
from mongodb.operations import add_index
from mongodb.conn import get_collection

from mongodb.operations import create_batch   # C
from mongodb.operations import retrieve_batch # R
from mongodb.operations import update_batch   # U
from mongodb.operations import delete_batch   # D


def load_dataset(dataset_dir, n):
    """
    Read tweets from .json files in a given dir
    returns tweet dataset as list of dicts
    """
    from os import listdir
    from os.path import join
    from utils.json_utils import json_load

    fnames = listdir(dataset_dir)
    fpaths = [ join(dataset_dir, fname) for fname in fnames ]
    tweets = [ json_load(fpath) for fpath in fpaths[:n] ]
    return tweets


def preprocess_tweets(tweets):
    """
    Creates a '_id' key in each tweet dict
    where tweet['_id'] = tweet['id'] 
    """
    preprocessed_tweets = []
    for tweet in tweets:
        preprocessed_tweets.append(add_index(tweet))
    return preprocessed_tweets


# Runtime testing for CRUD operations
# --create
def test_create(dataset_dir, n, db="mongo_db"):
    """
    get runtime execution for n create operations
    in a choosen database (mongodb or couchdb)
    """
    from timeit import default_timer

    assert db in ("mongo_db", "couch_db"),\
    "db should be 'mongo_db' or 'couch_db'"

    tweets = load_dataset(dataset_dir, n)
    #preprocessed_tweets = preprocess_tweets(tweets) # ObjectId indexing?
    preprocessed_tweets = tweets
    collection = get_collection()

    start = default_timer()  # Start timer
    create_batch(preprocessed_tweets, collection)
    end = default_timer()    # End timer
    time_delta = end - start # Get runtime

    return time_delta





if __name__ == "__main__":

    # ENV
    dataset_dir = "/home/eolus/Desktop/DAUPHINE/DBA/dm_data"

    # RESET DB
    def delete_all_db(client):
        for db_name in client.database_names():
            client.drop_database(db_name)
            print("DROPPED DB: {}".format(db_name))

    from mongodb.conn import get_client
    client = get_client()
    delete_all_db(client)
    

    # LOGS
    logs = {
        'mongodb' : {
            'create'  : {},
            'retrieve': {},
            'update'  : {},
            'delete'  : {}
            },
        'couchdb' : {
            'create'  : {},
            'retrieve': {},
            'update'  : {},
            'delete'  : {}
            }
        }

    # TESTS
    # --CREATE
    for n in [500, 5000, 50000]:
        runtime = test_create(dataset_dir, n=n, db="mongo_db")
        logs['mongodb']['create'][n] = runtime

    print(logs)

    
