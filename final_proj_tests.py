import unittest
from final_proj import *
#these tests are based off of my cached data (as this is the data that was inputted into my databases)
class TestDatabase(unittest.TestCase):
    def test_tweet_table(self):
        conn = sqlite3.connect('Bazzi.db')
        cur = conn.cursor()
        statement = 'SELECT Popularity, Polarity, Subjectivity FROM Tweets '
        results = cur.execute(statement)
        result = cur.fetchall()[0]
        self.assertEqual(result, (8, 'neutral', 'objective'))
        statement = 'SELECT COUNT(*) FROM Tweets '
        results = cur.execute(statement)
        result = cur.fetchall()[0]
        self.assertEqual(result, (40,))
        statement = 'SELECT [Popularity] FROM Tweets WHERE [Popularity] > 0 '
        results = cur.execute(statement)
        result = cur.fetchall()
        self.assertEqual(len(result), 6)
        conn.close()
    def test_song_table(self):
        conn = sqlite3.connect('Khalid.db')
        cur = conn.cursor()
        statement = 'SELECT Artist FROM Songs '
        result = cur.execute(statement)
        results = cur.fetchall()
        self.assertIn(('Khalid'), results[0])
        statement = 'SELECT Name FROM Songs WHERE Album_name = "American Teen" '
        results = cur.execute(statement)
        result = cur.fetchall()
        self.assertEqual(len(result), 15)
        statement = 'SELECT  Name, Popularity From Songs ORDER BY Popularity DESC '
        results = cur.execute(statement)
        result = cur.fetchall()[1]
        self.assertEqual(result, ("Silence", 91))
        statement = 'SELECT  Polarity, COUNT(Polarity) FROM Songs WHERE Polarity NOT NULL GROUP BY Polarity '
        results = cur.execute(statement)
        result = cur.fetchall()[0]
        self.assertEqual(result, ('negative', 15))
        conn.close()
class TestSongClass(unittest.TestCase):
    def test_init_and_artist_request(self):
        artist = artist_request('Khalid')
        s = artist[3]
        song = Song('Khalid', s)
        self.assertEqual(song.artist, 'Khalid')
        self.assertEqual(song.name, 'Location')
        self.assertEqual(song.popularity, 87)
        self.assertEqual(song.album_name, 'Single')
class TestTweetClass(unittest.TestCase):
    def test_init_and_twitter_request(self):
        tweets = twitter_request('Khalid')
        self.assertEqual(len(tweets), 21)
        tweet = tweets[0]
        self.assertEqual(tweet.popularity_score, tweet.retweet_count*2 + tweet.favorite_count*3)
        self.assertEqual(tweet.screen_name, 'RapFavorites')
        self.assertIn('Khalid', tweet.text)


unittest.main()
