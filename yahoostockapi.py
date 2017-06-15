
import requests 
from datetime import datetime
import pandas as pd
from io import StringIO

class yahoostockapi:


	def __init__(self):
		self.download_url = 'https://query1.finance.yahoo.com/v7/finance/download'
		self.crumb_url = 'https://query1.finance.yahoo.com/v1/test/getcrumb'
		self.cookie_url = 'https://finance.yahoo.com/quote/GC=F?p=GC=F'
		self.crumb = ''


	def connect(self):
		if not self.crumb:
			cookie_response = requests.get(self.cookie_url)
			crumb_response = requests.get(self.crumb_url, cookies=cookie_response.cookies)
			self.cookies = cookie_response.cookies
			self.crumb = crumb_response.text
			
		
	def get_historical_data(self, ticker, begin_date, end_date):
		self.connect()
		url = '%s/%s' % (self.download_url, ticker)
		ts_begin = int(datetime.strptime(begin_date, "%Y-%m-%d").timestamp())
		ts_end = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
		params = {
			'period1': ts_begin,
			'period2': ts_end,
			'interval': '1d',
			'events': 'history',
			'crumb': self.crumb
		}
		data = requests.get(url, params=params, cookies=self.cookies)
		return pd.read_csv(StringIO(data.text))
