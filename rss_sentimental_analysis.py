import re
import feedparser
from textblob import TextBlob


class RssClient(object):

	def __init__(self, link=rss_link):
		'''
		Creates a RssFeed object to mine News Titles
		'''
		try:
			rssFeed = feedparser.parse(link)
		except Error as e:
			raise Exception("Failed to access RSS: " + str(e))

	def get_rss_sentiment(self, title):
		'''
		Uses textblob's sentiment method to classify sentiment
		passed tweet
		'''
		analysis = TextBlob(self.clean_tweet(tweet))
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_titles(self, count = 10):
		'''
		Uses a query to search for titles
		'''
		titles = []
		try:
			fetched_titles = [self.rssFeed['entries'][i]['title'] for i in range(0, count)]
			for title in fetched_titles:
				# Dictionary that will hold title text and title sentiment
				parsed_title = {}
				parsed_title['text'] = tweet.text
				parsed_title['sentiment'] = self.get_tweet_sentiment(tweet.text)


				if tweet.retweet_count > 0:
					# if a tweet has retweets, ensures that it is only appended once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)
			return tweets
		except tweepy.TweepError as e:
			raise Exception("Error: " + str(e))
