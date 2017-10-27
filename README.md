# Advanced Database Project

**Date:** Oct 2017  
**Authors**: Emerick LECOMTE, Eole CERVENKA, 

**Abstract:**  
_In the context of building a topic discovery application using Twitter data (tweets), we are interested in comparing two candidate NoSQL document databases, MongoDB and CouchDB._


**Objectives**:  

+ We will first define the  application, the data, the sourcing process and the database functionalities needed for our use case.
+ We will then provide a qualitative review of the two candidate open-source databases MongoDB and CouchDB.
+ We will finally perform a quantitative performance comparison of the two databases.  
+ Given our operational needs, the qualitative and the quantitative comparisons will support our final decision to select the database that best fits our use case.


## Plan

**1. Execution**

+ Application presentation
+ Data (content, format)
+ Sourcing (source, frequency, volume)
+ Storage (MongoDB, CouchDB)

**2. Qualitative Analysis**

+ Coherence model
+ Concurrency
+ Data types
+ Fault tolerance
+ Availability
+ Scalability
+ Interface
+ Database setup
+ Integration with external systems

**3. Quantitative analysis**

+ Runtime performance comparison for query, update, delete, insert operations
+ Scalability performance comparison

**4. Conclusion**

+ Summary
+ Opinions

**5. Annexes**

+ Scripts
+ README


# Execution

+ Presentation of the application
+ Data (content, format)
+ Sourcing (source, frequency, volume)
+ Storage (MongoDB, CouchDB)

## Application overview

The application we are building is a topic discovery platform using Twitter data.

Marketing departments are typically interested in getting insights about what people discuss on social media. Such insights can be delivered in a SaaS platform that the analysts of client businesses can use to explore topics our application has discovered for a specific tweet dataset.

Tweets datasets are collections of tweets.
We can imagine multiple ways to make a topic extraction feature relevant to businesses.  
For example, we may want to study datasets of tweets for a given group of users (ie a specific demographic). Alternatively, we could be interested in building a dataset of tweets that contain a specific keyword to discover which topics that are often mentionned in the same tweets as the specified keyword.

To create these tweet datasets, we need the ability to store and query tweets based on their various attributes (cf next section about data).

Social media data is constantly generated and we want our application to reflect conversation trends as current as possible. However, we can still afford to load new tweets in batches on a use case basis. For example, if Coca-Cola wants to know the topics associated with its brands in tweets, we will load Coca-Cola related tweets just one time.

Finally, because we envision the application to be a SaaS platform, we need a database that supports concurrent access to the database.


## Data overview

### Content

Our application primarily uses [tweet objects](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object).

According to Twitter documentation, _"Tweets are the basic atomic building block of all things Twitter. Tweets are also known as “status updates.” The Tweet object has a long list of ‘root-level’ attributes, including fundamental attributes such as `id`, `created_at`, and `text`. Tweet objects are also the ‘parent’ object to several child objects. Tweet child objects include `user`, `entities`, and `extended_entities`. Tweets that are geo-tagged will have a `place` child object."_


### Format

Tweets are natively [JSON](http://json.org/) formatted. Below is preview of the top level atributes for the tweet object.

```
{
 "created_at":"Thu Apr 06 15:24:15 +0000 2017",
 "id": 850006245121695744,
 "id_str": "850006245121695744",
 "text": "1/ Today we’re sharing our vision for the future of the Twitter API platform!nhttps://t.co/XweGngmxlP",
 "user": {},  
 "entities": {}
}
```

The full data dictionary for tweet objects is available in the [official documentation for tweets](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object); please refer to this for more information.

## Sourcing overview

### Source

We will be using the Twitter REST API for fetching the tweets that are relevant to our use cases.

The endpoints: 

+ [`GET search/tweets`](https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html) is used for fetching tweets based on keywords
+ [`GET statuses / home_timeline`](https://developer.twitter.com/en/docs/tweets/timelines/overview) is used for sourcing tweets for a given user of interest.

Please find the data sourcing scripts in the annexe.	

### Frequency

We update the tweet database on a per use case basis. This means that everytime a client as a specific request we need to fetch the tweets related to the request using the appropriate API endpoint and then load the tweets in the document database.

### Volume

We typically expect to be working on datasets in the order of up to 1 to 10 millions tweets per use case.

For example; if a client is interested to discover topics across a sample set of 50,000 we would be retrieving the 50 most recent tweets for each user thus getting us ~2,5 millions tweets.

The size of a JSON tweet object is typically in the order of 2.5KB; therefore for each new use case a client brings, we would have to store an additional 2.5 to 25 GB in our database.


## Candidate databases: MongoDB and CouchDB

To be continued...

# Qualitative Analysis

The qualitative analysis studies the following aspects for each system:

+ Coherence model
+ Concurrency
+ Data types
+ Fault tolerance
+ Availability
+ Scalability
+ Interface
+ Database setup
+ Integration with external systems

## Coherence model
### MongoDB
### CouchDB
## Concurrency
### MongoDB
### CouchDB
## Data types
### MongoDB
### CouchDB
## Fault tolerance
### MongoDB
### CouchDB
## Availability
### MongoDB
### CouchDB
## Scalability
### MongoDB
### CouchDB
## Interface
### MongoDB
### CouchDB
## Database setup
### MongoDB
### CouchDB
## Integration with external systems
### MongoDB
### CouchDB
## Conclusion: quantitative comparison

# Quantitative analysis

The quantitative analysis studies the following aspects for each system:

+ Runtime performance analysis
+ Scalability performance analysis

## Runtime performance comparison

### Query
#### MongoDB
#### CouchDB
### Update
#### MongoDB
#### CouchDB
### Insert
#### MongoDB
#### CouchDB
### Delete
#### MongoDB
#### CouchDB

### Conclusion: runtime performance comparison 


## Scalability performance comparison
### MongoDB scalability performance analysis
### CouchDB scalability performance analysis
### Conclusion: Scalability performance comparison 
