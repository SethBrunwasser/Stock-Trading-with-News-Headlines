import pandas as pd
import numpy as np
from twitter_sentimental_analysis import TwitterClient
import rss_sentimental_analysis

'''
This utility function is used to search through Tweets/News Headlines
for company names and return the found companies and where they were found
'''
stock_names_df = pd.read_csv("stock_names.csv", header=0)
ticker_list = stock_names_df['Ticker Symbol']
company_list = stock_names_df['Compay Name'][:500]


def searchTwitter(query, count):
	tweetAPI = TwitterClient()
	tweets = tweetAPI.get_tweets(query, count=count)
	return tweets

def searchRssFeed(link):
	rssFeed = RssClient(link)
	titles = rssFeed.get_titles(count=maximum)
	return titles

maxPositiveReputation = {}
maxNegativeReputation = {}
mostConfidentReputation = {}

for name in company_list:
	tweets = searchTwitter(name, count=200)
	posTweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	negTweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	neuTweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
	
	profile = {'company': name, 'percent_positive': len(posTweets)/len(tweets), 
				'percent_negative': len(negTweets)/len(tweets), 'percent_neutral': len(neuTweets)/len(tweets)}
	
	print("Current Profile: {}".format(profile['company']))
	
	if not maxPositiveReputation:
		maxPositiveReputation = profile
		maxNegativeReputation = profile
		mostConfidentReputation = profile
	else:
		if maxPositiveReputation['percent_positive'] < profile['percent_positive']:
			maxPositiveReputation = profile
		if maxNegativeReputation['percent_negative'] < profile['percent_negative']:
			maxNegativeReputation = profile
		if mostConfidentReputation['percent_neutral'] > profile['percent_neutral']:
			mostConfidentReputation = profile

print("Best Reputation: {}".format(maxPositiveReputation))
print("Worst Reputation: {}".format(maxNegativeReputation))
print("Most Confident Reputation: {}".format(mostConfidentReputation))


