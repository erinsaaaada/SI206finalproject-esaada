import sqlite3
import tweepy
import spotipy
import secrets
import json
import requests
import sys
import spotipy
import lyricwikia
import plotly
from spotipy.oauth2 import SpotifyClientCredentials
from secrets import *
from requests_oauthlib import OAuth1Session
from aylienapiclient import textapi


spotify_key = secrets.sp_client_key
spotify_secret = secrets.sp_client_secret
cc = SpotifyClientCredentials(spotify_key, spotify_secret)
spotify = spotipy.client.Spotify(client_credentials_manager = cc)

ARTIST_CACHE = 'artists.json'

def make_request_using_cache(q):
    try:
        cache_file = open(ARTIST_CACHE, 'r')
        cache_contents = cache_file.read()
        #print(cache_contents)
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}
    if q in CACHE_DICTION.keys():
        print("Getting cached data...")
        return CACHE_DICTION[q]
    else:
        print("Making a request for new data...")
        resp = spotify.search(q, limit=50, offset=0, type='track', market=None)
        CACHE_DICTION[q] = resp
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(ARTIST_CACHE,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[q]

LYRICS_CACHE = 'lyrics.json'

def params_unique_combination1(artist, song):
    return artist + ' ' + song
def make_request_using_cache1(artist, song):
    try:
        cache_file = open(LYRICS_CACHE, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}
    unique_ident = params_unique_combination1(artist, song)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        try:
            lyrics = lyricwikia.get_lyrics(artist, song)
            CACHE_DICTION[unique_ident] = lyrics
        except:
            CACHE_DICTION[unique_ident] = 'No lyrics'
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(LYRICS_CACHE,"w")
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
def params_unique_combination2(query, count):
    return query

def make_twitter_request_using_cache(query, count):
    try:
        cache_file = open(TWITTER_CACHE, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}
    unique_ident = params_unique_combination2(query, count)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        resp = api.search(q=query, count=count)
        CACHE_DICTION[unique_ident] = resp
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(TWITTER_CACHE,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

s_id = secrets.aylien_id
s_key = secrets.aylien_key
client = textapi.Client(s_id, s_key)

SENTIMENT_CACHE = 'sentiment_cache.json'
POLARITY_CACHE = 'polarity_cache.json'

def params_unique_combination3(tweet):
    return tweet
def make_request_using_cache3(tweet, text):
    try:
        cache_file = open(SENTIMENT_CACHE, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}
    unique_ident = params_unique_combination3(tweet)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        resp = client.Sentiment(text)
        CACHE_DICTION[unique_ident] = resp
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(SENTIMENT_CACHE,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

def params_unique_combination4(song, artist):
    return song + ' ' + artist
def make_request_using_cache4(song, artist, text):
    try:
        cache_file = open(POLARITY_CACHE, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}
    unique_ident = params_unique_combination4(song, artist)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        resp = client.Sentiment(text)
        CACHE_DICTION[unique_ident] = resp
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(POLARITY_CACHE,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]


class Song:
    def __init__(self, artist, song, is_single=True, album_name = "Single"):
        self.song = song
        self.artist = artist
        self.name = self.song['name']
        self.release_date = self.song['album']['release_date']
        self.is_single = is_single
        if self.is_single:
            self.album_name = album_name
        else:
            self.album_name = self.song['album']['name']
        self.popularity = self.song['popularity']
        self.length = round(song['duration_ms']*.001, 3)
    def __str__(self):
        return '''Artist: {}
Song: {} ({} seconds) Release Date: {}
Album Name: {} Popularity: {}
-------------------------------'''.format(self.artist, self.name, self.length, self.release_date, self.album_name, self.popularity)

class Tweet:
    def __init__(self, tweet_dict_from_json=None):
        self.tweet_dict = tweet_dict_from_json
        self.text = self.tweet_dict["text"]
        self.screen_name = self.tweet_dict["user"]["screen_name"]
        self.createddate = self.tweet_dict["created_at"]
        self.retweet_count = self.tweet_dict["retweet_count"]
        self.favorite_count = self.tweet_dict["favorite_count"]
        self.id = self.tweet_dict["id"]
        self.popularity_score = self.retweet_count * 2 + self.favorite_count *3
    def __str__(self):
        return '''User: {}
Tweet: {}
Created Date: {}
Retweets: {} | Favorites: {}
Popularity Score: {}'''.format(self.screen_name, self.text, self.createddate, self.retweet_count, self.favorite_count, self.popularity_score)

def artist_request(q):
    r = make_request_using_cache(q)
    songs = []
    for t in r['tracks']['items']:
        for item in t['artists']:
            if item['name'] == q:
                songs += [t]
    return songs

def spotify_request(q):
    if ',' in q:
        for artist in q.split(' , '):
            r = make_request_using_cache(artist)
            artist_id_dict = {}
            for t in r['tracks']['items']:
                l = t['album']['artists']
                for x in l:
                    artist_id_dict[x['name']] = x['id']
            r = spotify.artist_albums(artist_id_dict[artist], album_type=None, country=None, limit=20, offset=0)
            top = spotify.artist_top_tracks(artist_id_dict[artist], country = 'US')
            top_dict = {}
            for t in top['tracks']:
                top_dict[t['name']] = t['popularity']
            print(top_dict)
            album_dict = {}
            for a in r['items']:
                album_dict[a['name']] = a['id']
            track_dict = {}
            for album_name, album_id in album_dict.items():
                count = 0
                tr = spotify.album_tracks(album_id, limit=50, offset=0)
                song_list = []
                for song in tr['items']:
                    if song['name'] in top_dict.keys():
                        song_list += [(song['name'], top_dict[song['name']])]
                track_dict[album_name] = song_list
                sort_songs = sorted(song_list, key = lambda x: x[1])
                song_names = [song[0] for song in sort_songs]


    else:
        r = make_request_using_cache(q)
        #print(r)
        artist_id_dict = {}
        for t in r['tracks']['items']:
            l = t['album']['artists']
            for x in l:
                artist_id_dict[x['name']] = x['id']
        r = spotify.artist_albums(artist_id_dict[q], album_type=None, country=None, limit=20, offset=0)
        top = spotify.artist_top_tracks(artist_id_dict[q], country = 'US')
        top_dict = {}
        for t in top['tracks']:
            top_dict[t['name']] = t['popularity']
        album_dict = {}
        for a in r['items']:
            album_dict[a['name']] = a['id']
        track_dict = {}
        for album_name, album_id in album_dict.items():
            tr = spotify.album_tracks(album_id, limit=50, offset=0)
            song_list = []
            for song in tr['items']:
                song_list += [song['name']]
            track_dict[album_name] = song_list

def twitter_request(artist):
    query = artist
    count = '70'
    r = make_twitter_request_using_cache(query, count)
    results = r["statuses"]
    tweets_list = []
    for d in results:
        if "RT" not in d["text"]:
            tweets_list += [d]
    inst_list = [Tweet(t) for t in tweets_list]
    sorted_inst_list = sorted(inst_list, key = lambda x: x.popularity_score, reverse = True)
    return sorted_inst_list

def get_lyrics(artist):
    for s in artist_request(artist):
        if s['album']['album_type'] == 'single':
            inst_list += [Song(artist, s)]
        else:
            inst_list += [Song(artist, s, False)]
    for s in inst_list:
        make_request_using_cache1(s.artist, s.name)

def tweet_sentiment(tweet_obj):
    resp = make_request_using_cache3(tweet_obj.text, {'text':tweet_obj.text})
    return resp

def lyric_sentiment(artist, song):
    resp = make_request_using_cache1(artist, song)
    if resp == 'No lyrics':
        return 'N/a'
    else:
        lyrics = resp
        sent = make_request_using_cache4(artist, song, lyrics)
        return sent

def init_song_table(artist):
    try:
        conn = sqlite3.connect('{}.db'.format(artist))
        cur = conn.cursor()
    except:
        print("Connection error.")
    try:
        table = "Songs"
        _SQL = """SELECT *
        FROM 'Songs'"""
        cur.execute(_SQL)
        results = cur.fetchall()
        user_input = input("Table exists. Delete? yes/no")
        if user_input.lower() == 'yes':
            statement ="""
                DROP TABLE IF EXISTS 'Songs';"""
            cur.execute(statement)
            statement1 = """CREATE TABLE 'Songs' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Artist' TEXT,
            'Name' TEXT,
            'Release_Date' TEXT,
            'Album_name' TEXT,
            'Popularity' INTEGER,
            'Polarity' TEXT,
            'Sentiment' TEXT,
            'Length' INTEGER
            );"""
            cur.execute(statement1)
        else:
            None
    except:
        statement1 = """CREATE TABLE 'Songs' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Artist' TEXT,
        'Name' TEXT,
        'Release_Date' TEXT,
        'Album_name' TEXT,
        'Popularity' INTEGER,
        'Polarity' TEXT,
        'Sentiment' TEXT,
        'Length' INTEGER
        );"""
        cur.execute(statement1)
    conn.commit()
    conn.close()

def init_tweet_table(artist):
    try:
        conn = sqlite3.connect('{}.db'.format(artist))
        cur = conn.cursor()
    except:
        print("Connection error.")
    try:
        table = "Tweets"
        _SQL = """SELECT *
        FROM 'Tweets'"""
        cur.execute(_SQL)
        results = cur.fetchall()
        user_input = input("Table exists. Delete? yes/no")
        if user_input.lower() == 'yes':
            statement ="""
                DROP TABLE IF EXISTS 'Tweets';"""
            cur.execute(statement)
            statement1 = """CREATE TABLE 'Tweets' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Tweet Date' TEXT,
            'Username' TEXT,
            'Tweet Text' TEXT,
            'Favorite Count' INTEGER,
            'Retweets' INTEGER,
            'Popularity' INTEGER,
            'Polarity' TEXT,
            'Subjectivity' TEXT
            );"""
            cur.execute(statement1)
        else:
            None
    except:
        statement1 = """CREATE TABLE "Tweets" (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Tweet Date' TEXT,
        'Username' TEXT,
        'Tweet Text' TEXT,
        'Favorite Count' INTEGER,
        'Retweets', INTEGER,
        'Popularity' INTEGER,
        'Polarity' TEXT,
        'Subjectivity' TEXT
        );"""
        cur.execute(statement1)
    conn.commit()
    conn.close()

def populate_song_table(artist):
    conn = sqlite3.connect('{}.db'.format(artist))
    cur = conn.cursor()
    inst_list = []
    for s in artist_request(artist):
        if s['album']['album_type'] == 'single':
            inst_list += [Song(artist, s)]
        else:
            inst_list += [Song(artist, s, False)]
    for song in inst_list:
        sentiment = lyric_sentiment(song.artist, song.name)
        if type(sentiment) == dict:
            subjectivity = sentiment['subjectivity']
            polarity = sentiment['polarity']
            insertion = [None, song.artist, song.name, song.release_date, song.album_name, song.popularity, subjectivity, polarity, song.length]
            statement = 'INSERT INTO "Songs" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
        else:
            subjectivity = None
            polarity = None
            insertion = [None, song.artist, song.name, song.release_date, song.album_name, song.popularity, subjectivity, polarity, song.length]
            statement = 'INSERT INTO "Songs" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
    conn.commit()

def populate_tweets_table(artist):
    conn = sqlite3.connect('{}.db'.format(artist))
    cur = conn.cursor()
    for tweet in twitter_request(artist):
        sentiment = tweet_sentiment(tweet)
        polarity = sentiment['polarity']
        subjectivity = sentiment['subjectivity']
        insertion = [None, tweet.createddate, tweet.screen_name, tweet.text, tweet.favorite_count, tweet.retweet_count, tweet.popularity_score, polarity, subjectivity]
        statement = 'INSERT INTO "Tweets" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()

def bar_chart():
    pass

def pie_chart():
    pass

def scatter_plot():
    pass

def process_command():
    pass

#if __name__=="__main__":
