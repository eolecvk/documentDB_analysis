import sys
import time
import datetime

#from os.path import join
#import simplejson as json

from functools import partial

from urllib.error import URLError
from http.client import BadStatusLine
from twython import Twython, TwythonError
import conn

#===============================

def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):
    """
    A nested helper function that handles common HTTPErrors.
    Return an updated value for wait_period if the problem is a 500 level error.
    Block until the rate limit is reset if it's a rate limiting issue (429 error).
    Returns None for 401 and 404 errors, which requires special handling by the caller.
    Keyword args:
    `max_errors` : maximum number of retries on error before exiting the function
    `*args`, `**kw` : args for twitter_api_func()
    """
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):

        if wait_period > 3600: # Seconds
            print ('Too many retries. Quitting.')
            raise e

        # See https://dev.twitter.com/docs/error-codes-responses for common codes
        if e.error_code == 401:
            print ('Encountered 401 Error (Not Authorized)')
            return None

        elif e.error_code == 404:
            print ('Encountered 404 Error (Not Found)')
            return None
        
        elif e.error_code == 429:
            print ('Encountered 429 Error (Rate Limit Exceeded)')
            if sleep_when_rate_limited:
                print ("Retrying in 15 minutes...ZzZ...")
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print ('...ZzZ...Awake now and trying again.')
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        
        elif e.error_code in (500, 502, 503, 504):
            print ('Encountered %iError. Retrying in %iseconds' %\
            (e.error_code, wait_period))
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        
        else:
            raise e
        # End of nested helper function

    wait_period = 2
    error_count = 0
    while True:
        try:
            return twitter_api_func(*args, **kw)

        except TwythonError as e:
            error_count = 0
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return

        except URLError as e:
            error_count += 1
            print ("URLError encountered. Continuing.")
            if error_count > max_errors:
                print ("Too many consecutive errors...bailing out.")
                raise

        except BadStatusLine as e:
            error_count += 1
            print ("BadStatusLine encountered. Continuing.")
            if error_count > max_errors:
                print ("Too many consecutive errors...bailing out.")
                raise


#===============================

def search(q=None,
    since_id=None, max_id=None, tweet_limit=sys.maxsize):
    """
    For a given query q, get recent tweets (up to 7 days old)
    Keyword args:
    `q`: keyword query
    `since_id`: id of the most ancient tweets to fetch up to.
    `max_id`: id of the most recent tweet to start fetching from (get timeline goes backward in time when fetching tweets)
    `tweet_limit`: Max number of tweets to return
    ---
    https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
    for details on API parameters
    """

    tweets = []

    twitter_api = conn.get_twitter_api()
    search_tweets = partial(
        make_twitter_request,
        twitter_api.search)

    cursor = max_id
    while cursor != 0:
        response = search_tweets(q=q,
            since_id=since_id, max_id=cursor, count=100)
        if response is None or response==[]:
            print("break_1")
            break
        else:
            try:
                cursor = min([t['id'] for t in response['statuses']])
            except:
                print(list(response.keys()))
            new_tweets = [t for t in response['statuses'] if t not in tweets]
            if new_tweets:
                tweets.extend(new_tweets)
                print("max_id = {cursor}".format(cursor=cursor))
            else:
                print("break_2")
                break
    return tweets


#===============================


if __name__ == "__main__":

    import conn
    twitter_api = conn.get_twitter_api()

    try:
        tweets = search(q='database')
    except TwythonError as e:
        print(e)

    #for tweet in tweets:
    #    print(tweet['text'])

    print(len(tweets))
