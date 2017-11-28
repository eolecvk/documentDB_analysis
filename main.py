"""
test runtime for CRUD operations
"""


from utils import load_dataset
from utils import timer
from utils import pprint_dict



def crud_runtime(dataset, db):

    if db == "mongodb":
        from mymongodb.operations import create_db
        from mymongodb.operations import delete_all_db
        from mymongodb.operations import create_bulk   # C
        from mymongodb.operations import retrieve_bulk # R
        from mymongodb.operations import update_bulk   # U
        from mymongodb.operations import delete_bulk   # D

        # config operations
        kw_create     = { 'tweets' : dataset }

        kw_retrieve   = { 'filter' : {
                            'retweet_count' : { '$gt' : 10 }
                        }
                    }

        kw_update     = { 'filter' : {
                            'retweet_count' : { '$gt' : 10 } 
                            },
                        'update' : {
                            '$set' : { 'popularity' : 'high' }
                        }
                    }

        kw_delete     = { 'filter' : {
                            'retweet_count' : { '$lt' : 10 }
                            }
                        }


    if db == "couchdb":
        from mycouchdb.operations import create_db
        from mycouchdb.operations import delete_all_db
        from mycouchdb.operations import create_bulk   # C
        from mycouchdb.operations import retrieve_bulk # R
        from mycouchdb.operations import update_bulk   # U
        from mycouchdb.operations import delete_bulk   # D

        # config operations
        kw_create   = { 'docs' : dataset }

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

    logs = {}
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
        logs[f_name] = rt
        print(rt)

    return logs



def generate_logs(dataset, sample_sizes, trials=10):

    logs_all = { "mongodb" : {}, "couchdb": {} }

    
    for db in ["mongodb", "couchdb"]:
        for size in sample_sizes:
            for i in range(trials):

                print("\n\t TEST | {} | n={} | #{}/10".format(
                    db, size, i+1))


                import copy
                sample = copy.deepcopy(dataset[:size])

                logs =  crud_runtime(dataset=sample, db=db)

                for k, v in logs.items():

                    if k not in logs_all[db].keys():
                        logs_all[db][k] = {size : [v]}
                    elif size not in logs_all[db][k].keys():
                        logs_all[db][k][size] = [v]
                    else:
                        logs_all[db][k][size].append(v)

    # avg
    for db in ["mongodb", "couchdb"]:
        for k in logs_all[db].keys():
            for size, rt_list in logs_all[db][k].items():
                avg = sum(rt_list) / float(len(rt_list)) 
                logs_all[db][k][size] = avg

    return logs_all



if __name__ == "__main__":

    # input data
    #dataset_dir = "/home/eolus/Desktop/DAUPHINE/DBA/dm_data"
    #tweets = load_dataset(dataset_dir)
    
    #Get logs
    #logs = generate_logs(dataset=tweets, sample_sizes=[2000], trials=5)
    #pprint_dict(logs)



    ### Confirm : create_view(),...

    view_json = {
        "_id":"_design/tweets",
        "_rev": "101",
        "language": "javascript",
        "views": {
            'popular': {
                "map" : "function(doc) {{ if (doc.retweet_count > 10) emit(null, doc) }}"
            }
        }
    }

    from mycouchdb.operations import create_view
    r = create_view(view_json, view_name="popular")
    print(r)


    from mycouchdb.operations import retrieve_bulk_v2
    from mycouchdb.conn import get_address_db
    print(get_address_db())
    r = retrieve_bulk_v2(view_name="popular")
    print(r)