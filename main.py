"""
test functions for CRUD operations
"""

from mongodb.operations import create_batch   # C
from mongodb.operations import retrieve_batch # R
from mongodb.operations import update_batch   # U
from mongodb.operations import delete_batch   # D


# utility: load dataset in memory
def load_dataset(dataset_dir, n):
    """
    returns tweet dataset as list of dicts
    """
    from os import listdir
    from os.path import join
    from utils.json_utils import json_load

    fnames = listdir(dataset_dir)
    fpaths = [ join(dataset_dir, fname) for fname in fnames ]
    tweets = [ json_load(fpath) for fpath in fpaths[:n] ]
    return tweets

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

    start = default_timer()
    create_batch(tweets)
    end = default_timer()
    time_delta = end - start

    return time_delta





if __name__ == "__main__":

    dataset_dir = "/home/eolus/Desktop/DAUPHINE/DBA/dm_data"

    test_create(dataset_dir, n=10000, db="mongo_db")



    
