"""
Wrappers for common operations (CRUD) on mongoDB
"""
import pymongo
from mongodb.conn import get_db
from mongodb.conn import get_collection

# INITIALIZATION
def ini_collection(collection_name):
    return collection



# CRUD
# --create
def add_index(tweet):
    tweet_id = tweet['id']
    preprocessed_tweet = tweet
    preprocessed_tweet['_id'] = tweet_id
    return preprocessed_tweet

def create(tweet):
    preprocessed_tweet = add_index(tweet)
    mongodb = get_db()
    mongodb.insert_one(preprocessed_tweet)

def create_batch(tweets, collection):
    collection.insert_many(tweets, ordered=False)

# --retrieve
def retrieve(**kwargs):
    mongodb = get_db()
    return mongodb.find_one(**kwargs)

def retrieve_batch(**kwargs):
    mongodb = get_db()
    return mongodb.find_many(**kwargs)


# --update
def update():
    pass

def update_batch():
    pass


# --delete
def delete():
    pass

def delete_batch():
    pass

if __name__ == "__main__":
    print("hello")
