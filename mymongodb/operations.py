"""
Wrappers for common operations (CRUD) on mongoDB
"""
import pymongo
from mymongodb.conn import get_client
from mymongodb.conn import get_db
from mymongodb.conn import get_collection


# Basic Utils
def preprocess_tweets(tweets):
    """
    Creates a '_id' key in each tweet dict
    where tweet['_id'] = tweet['id'] 
    """
    def add_index(tweet):
        tweet_id = tweet['id']
        preprocessed_tweet = tweet
        preprocessed_tweet['_id'] = tweet_id
        return preprocessed_tweet

    preprocessed_tweets = [add_index(tw) for tw in tweets]
    return preprocessed_tweets


def delete_all_db():
    
    client = get_client()
    for db_name in client.database_names():
        client.drop_database(db_name)
        print("DROPPED DB: {}".format(db_name))

def create_db():
    r = get_db()
    return r


# CRUD
# --create
def create(tweet):
    collection = get_collection()
    mongodb.insert_one(preprocessed_tweet)

def create_bulk(tweets):
    collection = get_collection()
    collection.insert_many(tweets, ordered=False)


# --retrieve
def retrieve_bulk(**kwargs):
    collection = get_collection()
    records = [r for r in collection.find(**kwargs)]
    print("nb matches:", len(records))
    return records


# --update
def update(**kwargs):
    collection = get_collection()
    collection.update_one(**kwargs)

def update_bulk(**kwargs):
    collection = get_collection()
    collection.update_many(**kwargs)


# --delete
def delete(**kwargs):
    collection = get_collection()
    collection.delete_one(**kwargs)

def delete_bulk(**kwargs):
    collection = get_collection()
    collection.delete_many(**kwargs)

if __name__ == "__main__":
    print("hello")
