import sqlite
import OAuth
import tweepy
import secrets
import json
import requests
from secrets import *
from requests_oauthlib import OAuth1Session


ARTIST_CACHE = 'artists.json'
try:
    cache_file = open(ARTIST_CACHE, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl):
    return baseurl

def make_request_using_cache(url):
    unique_ident = params_unique_combination(url)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

LYRICS_CACHE = 'lyrics.json'
try:
    cache_file = open(LYRICS_CACHE, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl):
    return baseurl

def make_request_using_cache(url):
    unique_ident = params_unique_combination(url)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

consumer_key = secrets.twitter_api_key
consumer_secret = secrets.twitter_api_secret
access_token = secrets.twitter_access_token
access_secret = secrets.twitter_access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

TWITTER_CACHE = 'tweet_cache1.json'
try:
    cache_file = open(TWITTER_CACHE, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def params_unique_combination3(query, count):
    return query + count

def make_twitter_request_using_cache3(query, count):
    unique_ident = params_unique_combination3(query, count)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        resp = api.search(q=query, count=count)
        CACHE_DICTION[unique_ident] = resp
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]


def init_database():
    pass
def populate_database():
    pass
def access_spotify():
    pass
def access_twitter():
    pass
def access_artists():
    pass
def access_artist():
    pass
def get_lyrics():
    pass
def sentiment():
    pass
def bar_chart():
    pass
def pie_chart():
    pass
def scatter_plot():
    pass
def process_command():
    pass
