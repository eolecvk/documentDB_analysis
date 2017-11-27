"""
test runtime for CRUD operations
"""


from utils import load_dataset
from utils import timer
from utils import pprint_dict


def crud_runtime(dataset, test_size, db="mongodb"):    

    if db not in ["mongodb", "couchdb"]:
        print("db should be in 'mongodb' or 'couchdb'")
        return

    elif db == "mongodb":
        from mymongodb.operations import create_db
        from mymongodb.operations import delete_all_db
        from mymongodb.operations import create_bulk   # C
        from mymongodb.operations import retrieve_bulk # R
        from mymongodb.operations import update_bulk   # U
        from mymongodb.operations import delete_bulk   # D

        # config operations
        kw_create   = { 'tweets' : dataset[:test_size] }
        kw_retrieve = { 'filter' : { 'lang' : 'fr' } }
        kw_update   = { 'filter' : { 'lang' : 'en' },
                        'update' : {
                        '$set' : { 'lang' : 'eng' } } }
        kw_delete   = { 'filter' : { 'lang' : 'fr' } }

    elif db == "couchdb":
        from mycouchdb.operations import create_db
        from mycouchdb.operations import delete_all_db
        from mycouchdb.operations import create_bulk   # C
        from mycouchdb.operations import retrieve_bulk # R
        from mycouchdb.operations import update_bulk   # U
        from mycouchdb.operations import delete_bulk   # D

        # config operations
        kw_create   = { 'docs' : dataset[:test_size] }

        kw_retrieve = {
            'mapfun': "function(doc) {{ if (doc.retweet_count > 10) {{ emit(doc._id, doc); }} }}"
            }

        kw_update   = {
            'mapfun': "function(doc) {{ if (doc.retweet_count > 10) {{ emit(doc._id, doc); }} }}",
            'update' : { 'popularity' : 'high'}
            }

        kw_delete   = {
            'mapfun': "function(doc) {{ if (doc.retweet_count < 10) {{ emit(doc._id, doc); }} }}"
            }

    logs = { test_size : {} }
    delete_all_db()
    create_db()
    for f, f_name, kw in [
        (create_bulk, 'create', kw_create),
        (retrieve_bulk, 'retrieve', kw_retrieve),
        (update_bulk, 'update', kw_update),
        (delete_bulk, 'delete', kw_delete)
        ] :

        print("timing: {}".format(f_name))
        rt, r = timer(f, **kw)
        logs[test_size][f_name] = rt
        print(rt)
        #print(r)

    #pprint_dict(logs)
    return logs


def mongodb_tests(dataset,
    test_sizes=[1, 100, 1000, 10000, 90000]):

    from mongodb.operations import delete_all_db
    from mongodb.operations import create_bulk   # C
    from mongodb.operations import retrieve_bulk # R
    from mongodb.operations import update_bulk   # U
    from mongodb.operations import delete_bulk   # D

    logs = {}
    for n in test_sizes:

        kw_create   = { 'tweets' : dataset[:n] }
        kw_retrieve = { 'filter' : { 'lang' : 'fr' } }
        kw_update   = { 'filter' : { 'lang' : 'en' },
                        'update' : {
                        '$set' : { 'lang' : 'eng' } } }
        kw_delete   = { 'filter' : { 'lang' : 'fr' } }

        delete_all_db()
        
        for f, f_name, kw in [
            (create_bulk, 'create', kw_create),
            (retrieve_bulk, 'retrieve', kw_retrieve),
            (update_bulk, 'update', kw_update),
            (delete_bulk, 'delete', kw_delete)
        ] :
            rt = timer(f, **kw)

            if f_name not in logs.keys():
                logs[f_name] = {}
            logs[f_name][n] = rt

    return logs





if __name__ == "__main__":

    # input data
    dataset_dir = "/home/eolus/Desktop/DAUPHINE/DBA/dm_data"
    tweets = load_dataset(dataset_dir, n=2000)

    logs_foo =  crud_runtime(tweets, 2000, "couchdb")
    pprint_dict(logs_foo)


    # from mycouchdb.operations import create_db
    # from mycouchdb.operations import delete_all_db
    # delete_all_db()
    # create_db()

    # from mycouchdb.operations import create_bulk   # C
    # r = create_bulk(docs=tweets)

    # from mycouchdb.operations import retrieve_bulk
    # mapfun = "function(doc) {{ if (doc.retweet_count > 10) {{ emit(doc._id, doc); }} }}"
    # r = retrieve_bulk(mapfun=mapfun)
    # print(len(r))



