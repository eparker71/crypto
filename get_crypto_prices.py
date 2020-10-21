#This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
import settings

parameters = {
        'symbol' : ','.join(settings.COIN_LIST),
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': settings.CMC_PRO_API_KEY,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(settings.QUOTE_URL, params=parameters)
  data = json.loads(response.text)
  print("Asset,Current Price")
  for coin in settings.COIN_LIST:
    print("{},{:0.4f}".format(coin, data['data'][coin]['quote']['USD']['price']))

  # this is a hack to fix a problem retrieving this asset from the api
  print("{},{:0.4f}".format("CGLD", 2.08))

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

