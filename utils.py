"""
- save tweet to .json
- load tweet from .json
- load list of dict based on dir containing .json files
"""

import os
import simplejson as json
from timeit import default_timer


def json_save(tweet, save_dir):
    """
    save tweet to .json
    """
    fname = "{}.json".format(tweet['id_str'])
    fpath = os.path.join(save_dir, fname)
    with open(fpath, 'w') as fp:
        json.dump(tweet, fp)


def json_load(fpath):
    """
    load tweet from .json
    """
    with open(fpath, 'r') as fp:
        tweet =json.load(fp)
    return tweet


def load_dataset(dataset_dir, n=None):
    """
    Read tweets from .json files in a given dir
    returns tweet dataset as list of dicts
    """
    fnames = os.listdir(dataset_dir)
    fpaths = [ os.path.join(dataset_dir, fname)
               for fname in fnames ]
    if n is not None: fpaths = fpaths[:n]
    tweets = [ json_load(fpath) for fpath in fpaths ]
    return tweets


def pprint_dict(in_dict):
    print(json.dumps(in_dict, indent=2))


def timer(f, **kwargs):
    start = default_timer()   # Start timer
    r = f(**kwargs)
    end = default_timer()     # End timer
    time_delta = end - start  # Get runtime
    return time_delta, r