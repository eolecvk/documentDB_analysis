
# Sourcing

## Source: Twitter (via REST API)

We will be using the Twitter REST API for fetching the tweets that are relevant to our use cases.

The endpoints:

+ `GET search/tweets` is used for fetching tweets based on keywords
+ `GET statuses / home_timeline` is used for sourcing tweets for a given user of interest.


## [Twython](https://pypi.python.org/pypi/twython/), A Pure Python Twitter API wrapper

We will be using the Python Twitter API wrapper `Twython` [[git]](www.github.com/ryanmcgrath/twython) for fetching the tweets that are relevant to our use cases.

Twython has a MIT License and is free to use.

The installation and usage is described in the [official source](https://github.com/ryanmcgrath/twython).

## Scripts

Our own data scripts using are available in a separate library that we developed [[source code]](https://github.com/eolecvk/twitter_toolkit/).

We use a basic search functions:

The script accomplishes the following sequence:
1. Retrieve authentication tokens
2. Request data with Twitter API

**Authentication**

```
from twython import Twython
twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
```

**/GET Search Request**

```
tweets = twitter.search(q='dauphine university')
```

We later proceed to saving the fetched data in database system.



