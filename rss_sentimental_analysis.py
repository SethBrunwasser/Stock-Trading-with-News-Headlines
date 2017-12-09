import re
import feedparser
from textblob import TextBlob


class RssClient(object):

	def __init__(self, link):
		'''
		Creates a RssFeed object to mine News Titles
		'''
		try:
			self.rssFeed = feedparser.parse(link)
		except Error as e:
			raise Exception("Failed to access RSS: " + str(e))

	def get_rss_sentiment(self, title):
		'''
		Uses textblob's sentiment method to classify sentiment
		passed tweet
		'''
		analysis = TextBlob(title)
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

		if count == 'maximum':
			count = len(self.rssFeed['entries'])

		try:
			fetched_titles = [(self.rssFeed['entries'][i].title, self.rssFeed['entries'][i].published) for i in range(0, count)]
			for title, date in fetched_titles:
				# Dictionary that will hold title text and title sentiment
				parsed_title = {}
				parsed_title['text'] = title
				parsed_title['sentiment'] = self.get_rss_sentiment(title)
				parsed_title['datetime'] = date
				titles.append(parsed_title)
			return titles
		except Exception as e:
			raise Exception("Error: " + str(e))
