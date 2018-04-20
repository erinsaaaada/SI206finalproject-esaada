import sqlite3
import tweepy
import spotipy
import secrets
import json
import requests
import lyricwikia
import plotly.plotly as py
import plotly.graph_objs as go
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
                    insertion = [None, song.artist, song.name, song.release_date, song.album_name, song.popularity, polarity, subjectivity, song.length]
                    statement = 'INSERT INTO "Songs" '
                    statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
                    cur.execute(statement, insertion)
                else:
                    subjectivity = None
                    polarity = None
                    insertion = [None, song.artist, song.name, song.release_date, song.album_name, song.popularity, polarity, subjectivity, song.length]
                    statement = 'INSERT INTO "Songs" '
                    statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
                    cur.execute(statement, insertion)
            conn.commit()
        else:
            return None
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
                insertion = [None, song.artist, song.name, song.release_date, song.album_name, song.popularity, polarity, subjectivity, song.length]
                statement = 'INSERT INTO "Songs" '
                statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)
            else:
                subjectivity = None
                polarity = None
                insertion = [None, song.artist, song.name, song.release_date, song.album_name, song.popularity, polarity, subjectivity, song.length]
                statement = 'INSERT INTO "Songs" '
                statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)
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
            for tweet in twitter_request(artist):
                sentiment = tweet_sentiment(tweet)
                polarity = sentiment['polarity']
                subjectivity = sentiment['subjectivity']
                insertion = [None, tweet.createddate, tweet.screen_name, tweet.text, tweet.favorite_count, tweet.retweet_count, tweet.popularity_score, polarity, subjectivity]
                statement = 'INSERT INTO "Tweets" '
                statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, )'
                cur.execute(statement, insertion)
            conn.commit()
        else:
            return None
    except:
        statement1 = """CREATE TABLE "Tweets" (
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
        for tweet in twitter_request(artist):
            sentiment = tweet_sentiment(tweet)
            polarity = sentiment['polarity']
            subjectivity = sentiment['subjectivity']
            insertion = [None, tweet.createddate, tweet.screen_name, tweet.text, tweet.favorite_count, tweet.retweet_count, tweet.popularity_score, polarity, subjectivity]
            statement = 'INSERT INTO "Tweets" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
        conn.commit()
    conn.close()

def bar_chart(artist, item):
    try:
        conn = sqlite3.connect('{}.db'.format(artist))
        cur = conn.cursor()
    except:
        print("Connection error.")
    if type(artist) == str:
        if item == 'tweets':
            statement = 'SELECT Subjectivity, SUM(Popularity) FROM Tweets GROUP BY Subjectivity '
            st = cur.execute(statement)
            x_values = ['objective', 'subjective']
            for item in st:
                if item[0] == 'objective':
                    objectivity = item[1]
                if item[0] == 'subjective':
                    subjectivity = item[1]
            y_values = [objectivity, subjectivity]
            data = [go.Bar(
                x=x_values,
                y=y_values
            )
        ]
            py.plot(data, filename='Tweet Subjectivity for {}'.format(artist))
        if item == 'songs':
            statement = 'SELECT Name, Popularity FROM Songs WHERE Popularity NOT NULL '
            st = cur.execute(statement)
            name_list = []
            popularity_list = []
            for r in st:
                if r[0] not in name_list:
                    name_list += [r[0]]
                    popularity_list += [r[1]]
            data = [go.Bar(
                x=name_list,
                y=popularity_list
            )
        ]
            py.plot(data, filename='Song Popularity for {}'.format(artist))
    if type(artist) == list:
        artist_dict = {}
        for a in artist:
            try:
                conn = sqlite3.connect('{}.db'.format(a))
                cur = conn.cursor()
            except:
                print("Connection error.")
            positive_count = 0
            negative_count = 0
            statement = '''SELECT Polarity, COUNT(Polarity) FROM Tweets
                            WHERE Polarity = "positive" OR Polarity = "negative"
                            GROUP BY Polarity '''
            st = cur.execute(statement)
            for row in st:
                if row[0] == 'positive':
                    positive_count += row[1]
                if row[0] == 'negative':
                    negative_count += row[1]
            statement1 = '''SELECT Polarity, COUNT(Polarity) FROM Songs
                            WHERE Polarity = "positive" OR Polarity = "negative"
                            GROUP BY Polarity '''
            st1 = cur.execute(statement1)
            for row in st1:
                if row[0] == 'positive':
                    positive_count += row[1]
                if row[0] == 'negative':
                    negative_count += row[1]
            artist_dict[a] = (positive_count, negative_count)
        positives = []
        negatives = []
        artist_list = []
        for v in artist_dict.items():
            artist_list += [v[0]]
            positives += [v[1][0]]
            negatives += [v[1][1]]
        trace0 = go.Bar(
        x=artist_list,
        y=positives,
        name='Positive',
        marker=dict(
            color='rgb(49,130,189)'
        )
        )
        trace1 = go.Bar(
        x=artist_list,
        y=negatives,
        name='Negative',
        marker=dict(
            color='rgb(204,204,204)',
        )
        )

        data = [trace0, trace1]
        layout = go.Layout(
        xaxis=dict(tickangle=-45),
        barmode='group',
        )

        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='angled-text-bar')

def pie_chart(artist, item, polarity):
    try:
        conn = sqlite3.connect('{}.db'.format(artist))
        cur = conn.cursor()
    except:
        print("Connection error.")
    if item == 'tweets':
        if polarity == 'polarity':
            statement = 'SELECT Polarity, COUNT(*) FROM Tweets GROUP BY Polarity '
            st = cur.execute(statement)
            label_list = []
            value_list = []
            for row in st:
                label_list += [row[0]]
                value_list += [row[1]]
            colors = ['#FEBFB3', '#E1396C']

            trace = go.Pie(labels=label_list, values=value_list,
                           hoverinfo='label+percent', textinfo='value',
                           textfont=dict(size=20),
                           marker=dict(colors=colors,
                                      line=dict(color='#000000', width=2)))

            py.plot([trace], filename='Tweet Polarity for {}'.format(artist))
        if polarity == 'subjectivity':
            statement = 'SELECT Subjectivity, COUNT(*) FROM Tweets WHERE Subjectivity NOT NULL GROUP BY Subjectivity '
            st = cur.execute(statement)
            label_list = []
            value_list = []
            for row in st:
                label_list += [row[0]]
                value_list += [row[1]]
            colors = ['#FEBFB3', '#E1396C']

            trace = go.Pie(labels=label_list, values=value_list,
                           hoverinfo='label+percent', textinfo='value',
                           textfont=dict(size=20),
                           marker=dict(colors=colors,
                                      line=dict(color='#000000', width=2)))

            py.plot([trace], filename='Tweet Subjectivity for {}'.format(artist))
    if item == 'songs':
        statement = 'SELECT Polarity, COUNT(*) FROM Songs WHERE Polarity = "positive" OR Polarity = "negative" GROUP BY Polarity '
        st = cur.execute(statement)
        label_list = []
        value_list = []
        for row in st:
            label_list += [row[0]]
            value_list += [row[1]]
        colors = ['#FEBFB3', '#E1396C']

        trace = go.Pie(labels=label_list, values=value_list,
                       hoverinfo='label+percent', textinfo='value',
                       textfont=dict(size=20),
                       marker=dict(colors=colors,
                                  line=dict(color='#000000', width=2)))

        py.plot([trace], filename='Song Polarity for {}'.format(artist))

def horizontal_bar(artist):
    try:
        conn = sqlite3.connect('{}.db'.format(artist))
        cur = conn.cursor()
    except:
        print("Connection error.")
    statement = 'SELECT Polarity, COUNT(Polarity) FROM Tweets GROUP BY Polarity '
    statement1 = 'SELECT Polarity, COUNT(Polarity) FROM Songs GROUP BY Polarity '
    y_values = ['positive', 'negative', 'neutral']
    st = cur.execute(statement)
    positive_t = '0'
    negative_t = '0'
    neutral_t = '0'
    for row in st:
        if row[0] == 'positive':
            positive_t = str(row[1])
        if row[0] == 'negative':
            negative_t = str(row[1])
        if row[0] == 'neutral':
            neutral_t = str(row[1])
    x_values = [int(positive_t), int(negative_t), int(neutral_t)]
    st1 = cur.execute(statement1)
    positive_s = '0'
    negative_s = '0'
    neutral_s = '0'
    for row in st1:
        if row[0] == 'positive':
            positive_s = str(row[1])
        if row[0] == 'negative':
            negative_s = str(row[1])
        if row[0] == 'neutral':
            neutral_s = str(row[1])
    x_values1 = [int(positive_s), int(negative_s), int(neutral_s)]
    trace1 = go.Bar(
        y=y_values,
        x=x_values,
        name='Tweets',
        orientation = 'h',
        marker = dict(
            color = 'rgba(246, 78, 139, 0.6)',
            line = dict(
                color = 'rgba(246, 78, 139, 1.0)',
                width = 3)
        )
    )
    trace2 = go.Bar(
        y=y_values,
        x=x_values1,
        name='Songs',
        orientation = 'h',
        marker = dict(
            color = 'rgba(58, 71, 80, 0.6)',
            line = dict(
                color = 'rgba(58, 71, 80, 1.0)',
                width = 3)
        )
    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='Polarity of Tweets versus Songs of {}'.format(artist))

def load_help_text():
    with open('help.txt') as f:
        return f.read()

def process_command():
    help_text = load_help_text()
    resp = ' '
    while resp != 'exit':
        resp = input('Enter a command, or enter help for a list of options: ')
        if resp.lower() == 'help':
            print(help_text)
            continue
        if resp.lower() == 'exit':
            print("Goodbye!")
            break
        if 'artist=' in resp:
            a = resp.split('=')
            if ',' in a[1]:
                b = a[1].split(',')
                init_tweet_table(b[0])
                init_song_table(b[0])
                if 'tweets' in b[1]:
                    if 'polarity' in b[1]:
                        pie_chart(b[0], 'tweets', 'polarity')
                        continue
                    if 'subjectivity' in b[1]:
                        if 'subjectivity pie' in b[1]:
                            pie_chart(b[0], 'tweets', 'polarity')
                            continue
                        else:
                            bar_chart(b[0], 'tweets')
                            continue
                if 'songs' in b[1]:
                    if 'polarity' in b[1]:
                        pie_chart(b[0], 'songs', 'polarity')
                        continue
                    if 'popularity' in b[1]:
                        bar_chart(b[0], 'songs')
                        continue
            else:
                init_song_table(a[1])
                init_tweet_table(a[1])
                horizontal_bar(a[1])
                continue
        if 'artists=' in resp:
            a = resp.split('=')[1:]
            ar = a[0]
            artist_list = ar.split(', ')
            for artist in artist_list:
                init_song_table(artist)
                init_tweet_table(artist)
            bar_chart(artist_list, 'all')
            continue
        else:
            print('Invalid input, please try again.')
            continue


if __name__=="__main__":
    process_command()
