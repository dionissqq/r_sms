from consts import BEARER_TOKEN
import requests
import json

def create_headers():
    headers = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}
    return headers

def get_tweets_by_hashtag(hashtag, number):
    query = "{} lang:en -is:retweet".format(hashtag)
    tweet_fields = "tweet.fields=text"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results={}".format(
        query, tweet_fields, number
    )
    headers = create_headers()
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
    
def get_tweets_by_user(username):
    query = "lang:en from:{} -is:retweet".format(username)
    tweet_fields = "tweet.fields=text"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields
    )
    headers = create_headers()
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()