"""
- save tweet to .json
- load tweet from .json
"""

import simplejson as json

def json_save(tweet, save_dir):
    """
    save tweet to .json
    """
    from os.path import join
    fname = "{}.json".format(tweet['id_str'])
    fpath = join(save_dir, fname)
    with open(fpath, 'w') as fp:
        json.dump(tweet, fp)

def json_load(fpath):
    """
    load tweet from .json
    """
    import simplejson as json
    with open(fpath, 'r') as fp:
        tweet =json.load(fp)
    return tweet