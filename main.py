"""
test runtime for CRUD operations
"""


from utils import load_dataset
from utils import timer
from utils import pprint_dict



def crud_runtime(dataset, db):
    
    logs = {}


    if db == "mongodb":
        from mymongodb.operations import delete_all_db
        from mymongodb.operations import create_db
        from mymongodb.operations import create_bulk   # C
        from mymongodb.operations import retrieve_bulk # R
        from mymongodb.operations import update_bulk   # U
        from mymongodb.operations import delete_bulk   # D

        delete_all_db()
        create_db()

        kw_create     = {'tweets' : dataset }
        kw_retrieve   = {'filter' : {'retweet_count' : {'$gt' : 10}}}
        kw_update     = {'filter' : {'retweet_count' : {'$gt' : 10}},
                         'update' : {'$set' : { 'popularity' : 'high'}}}
        kw_delete     = {'filter' : {'retweet_count' : {'$lt' : 10}}}

        for f, f_name, kw in [
            (create_bulk, 'create', kw_create),
            (retrieve_bulk, 'retrieve', kw_retrieve),
            (update_bulk, 'update', kw_update),
            (delete_bulk, 'delete', kw_delete) ]:
            rt, r = timer(f, **kw)
            logs[f_name] = rt



    elif db == "couchdb":
        from mycouchdb.operations import delete_all_db
        from mycouchdb.operations import create_db
        from mycouchdb.operations import create_bulk   # C
        from mycouchdb.operations import create_view   # R (overhead)        
        from mycouchdb.operations import query         # R
        from mycouchdb.operations import update_bulk   # U
        from mycouchdb.operations import delete_bulk   # D

        try:
            delete_all_db()
            create_db()
        except Exception as e:
            print(e)

        # config operations
        kw_create   = { 'docs' : dataset }
        view_json = {
            "_id":"_design/tweets",
            "language": "javascript",
            "views":
            {
                'popular': {
                    "map" : "function(doc) {{ if (doc.retweet_count >= 10) emit(null, doc) }}"
                },
                'not_popular': {
                    "map" : "function(doc) {{ if (doc.retweet_count < 10) emit(null, doc) }}"
                }
            }
        }
        kw_create_view = { 'view_json' : view_json}
        kw_retrieve = {'view_name' : 'popular'}
        kw_update = {'view_name' : 'popular',
                     'update' : {'popularity' : 'high'}}
        kw_delete = {'view_name' : 'not_popular'}


        for f, f_name, kw in [
            (create_bulk, 'create', kw_create),
            (create_view, 'create_view', kw_create_view),
            (query, 'query', kw_retrieve),
            (update_bulk, 'update', kw_update),
            (delete_bulk, 'delete', kw_delete) ]:

            rt, r = timer(f, **kw)
            logs[f_name] = rt
            print(f_name, rt)

    return logs



def generate_logs(dataset, sample_sizes, trials=10):

    logs_all = { "mongodb" : {}, "couchdb": {} }

    
    for db in ["mongodb", "couchdb"]:
        for size in sample_sizes:
            for i in range(trials):

                print("\n\t TEST | {} | n={} | #{}/{}".format(
                    db, size, i+1, trials))


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
    dataset_dir = "/home/eolus/Desktop/DAUPHINE/DBA/dm_data"
    tweets = load_dataset(dataset_dir)
    
    #Get logs
    logs = generate_logs(dataset=tweets, sample_sizes=[2000], trials=5)
    pprint_dict(logs)




    #print(update_design(view_json))

    #print(pprint_dict(retrieve_all_designs()))



    # kw_retrieve = {
    #     'mapfun': "function(doc) {{ if (doc.retweet_count > 10) {{ emit(doc._id, doc); }} }}"
    #     }

    # kw_update   = {
    #     'mapfun': "function(doc) {{ if (doc.retweet_count > 10) {{ emit(doc._id, doc); }} }}",
    #     'update' : { 'popularity' : 'high'}
    #     }

    # kw_delete   = {
    #     'mapfun': "function(doc) {{ if (doc.retweet_count < 10) {{ emit(doc._id, doc); }} }}"
    #     }