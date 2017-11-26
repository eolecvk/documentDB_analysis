
import couchdb

from couchdb.conn import get_server
from couchdb.conn import get_db


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



def create(tweet):
	db = get_db()
	db[tweet_id] = tweet


def retrieve(tweet_id):
	db = get_db()
	tweet = db[tweet_id]
	return tweet