from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
import requests
import json
import os
import csv
import pprint
import settings

now = datetime.now()
pp = pprint.PrettyPrinter(depth=6)

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': settings.CMC_PRO_API_KEY,
}

session = Session()
session.headers.update(headers)

parameters = {
        'symbol' : ','.join(settings.COIN_LIST),
}

"""
create a csv file called "message_rules.csv" in the following format:

Asset,Direction,Limit 
BTC,0,7125.00
BTC,1,6950.00

The first column contains the asset symbol, here we have BTC (Bitcon)
The second column tell us if we want this to be greater than or less than the limit
0 = greater than Limit
1 = less than Limit
the last column is the limit we are looking to test in dollars

You can have as many assets as you like

"""
def main():

    current_price_change = {}
    try:
        response = session.get(settings.QUOTE_URL, params=parameters)
        data = json.loads(response.text)
        for coin in settings.COIN_LIST:
            # this needs to be cleaned up, we should get using get and
            # have a plan for the coin not existing
            current_price_change[coin] = float(data['data'][coin]['quote']['USD']['percent_change_1h'])
    except (ConnectionError, Timeout, TooManyRedirects, KeyError) as e:
        print(e)
        return 

    send = False
    message = ""
    with open('message_rules.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asset = row["Asset"].strip()
            direction = int(row["Direction"].strip())
            limit = float(row["Limit"].strip())
            print("{} {} {} {}".format(asset, direction, limit, current_price_change[asset]))            
            if direction == 0 and current_price_change[asset] > limit:
                message += "{} UP, curr {:.3f}% (1hr)\n".format(asset, current_price_change[asset])
                send = True
            elif direction == 1 and current_price_change[asset] < limit:
                message += "{} DOWN, curr {:.3f}% (1hr)\n".format(asset, current_price_change[asset])
                send = True

    if send:
        resp = requests.post(settings.TEXT_URL, {
            'phone': settings.TEXT_NUM,
            'message': message,
            'key': settings.TEXTBELT_KEY,
        })
        print(resp.json)

if __name__ == "__main__":
    main()

