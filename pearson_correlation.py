import numpy as np
import quandl
from find_companies import TwitterResults

'''
Calculating pearson correlation using quandl stock data.
'''


twitter_results = TwitterResults()
profiles = twitter_results[0]

average_polarities = [(company['ticker'], company['average_polarity']) for company in profiles]

def get_netChange(ticker):
	data = quandl.get("WIKI/"+ticker, rows=2)
	return data[['Close']].diff().iloc[1]['Close']

tickers_netChange_polarity = []
for ticker, polarity in average_polarities[::10]:
	try:
		tickers_netChange_polarity.append((ticker, get_netChange(ticker), polarity))
	except ValueError as e:
		raise Exception(e)

tickers = [ticker[0] for ticker in tickers_netChange_polarity]
changes = [changes[1] for changes in tickers_netChange_polarity]
polarities = [polarities[2] for polarities in tickers_netChange_polarity]

correlation = np.corrcoef(polarities, changes)[0, 1]
print("Correlation between polarities and net change: {}".format(correlation))