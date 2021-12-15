
from view import crypto_htmlbuilder as crview

import requests
import json
import datetime
import time
from urllib.parse import urlparse

import pickle
import os

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import yaml
basedir = os.getcwd()
with open(basedir + '/config/cryptowand_config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
     
coinmarketcap_apikey = config['api-providers']['coinmarketcap']['apikey']

def get_api_response(url):
    try:
        content = requests.get(url)
        return json.loads(content.content)
    except:
        return 'error'

def load_cmc_current_list(coinmarketcap_apikey):
    url =  config['api-providers']['coinmarketcap']['pricingdata_url']
    parameters = {
        'start': '1',
        'limit': config['coins-to-display'],
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coinmarketcap_apikey,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        json_cmc = data['data']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    # print(json_cmc)
    cmc_current_list = {}
    for coin in json_cmc:
        # print(coin)
        cmc_current_list[coin['symbol']] = {"id": coin['id'], "coin_name": coin['name'],"coin_slug": coin['slug'],
                                            "price": coin['quote']['USD']['price'], "marketcap": coin['quote']['USD']['market_cap'],
                                            "pct_1h": coin['quote']['USD']['percent_change_1h'], "pct_24h": coin['quote']['USD']['percent_change_24h'],
                                            "pct_7d": coin['quote']['USD']['percent_change_7d'], "pct_30d": coin['quote']['USD']['percent_change_30d'],
                                            "rank": coin['cmc_rank'], "symbol": coin['symbol']}

    return (cmc_current_list)


def main():
    print('Just Checking In')


if __name__ == "__main__":
    main()
