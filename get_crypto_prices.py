#This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
#import requests_cache
import json
import os

#requests_cache.install_cache('cache', backend='sqlite', expire_after=180)

CMC_PRO_API_KEY = os.environ.get("CMC_PRO_API_KEY")
coin_list = ['BAT', 'LTC', 'BTC', 'XLM', 'XRP']

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
        'symbol' : ','.join(coin_list),
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': CMC_PRO_API_KEY,
}

#session = requests_cache.CachedSession() 
session = Session()

session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print("Asset,Current Price")
  for coin in coin_list:
    print("{},{:0.4f}".format(coin, data['data'][coin]['quote']['USD']['price']))

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

