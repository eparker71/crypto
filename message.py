from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import requests
#import requests_cache
import json
import os
import csv
import pprint

pp = pprint.PrettyPrinter(depth=6)

#requests_cache.install_cache('cache', backend='sqlite', expire_after=60)

# You must set these in your environment
TEXTBELT_KEY    = os.environ.get("TEXTBELT_KEY")
CMC_PRO_API_KEY = os.environ.get("CMC_PRO_API_KEY")
TEXT_NUM        = os.environ.get("TEXT_NUM")

# using these API's
quote_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
text_url  = 'https://textbelt.com/text'

coin_list = ['BAT', 'LTC', 'BTC', 'XLM', 'XRP']

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': CMC_PRO_API_KEY,
}

session = Session() #requests_cache.CachedSession()
session.headers.update(headers)

parameters = {
        'symbol' : ','.join(coin_list),
}

"""
create a csv file in the following format:

Asset,Direction,Limit 
BTC,0,7125.00
BTC,1,6950.00

The first column contains the asset symbol, here we have BTC (Bitcon)
The second column tell us if we want this to be greater than or less than the limit
0 = greater than
1 = less than
the last column is the limit we are looking to test in dollars

You can have as many assets as you like
"""
def main():

    current_price = {}
    try:
        response = session.get(quote_url, params=parameters)
        data = json.loads(response.text)
        for coin in coin_list:
            current_price[coin] = float(data['data'][coin]['quote']['USD']['price'])
    except (ConnectionError, Timeout, TooManyRedirects, KeyError) as e:
        print(e)
        return 

    pp.pprint(current_price)
    with open('message_rules.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            send = False
            asset = row["Asset"]
            direction = int(row["Direction"])
            limit = float(row["Limit"])            
            if direction == 0 and current_price[asset] > limit:
                message = "{} is above ${}, curr ${:.3f}".format(asset, limit, current_price[asset])
                send = True
            elif direction == 1 and current_price[asset] < limit:
                message = "{} is below ${}, curr ${:.3f}".format(asset, limit, current_price[asset])
                send = True

            if send:
                resp = requests.post(text_url, {
                    'phone': TEXT_NUM,
                    'message': message,
                    'key': TEXTBELT_KEY,
                })
                print(resp.text)


if __name__ == "__main__":
    main()

