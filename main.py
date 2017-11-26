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
        from mongodb.operations import delete_all_db
        from mongodb.operations import create_bulk   # C
        from mongodb.operations import retrieve_bulk # R
        from mongodb.operations import update_bulk   # U
        from mongodb.operations import delete_bulk   # D

        kw_create   = { 'tweets' : dataset[:test_size] }
        kw_retrieve = { 'filter' : { 'lang' : 'fr' } }
        kw_update   = { 'filter' : { 'lang' : 'en' },
                        'update' : {
                        '$set' : { 'lang' : 'eng' } } }
        kw_delete   = { 'filter' : { 'lang' : 'fr' } }

    elif db == "couchdb":
        from couchdb.operations import delete_all_db
        from couchdb.operations import create_bulk   # C
        from couchdb.operations import retrieve_bulk # R
        from couchdb.operations import update_bulk   # U
        from couchdb.operations import delete_bulk   # D

        kw_create   = { 'docs' : dataset[:test_size] }
        kw_retrieve = { 'mapfun': """function(doc) {
                                if (doc.lang == "fr") {
                                    emit(doc._id, doc);
                                    }
                                }""" }
        #USE MAPFUN STR
        # cf https://stackoverflow.com/questions/10404178/how-can-i-delete-multiple-documents-in-couchdb#10404256
        # cf https://wiki.apache.org/couchdb/Introduction_to_CouchDB_views

        kw_update   = { 'filter' : { 'lang' : 'en' },
                        'update' : {
                        '$set' : { 'lang' : 'eng' } } }
        kw_delete   = { 'filter' : { 'lang' : 'fr' } }

    logs = { test_size : {} }
    delete_all_db()
    for f, f_name, kw in [
        (create_bulk, 'create', kw_create),
        (retrieve_bulk, 'retrieve', kw_retrieve),
        (update_bulk, 'update', kw_update),
        (delete_bulk, 'delete', kw_delete)
        ] :
        rt = timer(f, **kw)
        logs[test_size][f_name] = rt

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
    tweets = load_dataset(dataset_dir)

    logs_foo =  crud_runtime(tweets, 1000, "couchdb")
    pprint_dict(logs_foo)
    


    # # log
    # logs = {
    #     'mongodb' : {
    #         'create'  : {},
    #         'retrieve': {},
    #         'update'  : {},
    #         'delete'  : {}
    #         },
    #     'couchdb' : {
    #         'create'  : {},
    #         'retrieve': {},
    #         'update'  : {},
    #         'delete'  : {}
    #         }
    #     }
