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
        kw_delete     = {'filter' : {'retweet_count' : {'$gt' : 10}}}

        for f, f_name, kw in [
            (create_bulk, 'create', kw_create),
            (retrieve_bulk, 'retrieve', kw_retrieve),
            (update_bulk, 'update', kw_update),
            (delete_bulk, 'delete', kw_delete) ]:
            
            rt, r = timer(f, **kw)
            logs[f_name] = rt
            print(f_name, '\t', rt)



    elif db == "couchdb":
        from mycouchdb.operations import delete_all_db
        from mycouchdb.operations import create_db
        from mycouchdb.operations import create_bulk   # C
        from mycouchdb.operations import create_view   # R (overhead)        
        from mycouchdb.operations import query         # R
        from mycouchdb.operations import create_view_retrieve
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
                }
            }
        }
        kw_create_view = { 'view_json' : view_json}
        kw_retrieve = {'view_name' : 'popular'}
        kw_create_view_retrieve = {
            'view_json' : view_json,
            'view_name' : 'popular'
            }
        kw_update = {'view_name' : 'popular',
                     'update' : {'popularity' : 'high'}}
        kw_delete = {'view_name' : 'popular'}


        for f, f_name, kw in [
            (create_bulk, 'create', kw_create),
            (create_view_retrieve, 'create_view_retrieve', kw_create_view_retrieve),
            (query, 'query', kw_retrieve),
            (update_bulk, 'update', kw_update),
            (delete_bulk, 'delete', kw_delete) ]:

            rt, r = timer(f, **kw)
            logs[f_name] = rt
            print(f_name, '\t', rt)

    return logs



def generate_logs(dataset, sample_sizes, trials=4):

    logs_all = { "mongodb" : {}, "couchdb": {} }

    
    for db in ["couchdb"]:
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
    import sys
    assert len(sys.argv)==2,"""
Command not properly formatted; correct format:
```
python3 main.py {dataset_directory}
```
"""
    dataset_dir = argv[1]
    tweets = load_dataset(dataset_dir)
    
    #Get logs
    logs = generate_logs(dataset=tweets,
        sample_sizes=[10000, 20000, 50000, 70000, 90000],
        trials=4)
    pprint_dict(logs)
