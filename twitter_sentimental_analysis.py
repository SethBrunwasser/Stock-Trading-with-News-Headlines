import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):

	def __init__(self):
		'''
		Creates a Tweepy API object to mine tweets
		'''
		consumer_key = "TVpdLCDUCftx9P8GmyNLHS60j"
		consumer_key_secret = "3K46M2PE8PwS8odI3zKyz76X4NpRtBHlrqcfmk0phU6wQc4reT"
		access_token = "938993275158925312-WzpBEf600zCUYq5TfoaL3s5QG5HMKX3"
		access_token_secret = "NY8ehID4E8mQVGx4ZbqvmLqIe698KVdPbRDQpavL2K7kh"

		# Attempting authentication
		try:
			self.auth = OAuthHandler(consumer_key, consumer_key_secret)
			self.auth.set_access_token(access_token, access_token_secret)
			self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
		except:
			raise Exception("Error: Authentication failed")

	def clean_tweet(self, tweet):
		'''
		Uses regex to clean tweet by removing links and special characters
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet, scalar=False):
		'''
		Uses textblob's sentiment method to classify sentiment
		passed tweet.
		The scalar parameter will return the polarity ([-1.0, 1.0]) if True
		'''
		analysis = TextBlob(self.clean_tweet(tweet))
		if scalar is False:
			if analysis.sentiment.polarity > 0:
				return 'positive'
			elif analysis.sentiment.polarity == 0:
				return 'neutral'
			else:
				return 'negative'
		else:
			return analysis.sentiment.polarity

	def get_tweets(self, query, count = 10):
		'''
		Uses a query to search for tweets
		'''
		tweets = []
		try:
			fetched_tweets = self.api.search(q = query, count = count)
			for tweet in fetched_tweets:
				# Dictionary that will hold tweet text and tweet sentiment
				parsed_tweet = {}
				
				parsed_tweet['text'] = tweet.text
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text, scalar=True)
				parsed_tweet['datetime'] = tweet.created_at

				if tweet.retweet_count > 0:
					# if a tweet has retweets, ensures that it is only appended once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)
			return tweets
		except tweepy.TweepError as e:
			raise Exception("Error: " + str(e))
