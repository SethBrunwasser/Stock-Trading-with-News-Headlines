import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup

'''
This is simply a utility function to scrape Wikipedia's S&P 500 list for
company names and their corresponding stock tickers to be exported to csv
'''

site = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

def get_list():
	req = requests.get(site, params=None)
	soup = BeautifulSoup(req.content, "html.parser")

	table = soup.find('table', {'class': 'wikitable sortable'})
	
	stock_name_data = {}

	for row in table.findAll('tr'):
		col = row.findAll('td')
		if len(col) > 0:
			ticker_symbol = str(col[0].a.text).strip()
			company_name = str(col[1].a.text).strip()
			stock_name_data[ticker_symbol] = company_name

	return stock_name_data

with open('stock_names.csv', mode='w', newline="") as f:
	fieldnames = ['Ticker Symbol', 'Compay Name']
	writer = csv.writer(f)
	writer.writerow(fieldnames)
	for key, value in get_list().items():
		writer.writerow([key, value])