"""
test runtime for CRUD operations
"""
from mongodb.operations import delete_all_db

from mongodb.operations import create_batch   # C
from mongodb.operations import retrieve_batch # R
from mongodb.operations import update_batch   # U
from mongodb.operations import delete_batch   # D



def pprint_dict(in_dict):
    import simplejson as json
    print(json.dumps(in_dict, indent=2))


def load_dataset(dataset_dir):
    """
    Read tweets from .json files in a given dir
    returns tweet dataset as list of dicts
    """
    from os import listdir
    from os.path import join
    from utils.json_utils import json_load

    fnames = listdir(dataset_dir)
    fpaths = [ join(dataset_dir, fname) for fname in fnames ]
    tweets = [ json_load(fpath) for fpath in fpaths ]
    return tweets



def timer(f, **kwargs):
    from timeit import default_timer
    start = default_timer()   # Start timer
    f(**kwargs)
    end = default_timer()     # End timer
    time_delta = end - start  # Get runtime
    return time_delta


if __name__ == "__main__":

    # input data
    dataset_dir = "/home/eolus/Desktop/DAUPHINE/DBA/dm_data"
    tweets = load_dataset(dataset_dir)

    # log
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

    # run test for various data size
    for n in [1, 100, 1000, 10000, 90000]:

        # tests attributes
        kw_create   = { 'tweets' : tweets[:n] }
        kw_retrieve = { 'filter' : { 'lang' : 'fr' } }
        kw_update   = { 'filter' : { 'lang' : 'en' },
                        'update' : {
                        '$set' : { 'lang' : 'eng' } }
                        }
        kw_delete   = { 'filter' : { 'lang' : 'fr' } }

        delete_all_db() # reset DB
        
        for f, f_name, kw in [
            (create_batch, 'create', kw_create),
            (retrieve_batch, 'retrieve', kw_retrieve),
            (update_batch, 'update', kw_update),
            (delete_batch, 'delete', kw_delete)
        ] :
            rt = timer(f, **kw)
            logs['mongodb'][f_name][n] = rt

    pprint_dict(logs)

    
