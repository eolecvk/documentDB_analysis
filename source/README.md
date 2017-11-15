
# Sourcing

## Source: Twitter (via REST API)

We will be using the Twitter REST API for fetching the tweets that are relevant to our use cases.

The endpoints:

+ `GET search/tweets` is used for fetching tweets based on keywords
+ `GET statuses / home_timeline` is used for sourcing tweets for a given user of interest.

## Requirements

Using the Twitter REST API requires one accomplish the following steps:

**1. to sign-up as a Twitter user (or use an existing account)**

**2. to [register a new app](https://apps.twitter.com/) on the developer**

![](https://github.com/eolecvk/documentDB_analysis/blob/master/source/img/1_app_registration.png)

**3. to generate a consumer/secret key pair for the app**

![](https://github.com/eolecvk/documentDB_analysis/blob/master/source/img/2_app_keys.png)

## [Twython](https://pypi.python.org/pypi/twython/), A Pure Python Twitter API wrapper

We will be using the Python Twitter API wrapper `Twython` [[git]](www.github.com/ryanmcgrath/twython) to simplify querying the API.  
Twython has a MIT License and is free to use.  
The installation and usage is described in the [official source](https://github.com/ryanmcgrath/twython).

## Our custom [`twitter_toolkit`](https://github.com/eolecvk/twitter_toolkit/)

We packaged the Python code for sourcing Twitter data as standalone library available on GitHub [[git]](https://github.com/eolecvk/twitter_toolkit/).

We use the library to accomplish the following sequence:
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
tweets = twitter.search(q='nosql')
```

We later proceed to saving the fetched data in our database system.



