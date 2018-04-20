# SI206finalproject-esaada

This project used a variety of data sources, including the Twitter API, Spotify API, Aylien Sentiment Analysis, and the LyricWikia Database. In order to access these data sources, you can do the following:
APIS:

Twitter API-make an app, include key/secret in secrets file- https://developer.twitter.com/
Spotify API-make an app, include key/secret in secrets file- https://beta.developer.spotify.com/
Ayien sentiment analysis-make an app, include key/secret in secrets file- https://docs.aylien.com/textapi/#getting-started

I have installed modules (included in requirements file), that handle the OAuth for these APIs and make them easier to navigate

My data presentation source is Plotly, and you can set up an account to view the charts at https://plot.ly/

My song data is accessed in the function artist_request(artist), which uses Spotify to gain access to the artist data. From there, I put these songs into the Song class when I initialize my song database.

My Tweet data is accessed in the function twitter_request(artist), which uses the twitter api to access tweets that mention the name of a specific artist. It then inputs these values into the Tweet class to be formatted for my database.

My function get_lyrics takes the name of an artist and runs it through the lyricwikia database to retrieve all of the lyrics to all of their songs (those that are on the database-not all song lyrics are accessible on this database, this is why some of the song sentiments come up as null) to run through the sentiment analysis.

My tweet/lyric sentiment functions use the aylien sentiment analysis to get the sentiment of each tweet or lyric. The API also determines subjectivity/objectivity (this works mostly for tweets, but I still stored this information in my lyric database)

USER GUIDE:

Upon running this code, you will be asked to enter a command. Here is a copy of the help text, which describes the ways in which you can interact with this program:

Commands available: Enter the name of one artist (artist=artist name) followed by optional parameters described below, or a list of artists separated by commas.

If one artist name is entered:
IMPORTANT: If you want to enter an optional value, enter a comma after artist name eg. <artist=artist name, optional values>
	Optional: <tweets> <polarity, subjectivity or subjectivity pie> | <songs> <polarity or popularity>
		-tweets polarity: shows a pie chart of the number of tweets considered positive or negative for the artist
		-tweets subjectivity: shows bar chart of number of objective versus subjective tweets
		-tweets subjectivity pie: shows pie chart of subjective vs objective
		-songs polarity: shows pie chart of positive versus negative songs
		-songs popularity: shows bar chart of songs and popularity

	If no optional values are entered a horizontal bar graph will appear containing the number of positive and negative elements of the artist (tweets + songs)

If a list of artists is entered a grouped bar graph will appear containing each artist in the list with their total positive and negative elements grouped side by side.


Sample inputs:

Single artist, tweets, polarity: <artist=artist name, tweets polarity>
List of artists: <artists=artist1, artist2, artist3>
